from PySide6.QtWidgets import QDialog, QListWidgetItem, QListWidget
from PySide6.QtCore import Qt, QTimer, QSize

from functools import partial

import package.ui.templateslistsialogwindow_ui as templateslistsialogwindow_ui

import package.components.dialogwindow.neddw.nedtemplatedialogwindow as nedtemplatedialogwindow
import package.components.dialogwindow.neddw.nedpagedialogwindow as nedpagedialogwindow
import package.components.widgets.customitemqlistwidget as customitemqlistwidget

# TODO self.__osbm.obj_prodb.set_active_template_for_node_by_id(id_parent_node, id_template) автоматически для единственного шаблона


class TemplatesListDialogWindow(QDialog):
    def __init__(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("TemplatesListDialogWindow __init__(osbm)")
        super(TemplatesListDialogWindow, self).__init__()
        self.ui = templateslistsialogwindow_ui.Ui_TemplatesListDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        self.__icons = self.__osbm.obj_icons.get_icons()
        #
        self.__templates = []
        self.__pages = []
        self.__templates_items = []
        self.__pages_items = []

        # конфигурация
        self.config_lws()
        #
        self.reconfig("REFORM")
        # # подключаем деействия
        self.connecting_actions()

    def resizeEvent(self, event):
        super(TemplatesListDialogWindow, self).resizeEvent(event)
        QTimer.singleShot(0, self, self.update_sizes)

    def update_sizes(self):
        # resize_templates_items
        for item in self.__templates_items:
            widget = self.ui.lw_templates.itemWidget(item)
            item.setSizeHint(item.sizeHint().boundedTo(self.ui.lw_templates.sizeHint()))
            if widget is not None:
                widget_size = widget.sizeHint()
                widget.setFixedSize(
                    QSize(self.ui.lw_pages.size().width() - 2, widget_size.height())
                )
        # resize_pages_items
        for item in self.__pages_items:
            widget = self.ui.lw_pages.itemWidget(item)
            item.setSizeHint(item.sizeHint().boundedTo(self.ui.lw_pages.sizeHint()))
            if widget is not None:
                widget_size = widget.sizeHint()
                widget.setFixedSize(
                    QSize(self.ui.lw_pages.size().width() - 2, widget_size.height())
                )

    def reconfig(
        self, type_reconfig="", open_form=None, open_template=None, open_page=None
    ):
        self.__osbm.obj_logg.debug_logger(
            f"TemplatesListDialogWindow reconfig(type_reconfig): type_reconfig = {type_reconfig}"
        )
        if type_reconfig == "REFORM":
            self.config_forms(open_form)
            self.config_templates(open_template)
            self.config_pages(open_page)
        elif type_reconfig == "RETEMPLATE":
            self.config_templates(open_template)
            self.config_pages(open_page)
        elif type_reconfig == "REPAGE":
            self.config_pages(open_page)

    def config_lws(self):
        self.__osbm.obj_logg.debug_logger("TemplatesListDialogWindow config_lws()")
        for list_widget in [self.ui.lw_templates, self.ui.lw_pages]:
            list_widget.setResizeMode(QListWidget.Adjust)
            list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def config_forms(self, open_form=None):
        self.__osbm.obj_logg.debug_logger("TemplatesListDialogWindow config_forms()")
        #
        forms = self.__osbm.obj_prodb.get_form_nodes()
        combobox = self.ui.combox_forms
        combobox.blockSignals(True)
        combobox.clear()
        for index, form in enumerate(forms):
            combobox.addItem(form.get("name_node"), form)
        #
        if combobox.count() > 0:
            if open_form:
                index_form = next(
                    (
                        i
                        for i, form in enumerate(forms)
                        if form.get("id_node") == open_form.get("id_node")
                    ),
                    0,
                )
                if index_form is not None:
                    combobox.setCurrentIndex(index_form)
                else:
                    combobox.setCurrentIndex(0)
            else:
                combobox.setCurrentIndex(0)
        combobox.blockSignals(False)

    def config_templates(self, open_template=None):
        self.__osbm.obj_logg.debug_logger(
            "TemplatesListDialogWindow config_templates()"
        )
        form = self.ui.combox_forms.currentData()

        print(f"form = {form}")
        # TODO Подумать про PDF_NODE
        if form:
            templates = self.__osbm.obj_prodb.get_templates_by_form(form)
            self.__templates = templates
            self.__templates_items = []
            list_widget = self.ui.lw_templates
            #
            id_active_template = form.get("id_active_template")
            print(f"form = {form}")
            print(f"templates = {templates}")
            list_widget.blockSignals(True)
            list_widget.clear()
            for template in templates:
                is_active = False
                if template.get("id_template") == id_active_template:
                    is_active = True
                custom_widget = customitemqlistwidget.CustomItemQListWidget(
                    self.__osbm, "TEMPLATE", template, is_active
                )
                item = QListWidgetItem()
                item.setData(0, template)
                # Указываем размер элемента
                item.setSizeHint(custom_widget.sizeHint())
                item.setSizeHint(item.sizeHint().boundedTo(list_widget.sizeHint()))
                list_widget.addItem(item)
                # Устанавливаем виджет для элемента
                list_widget.setItemWidget(item, custom_widget)
                # кнопки
                self.config_buttons_for_item(custom_widget)
                #
                self.__templates_items.append(item)
            print(f"self.__templates = {self.__templates}")
            if self.__templates_items:
                # выбор нужного шаблона
                if open_template:
                    index_template = next(
                        (
                            i
                            for i, template in enumerate(templates)
                            if template.get("id_template")
                            == open_template.get("id_template")
                        ),
                        0,
                    )
                    list_widget.setCurrentRow(index_template)
                else:
                    list_widget.setCurrentRow(0)
            list_widget.blockSignals(False)

    def config_pages(self, open_page=None):
        self.__osbm.obj_logg.debug_logger("TemplatesListDialogWindow config_pages()")
        item_template = self.ui.lw_templates.currentItem()
        if item_template is not None:
            print("if item_template is not None:")
            template = item_template.data(0)
            # сортированный список страниц
            pages = self.__osbm.obj_prodb.get_pages_by_template(template)
            self.__pages = pages
            self.__pages_items = []
            list_widget = self.ui.lw_pages
            #
            list_widget.blockSignals(True)
            list_widget.clear()
            for page in pages:
                custom_widget = customitemqlistwidget.CustomItemQListWidget(
                    self.__osbm, "PAGE", page
                )
                item = QListWidgetItem()
                item.setData(0, page)
                # Указываем размер элемента
                item.setSizeHint(custom_widget.sizeHint())
                item.setSizeHint(item.sizeHint().boundedTo(list_widget.sizeHint()))
                list_widget.addItem(item)
                # Устанавливаем виджет для элемента
                list_widget.setItemWidget(item, custom_widget)
                # кнопки
                self.config_buttons_for_item(custom_widget)
                #
                self.__pages_items.append(item)
            #
            if self.__pages_items:
                if open_page:
                    index_template = next(
                        (
                            i
                            for i, page in enumerate(pages)
                            if page.get("id_page") == open_page.get("id_page")
                        ),
                        0,
                    )
                    list_widget.setCurrentRow(index_template)
                elif self.__templates_items:
                    list_widget.setCurrentRow(0)
            #

            list_widget.blockSignals(False)

    def config_buttons_for_item(self, item_widget):
        self.__osbm.obj_logg.debug_logger(
            f"TemplatesListDialogWindow config_buttons_for_item(item_widget)\nitem_widget = {item_widget}"
        )
        edit_button = item_widget.get_btn_edit()
        delete_button = item_widget.get_btn_delete()
        type_window = item_widget.get_type_window()
        edit_button.clicked.connect(
            partial(
                self.edit_item,
                type_window=type_window,
                data=item_widget.get_data(),
                is_active=item_widget.get_is_active()
            )
        )
        delete_button.clicked.connect(
            partial(
                self.delete_item, type_window=type_window, data=item_widget.get_data(), is_active=item_widget.get_is_active()
            )
        )

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger(
            "TemplatesListDialogWindow connecting_actions()"
        )
        # кнопки
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")
        self.ui.btn_add_page.clicked.connect(self.add_page)
        self.ui.btn_add_page.setShortcut("Ctrl+P")
        self.ui.btn_add_template.clicked.connect(self.add_template)
        self.ui.btn_add_template.setShortcut("Ctrl+T")
        # смена индекса
        self.ui.combox_forms.currentIndexChanged.connect(
            lambda index: self.reconfig("RETEMPLATE")
        )
        self.ui.lw_templates.currentItemChanged.connect(
            lambda item: self.reconfig("REPAGE")
        )

    def edit_item(self, type_window, data, is_active=False):
        self.__osbm.obj_logg.debug_logger(
            f"TemplatesListDialogWindow edit_item(btn):\ntype_window = {type_window}\n data = {data}"
        )
        if type_window == "TEMPLATE":
            template = data
            result = self.ned_temp_dw("edit", template, is_active)
            if result:
                # СТРАНИЦА obj_nedtempdw
                data = self.__osbm.obj_nedtempdw.get_data()
                name_template = data.get("name_template")
                self.__osbm.obj_prodb.set_new_name_for_template(template, name_template)
                # is_active
                # order у template остутсвует
                is_active = data.get("IS_ACTIVE")
                if is_active:
                    id_parent_node = template.get("id_parent_node")
                    id_template = template.get("id_template")
                    self.__osbm.obj_prodb.set_active_template_for_node_by_id(id_parent_node, id_template)
                # было: self.reconfig("RETEMPLATE", None, data, None)
                open_form = self.ui.combox_forms.currentData()
                self.reconfig("REFORM", open_form, data, None)

        elif type_window == "PAGE":
            self.edit_page(data)

    def update_order_pages(self, editpage, new_order_page):
        self.__osbm.obj_logg.debug_logger(
            f"TemplatesListDialogWindow update_order_pages(editpage, new_order_page):\n editpage = {editpage}\n new_order_page = {new_order_page}"
        )
        # подготовка данных (-11 - спец значение)
        id_editpage = editpage.get("id_page", -111)
        pages = [page for page in self.__pages if page.get("id_page") != id_editpage]
        pages = sorted(pages, key=lambda x: x.get("order_page"))
        pages.insert(new_order_page, editpage)
        # обновить значения
        for index, page in enumerate(pages):
            # order_page = page.get("order_page")
            self.__osbm.obj_prodb.set_order_for_page(page, index)

    def delete_item(self, type_window, data, is_active=False):
        self.__osbm.obj_logg.debug_logger(
            f"TemplatesListDialogWindow delete_item(btn):\ntype_window = {type_window}\n data = {data}"
        )
        if type_window == "TEMPLATE":
            name_template = data.get("name_template")
            result = self.__osbm.obj_dw.question_message(
                f'Вы действительно хотите удалить этот шаблон:\n"{name_template}"?'
            )
            if result:
                self.__osbm.obj_prodb.delete_template(data)
                open_form = self.ui.combox_forms.currentData()
                if is_active:  
                    self.set_active_template_after_delete(data, open_form)          
                # было: self.reconfig("RETEMPLATE")
                self.reconfig("REFORM", open_form, None, None)


        elif type_window == "PAGE":
            name_page = data.get("name_page")
            result = self.__osbm.obj_dw.question_message(
                f'Вы действительно хотите удалить эту страницу:\n"{name_page}"?'
            )
            if result:
                self.delete_page(data)
                self.reconfig("REPAGE")

    def set_active_template_after_delete(self, old_data, form):
        self.__osbm.obj_logg.debug_logger(
            f"TemplatesListDialogWindow set_active_template_after_delete(data):\nold_data = {old_data}"
        )
        self.__templates.remove(old_data)
        if self.__templates:
            id_new_template = self.__templates[0].get("id_template")            
            id_parent_node = form.get("id_node")
            self.__osbm.obj_prodb.set_active_template_for_node_by_id(id_parent_node, id_new_template)


    def delete_page(self, page):
        self.__osbm.obj_logg.debug_logger(
            f"TemplatesListDialogWindow delete_page(page):\npage = {page}"
        )
        filename_page = page.get("filename_page")
        self.__osbm.obj_film.delete_page_from_project(filename_page)
        self.__osbm.obj_prodb.delete_page(page)

    def add_page(self):
        self.__osbm.obj_logg.debug_logger("TemplatesListDialogWindow add_page()")
        result = self.ned_page_dw("create")
        item_template = self.ui.lw_templates.currentItem()
        if result and item_template:
            template = item_template.data(0)
            id_parent_template = template.get("id_template")
            #
            data = self.__osbm.obj_nedpagedw.get_data()
            filename_page = data.get("filename_page")
            name_page = data.get("name_page")
            typefile_page = data.get("typefile_page")
            order_page = data.get("order_page")
            # "order_page": -111, ТАК ДОЛЖНО БЫТЬ!!!
            new_page = {
                "id_parent_template": id_parent_template,
                "name_page": name_page,
                "filename_page": filename_page,
                "typefile_page": typefile_page,
                "order_page": -111,
                "included": 1,
            }
            # добавляем вершину
            primary_key = self.__osbm.obj_prodb.insert_page(new_page)
            # обновляем order
            page_for_order = self.__osbm.obj_prodb.get_page_by_id(primary_key)
            self.update_order_pages(page_for_order, order_page)
            # перемещение из temp в forms
            temp_copy_file_path = data.get("TEMP_COPY_FILE_PATH")
            if typefile_page == "DOCX":
                self.__osbm.obj_film.docx_from_temp_to_forms(
                    temp_copy_file_path, filename_page
                )
            elif typefile_page == "PDF":
                self.__osbm.obj_film.pdf_from_temp_to_pdfs(
                    temp_copy_file_path, filename_page
                )
            self.reconfig("REPAGE")

    def edit_page(self, data):
        page = data
        result = self.ned_page_dw("edit", page)
        if result:
            # СТРАНИЦА obj_nedpagedw
            data = self.__osbm.obj_nedpagedw.get_data()
            # Обновить в БД страницу
            typefile_page = data.get("typefile_page")
            edit_page = {
                "id_page": page.get("id_page"),
                "name_page": data.get("name_page"),
                "filename_page": data.get("filename_page"),
                "typefile_page": typefile_page,
            }
            self.__osbm.obj_prodb.update_page(edit_page)
            # обновить order
            self.update_order_pages(data, data.get("order_page"))
            # TODO (Проверять и Удалять в отдельном потоке периодически)
            # перемещение из temp в forms
            new_filename_page = data.get("filename_page")
            temp_copy_file_path = data.get("TEMP_COPY_FILE_PATH")
            if typefile_page == "DOCX":
                self.__osbm.obj_film.docx_from_temp_to_forms(
                    temp_copy_file_path, new_filename_page
                )
            elif typefile_page == "PDF":
                self.__osbm.obj_film.pdf_from_temp_to_pdfs(
                    temp_copy_file_path, new_filename_page
                )
            self.reconfig("REPAGE", None, None, data)

    def add_template(self):
        self.__osbm.obj_logg.debug_logger("TemplatesListDialogWindow add_template()")
        result = self.ned_temp_dw("create")
        if result:
            data = self.__osbm.obj_nedtempdw.get_data()
            name_template = data.get("name_template")
            copy_template = data.get("copy_template")
            # добавить
            form = self.ui.combox_forms.currentData()
            if form:
                id_new_template = self.__osbm.obj_prodb.add_template(
                    name_template, form
                )
                # копирование
                if copy_template != "empty":
                    id_copy_template = copy_template.get("id_template")
                    new_template = {
                        "id_template": id_new_template,
                        "name_template": name_template,
                        "id_parent_node": form.get("id_node"),
                    }
                    old_template = self.__osbm.obj_prodb.get_template_by_id(
                        id_copy_template
                    )
                    self.copy_template(old_template, new_template)
                # активность для текущего
                is_active = data.get("IS_ACTIVE")
                if is_active:
                    id_parent_node = form.get("id_node")
                    id_template = id_new_template
                    self.__osbm.obj_prodb.set_active_template_for_node_by_id(id_parent_node, id_template)
                
                # было: self.reconfig("RETEMPLATE")
                open_form = self.ui.combox_forms.currentData()
                self.reconfig("REFORM", open_form, None, None)


    def copy_template(self, old_template, new_template):
        self.__osbm.obj_logg.debug_logger(
            f"copy_template():\nold_template = {old_template}\nnew_template = {new_template}"
        )
        # поэтапно
        self.copy_template_templates_data(old_template, new_template)
        old_to_new_pages = self.copy_template_pages(old_template, new_template)
        self.copy_template_pages_data(old_to_new_pages)

    def copy_template_templates_data(self, old_template, new_template):
        self.__osbm.obj_logg.debug_logger(
            f"copy_template_templates_data():\nold_template = {old_template}\nnew_template = {new_template}"
        )
        td_pairs = self.__osbm.obj_prodb.get_template_data(old_template)
        for td_pair in td_pairs:
            self.__osbm.obj_prodb.insert_template_data(new_template, td_pair)

    def copy_template_pages(self, old_template, new_template) -> dict:
        self.__osbm.obj_logg.debug_logger(
            f"copy_template_pages() -> dict:\nold_template = {old_template}\nnew_template = {new_template}"
        )
        old_to_new_pages = dict()
        p_pairs = self.__osbm.obj_prodb.get_pages_by_template(old_template)
        for p_pair in p_pairs:
            old_page_filename = p_pair.get("filename_page")
            typefile_page = p_pair.get("typefile_page")
            # копирование
            new_page_filename = self.__osbm.obj_film.copynew_page_for_new_template(
                old_page_filename, typefile_page
            )
            # добавление в бд
            new_page = {
                "id_parent_template": new_template.get("id_template"),
                "name_page": p_pair.get("name_page"),
                "filename_page": new_page_filename,
                "typefile_page": typefile_page,
                "order_page": p_pair.get("order_page"),
                "included": p_pair.get("included"),
            }
            new_id_page = self.__osbm.obj_prodb.insert_page(new_page)
            old_to_new_pages[p_pair.get("id_page")] = new_id_page
        return old_to_new_pages

    def copy_template_pages_data(self, old_to_new_pages):
        self.__osbm.obj_logg.debug_logger(
            f"copy_template_pages_data():\nold_to_new_pages = {old_to_new_pages}"
        )
        for old_id_page, new_id_page in old_to_new_pages.items():
            old_page = {
                "id_page": old_id_page,
            }
            new_page = {
                "id_page": new_id_page,
            }
            pd_pairs = self.__osbm.obj_prodb.get_page_data(old_page)
            for pd_pair in pd_pairs:
                pair = {
                    "id_variable": pd_pair.get("id_variable"),
                }
                self.__osbm.obj_prodb.insert_page_data(new_page, pair)

    def ned_temp_dw(self, type_ned, template=None, is_active=False) -> bool:
        self.__osbm.obj_logg.debug_logger("TemplatesListDialogWindow ned_temp_dw()")
        self.__osbm.obj_nedtempdw = nedtemplatedialogwindow.NedTemplateDialogWindow(
            self.__osbm, type_ned, self.__templates, template, is_active
        )
        result = self.__osbm.obj_nedtempdw.exec()
        return result == QDialog.Accepted

    def ned_page_dw(self, type_ned, page=None) -> bool:
        self.__osbm.obj_logg.debug_logger("TemplatesListDialogWindow ned_page_dw()")
        self.__osbm.obj_nedpagedw = nedpagedialogwindow.NedPageDialogWindow(
            self.__osbm, type_ned, self.__pages, page
        )
        result = self.__osbm.obj_nedpagedw.exec()
        return result == QDialog.Accepted
    