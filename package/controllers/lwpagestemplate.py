from PySide6.QtWidgets import QListWidgetItem


class MyListWidgetItem(QListWidgetItem):
    """
    Кастомный QListWidgetItem с полем page.
    """

    def __init__(self, page):
        super().__init__()
        self.page = page

    def get_page(self):
        return self.page


class LWPagesTemplate:
    def __init__(self):
        self.__lw_pages_template = None
        self.__icons = None

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger(
            "LWPagesTemplate setting_all_osbm()"
        )

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
        self.__lw_pages_template.itemClicked.connect(
            lambda current: self.item_page_updated(current)
        )

    def is_page_template_selected(self):
        self.__osbm.obj_logg.debug_logger("LWPagesTemplate get_lw_pages_template()")
        return self.__lw_pages_template.currentItem()

    def get_page_by_current_item(self):
        self.__osbm.obj_logg.debug_logger(
            "LWPagesTemplate get_page_by_current_item()"
        )
        current = self.__lw_pages_template.currentItem()
        if current is None:
            return None
        return current.get_page()

    def item_page_updated(self, current):
        """
        Слот для сигнала itemClicked.
        """
        self.__osbm.obj_logg.debug_logger(
            f"LWPagesTemplate item_page_updated(current):\ncurrent = {current}"
        )
        page = current.get_page()
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
        pdf_path = str()
        try:
            pdf_path = self.__osbm.obj_conv.create_one_page_pdf(page)
        except self.__osbm.obj_ers.MsWordError:
            self.__osbm.obj_offp.terminate_msword()
            self.__osbm.obj_stab.update_status_msword_label(False)
            if is_convert_flag:
                msg = "Отображение недоступно! Выбранный конвертер перестал работать. Сохранение при этом доступно."
                self.__osbm.obj_dw.warning_message(msg)
                self.__osbm.obj_stab.set_message(msg)

        except self.__osbm.obj_ers.LibreOfficeError:
            self.__osbm.obj_offp.terminate_libreoffice()
            self.__osbm.obj_stab.update_status_libreoffice_label(False)
            if is_convert_flag:
                msg = "Отображение недоступно! Выбранный конвертер перестал работать. Сохранение при этом доступно."
                self.__osbm.obj_dw.warning_message(msg)
                self.__osbm.obj_stab.set_message(msg)

        except Exception as e:
            self.__osbm.obj_logg.error_logger(
                f"Error in create_and_view_current_page(page): {e}"
            )

        if pdf_path:
            self.__osbm.obj_pdfv.load_and_show_pdf_document(pdf_path)
        else:
            self.__osbm.obj_pdfv.set_empty_pdf_view()

    def current_page_to_pdf(self):
        self.__osbm.obj_logg.debug_logger(
            "LWPagesTemplate IN current_page_to_pdf()"
        )
        current = self.__lw_pages_template.currentItem()
        page = current.get_page()
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
                item = MyListWidgetItem(page)
                item.setText(page.get("name_page"))
                item.setIcon(self.__icons.get("page"))
                self.__lw_pages_template.addItem(item)
        self.__lw_pages_template.blockSignals(False)

# obj_lwpt = LWPagesTemplate()
