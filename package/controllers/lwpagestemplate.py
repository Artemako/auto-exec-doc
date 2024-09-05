from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt, QRect


class LWPagesTemplate:
    def __init__(self):
        self.__lw_pages_template = None
        self.__icons = None

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("LWPagesTemplate setting_all_osbm()")

    def connect_pages_template(self, lw_pt):
        """
        Подключить _lw_pages_template.
        """
        self.__osbm.obj_logg.debug_logger(
            f"LWPagesTemplate connect_pages_template(lw_pt):\nlw_pt = {lw_pt}"
        )
        self.__lw_pages_template = lw_pt
        self.__icons = self.__osbm.obj_icons.get_icons()
        self.clear_pt()
        # Подключение сигналов
        self.__lw_pages_template.itemClicked.connect(self.on_item_clicked)
        self.__lw_pages_template.itemChanged.connect(self.on_item_changed)

    def on_item_clicked(self, item):
        self.__osbm.obj_logg.debug_logger(
            f"LWPagesTemplate on_item_clicked(item):\nitem = {item}"
        )
        # проверка на чекбокс
        item_rect = self.__lw_pages_template.visualItemRect(item)
        mouse_position = self.__lw_pages_template.mapFromGlobal(self.__lw_pages_template.cursor().pos())
        # Определяем область чекбокса
        checkbox_rect = QRect(item_rect.topLeft(), item_rect.size())
        checkbox_rect.setWidth(20)
        if checkbox_rect.contains(mouse_position):
            return 
        else:
            # открываем страницу
            self.item_page_updated(item)

    def on_item_changed(self, item):
        """
        Слот для обработки изменений состояния чекбокса.
        """
        self.__osbm.obj_logg.debug_logger(
            f"LWPagesTemplate on_item_changed(item):\nitem = {item}"
        )
        if item.checkState() in (Qt.Checked, Qt.Unchecked):
            self.__osbm.obj_prodb.set_included_for_page(
                item.data(Qt.UserRole), int(item.checkState() == Qt.Checked)
            )

    def is_page_template_selected(self):
        self.__osbm.obj_logg.debug_logger("LWPagesTemplate get_lw_pages_template()")
        return self.__lw_pages_template.currentItem()

    def get_page_by_current_item(self):
        self.__osbm.obj_logg.debug_logger("LWPagesTemplate get_page_by_current_item()")
        current = self.__lw_pages_template.currentItem()
        return current.data(Qt.UserRole) if current else None

    def item_page_updated(self, current):
        """
        Слот для сигнала itemClicked.
        """
        self.__osbm.obj_logg.debug_logger(
            f"LWPagesTemplate item_page_updated(current):\ncurrent = {current}"
        )
        page = current.data(Qt.UserRole)
        # Обновить SAInputForms
        self.__osbm.obj_saif.update_scrollarea(page)
        # открыть pdf форму для текущей страницы
        self.create_and_view_current_page(page)

    def create_and_view_current_page(self, page):
        self.__osbm.obj_logg.debug_logger(
            f"LWPagesTemplate create_and_view_current_page(page):\npage = {page}"
        )
        app_converter = self.__osbm.obj_setdb.get_app_converter()
        status_msword = self.__osbm.obj_offp.get_status_msword()
        status_libreoffice = self.__osbm.obj_offp.get_status_libreoffice()
        is_convert_flag = True
        if app_converter == "MSWORD" and status_msword:
            pass
        elif app_converter == "LIBREOFFICE" and status_libreoffice:
            pass
        else:
            msg = "Отображение недоступно! Выбранный конвертер не работает. Сохранение при этом доступно."
            self.__osbm.obj_dw.warning_message(msg)
            self.__osbm.obj_stab.set_message(msg)
            is_convert_flag = False
        #
        if is_convert_flag:
            pdf_path = str()
            is_error = False
            self.__osbm.obj_dw.process_show_start()
            try:
                pdf_path = self.__osbm.obj_conv.create_one_page_pdf(page)
            except self.__osbm.obj_com.errors.MsWordError:
                self.__osbm.obj_offp.terminate_msword()
                self.__osbm.obj_stab.update_status_msword_label(False)
                if is_convert_flag:
                    msg = "Отображение недоступно! Выбранный конвертер перестал работать. Сохранение при этом доступно."
                    self.__osbm.obj_dw.warning_message(msg)
                    self.__osbm.obj_stab.set_message(msg)
                is_error = True

            except self.__osbm.obj_com.errors.LibreOfficeError:
                self.__osbm.obj_offp.terminate_libreoffice()
                self.__osbm.obj_stab.update_status_libreoffice_label(False)
                if is_convert_flag:
                    msg = "Отображение недоступно! Выбранный конвертер перестал работать. Сохранение при этом доступно."
                    self.__osbm.obj_dw.warning_message(msg)
                    self.__osbm.obj_stab.set_message(msg)
                is_error = True

            except Exception as e:
                self.__osbm.obj_logg.error_logger(
                    f"Error in create_and_view_current_page(page): {e}"
                )
                self.__osbm.obj_dw.warning_message(f"Ошибка: {e}")
                is_error = True
            #
            self.__osbm.obj_dw.process_show_end()
        #
        if is_convert_flag and not is_error and pdf_path:
            self.__osbm.obj_pdfv.load_and_show_pdf_document(pdf_path)
        else:
            self.__osbm.obj_pdfv.set_empty_pdf_view()

    def current_page_to_pdf(self):
        self.__osbm.obj_logg.debug_logger("LWPagesTemplate IN current_page_to_pdf()")
        current = self.__lw_pages_template.currentItem()
        page = current.data(Qt.UserRole)
        self.create_and_view_current_page(page)

    def clear_pt(self):
        self.__osbm.obj_logg.debug_logger("LWPagesTemplate clear_pt()")
        try:
            if self.__lw_pages_template is not None:
                self.__lw_pages_template.blockSignals(True)
                self.__lw_pages_template.clear()
                self.__lw_pages_template.blockSignals(False)
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"Error in clear_pt(): {e}")

    def update_pages_template(self, template):
        """
        Обновить _lw_pages_template.
        """
        self.__osbm.obj_logg.debug_logger(
            f"LWPagesTemplate update_pages_template(template):\ntemplate = {template}"
        )
        self.clear_pt()
        self.__lw_pages_template.blockSignals(True)
        if template:
            pages = self.__osbm.obj_prodb.get_pages_by_template(template)
            for page in pages:
                print(f"page = {page}")
                item = QListWidgetItem()
                item.setText(page.get("name_page"))
                item.setCheckState(Qt.Checked if page.get("included") else Qt.Unchecked)
                #
                typefile_page = page.get("typefile_page")
                if typefile_page == "DOCX":
                    item.setIcon(self.__icons.get("page"))
                elif typefile_page == "PDF":
                    item.setIcon(self.__icons.get("pdf"))
                #
                item.setData(Qt.UserRole, page)
                self.__lw_pages_template.addItem(item)

        self.__lw_pages_template.blockSignals(False)


# obj_lwpt = LWPagesTemplate()
