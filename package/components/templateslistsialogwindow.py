from PySide6.QtWidgets import QDialog, QListWidgetItem

from functools import partial

import package.ui.templateslistsialogwindow_ui as templateslistsialogwindow_ui

import package.components.nedtemplatedialogwindow as nedtemplatedialogwindow
import package.components.nedpagedialogwindow as nedpagedialogwindow
import package.components.widgets.customitemqlistwidget as customitemqlistwidget


class TemplatesListDialogWindow(QDialog):
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger(
            "TemplatesListDialogWindow __init__(obs_manager)"
        )
        super(TemplatesListDialogWindow, self).__init__()
        self.ui = templateslistsialogwindow_ui.Ui_TemplatesListDialogWindow()
        self.ui.setupUi(self)
        #
        self.__templates = []
        self.__pages = []
        # конфигурация
        self.config_forms()
        self.config_templates()
        self.config_pages()
        # # подключаем деействия
        self.connecting_actions()

    def reconfig(self):
        self.__obs_manager.obj_l.debug_logger("TemplatesListDialogWindow reconfig()")
        self.config_templates()
        self.config_pages()

    def config_forms(self):
        self.__obs_manager.obj_l.debug_logger(
            "TemplatesListDialogWindow config_forms()"
        )
        # TODO Подумать про сортировку (алфавит?)
        forms = self.__obs_manager.obj_pd.get_form_nodes()
        combobox = self.ui.combox_forms
        combobox.blockSignals(True)
        combobox.clear()
        for index, form in enumerate(forms):
            combobox.addItem(form.get("name_node"), form)
        combobox.blockSignals(False)

    def config_templates(self):
        self.__obs_manager.obj_l.debug_logger(
            "TemplatesListDialogWindow config_templates()"
        )
        form = self.ui.combox_forms.currentData()
        if form is not None:
            templates = self.__obs_manager.obj_pd.get_templates_by_form(form)
            self.__templates = templates
            print(f"form = {form}")
            print(f"templates = {templates}")
            list_widget = self.ui.lw_templates
            list_widget.blockSignals(True)
            list_widget.clear()
            for template in templates:
                custom_widget = customitemqlistwidget.CustomItemQListWidget(
                    self.__obs_manager, "TEMPLATE", template
                )
                item = QListWidgetItem()
                item.setData(0, template)
                # Указываем размер элемента
                item.setSizeHint(custom_widget.sizeHint())
                list_widget.addItem(item)
                # Устанавливаем виджет для элемента
                list_widget.setItemWidget(item, custom_widget)
                # кнопки
                self.config_buttons_for_item(custom_widget)
            list_widget.setCurrentRow(0)
            list_widget.blockSignals(False)

    def config_pages(self):
        self.__obs_manager.obj_l.debug_logger(
            "TemplatesListDialogWindow config_pages()"
        )
        item_template = self.ui.lw_templates.currentItem()
        if item_template is not None:
            template = item_template.data(0)
            pages = self.__obs_manager.obj_pd.get_pages_by_template(template)
            self.__pages = pages
            list_widget = self.ui.lw_pages
            list_widget.blockSignals(True)
            list_widget.clear()
            for page in pages:
                custom_widget = customitemqlistwidget.CustomItemQListWidget(
                    self.__obs_manager, "PAGE", page
                )
                item = QListWidgetItem()
                item.setData(0, page)
                # Указываем размер элемента
                item.setSizeHint(custom_widget.sizeHint())
                list_widget.addItem(item)
                # Устанавливаем виджет для элемента
                list_widget.setItemWidget(item, custom_widget)
                # кнопки
                self.config_buttons_for_item(custom_widget)
            list_widget.setCurrentRow(0)
            list_widget.blockSignals(False)

    def config_buttons_for_item(self, item_widget):
        self.__obs_manager.obj_l.debug_logger(
            f"TemplatesListDialogWindow config_buttons_for_item(item_widget)\nitem_widget = {item_widget}"
        )
        edit_button = item_widget.get_btn_edit()
        delete_button = item_widget.get_btn_delete()
        type_window = item_widget.get_type_window()
        edit_button.clicked.connect(
            partial(
                self.edit_item, type_window=type_window, data=item_widget.get_data()
            )
        )
        delete_button.clicked.connect(
            partial(
                self.delete_item, type_window=type_window, data=item_widget.get_data()
            )
        )

    def connecting_actions(self):
        self.__obs_manager.obj_l.debug_logger(
            "TemplatesListDialogWindow connecting_actions()"
        )
        # кнопки
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_add_page.clicked.connect(self.add_page)
        self.ui.btn_add_template.clicked.connect(self.add_template)
        # смена индекса
        self.ui.combox_forms.currentIndexChanged.connect(
            self.combox_forms_index_changed
        )
        self.ui.lw_templates.currentItemChanged.connect(self.config_pages)

    def combox_forms_index_changed(self):
        self.__obs_manager.obj_l.debug_logger(
            "TemplatesListDialogWindow combox_forms_index_changed()"
        )
        self.config_templates()
        self.config_pages()

    def edit_item(self, type_window, data):
        self.__obs_manager.obj_l.debug_logger(
            f"TemplatesListDialogWindow delete_item(btn):\ntype_window = {type_window}\n data = {data}"
        )
        if type_window == "TEMPLATE":
            template = data
            result = self.ned_temp_dw("edit", template)
            if result:
                data = self.__obs_manager.obj_ned_temp_dw.get_data()
                name_template = data.get("name_template")
                self.__obs_manager.obj_pd.set_new_name_for_template(
                    template, name_template
                )
                self.reconfig()

        elif type_window == "PAGE":
            page = data
            result = self.ned_page_dw("edit", page)
            if result:
                item_template = self.ui.lw_templates.currentItem()
                if item_template is not None:
                    template = item_template.data(0)
                    data = self.__obs_manager.obj_ned_temp_dw.get_data()
                    # Если поменялся документ то нужно его обновить (удаля старый)
                    old_filename_page = page.get("filename_page")
                    new_filename_page = data.get("filename_page")
                    if old_filename_page != new_filename_page:
                        self.__obs_manager.obj_ffm.delete_page_from_project(
                            old_filename_page
                        )
                    # Если поменялся order
                    old_order_page = page.get("order_page")
                    new_order_page = data.get("order_page")
                    if old_order_page != new_order_page:
                        self.update_order_pages(page, new_order_page)
                    self.update_page(data)
                    self.reconfig()

    def update_order_pages(self, editpage, new_order_page):
        self.__obs_manager.obj_l.debug_logger(
            f"TemplatesListDialogWindow update_order_pages(id_editpage, new_order_page):\editpage = {editpage}\nnew_order_page = {new_order_page}"
        )
        # подготовка данных
        id_editpage = editpage.get("id_page")
        pages = [page for page in self.__pages if page.get("id_page") != id_editpage]
        pages = sorted(pages, key=lambda x: x.get("order_page"))
        pages.insert(new_order_page, editpage)
        # обновить значения
        for index, page in enumerate(pages):
            order_page = page.get("order_page")
            if order_page != index:
                self.__obs_manager.obj_pd.set_order_for_page(page, index)

    def delete_item(self, type_window, data):
        self.__obs_manager.obj_l.debug_logger(
            f"TemplatesListDialogWindow delete_item(btn):\ntype_window = {type_window}\n data = {data}"
        )
        if type_window == "TEMPLATE":
            name_template = data.get("name_template")
            result = self.__obs_manager.obj_dw.question_message(
                f"Вы точно хотите удалить {name_template}?"
            )
            if result:
                self.delete_pages()
                self.__obs_manager.obj_pd.delete_template(data)
                self.__obs_manager.obj_pd.delete_template_all_data(data)
                self.reconfig()
        elif type_window == "PAGE":
            name_page = data.get("name_page")
            result = self.__obs_manager.obj_dw.question_message(
                f"Вы точно хотите удалить {name_page}?"
            )
            if result:
                self.delete_page(data)
                self.reconfig()

    def delete_pages(self):
        self.__obs_manager.obj_l.debug_logger(
            "TemplatesListDialogWindow delete_pages()"
        )
        pages = self.__pages
        for page in pages:
            self.delete_page(page)

    def delete_page(self, page):
        self.__obs_manager.obj_l.debug_logger(f"TemplatesListDialogWindow delete_page(page):\npage = {page}")
        filename_page = page.get("filename_page")
        self.__obs_manager.obj_ffm.delete_page_from_project(filename_page)
        self.__obs_manager.obj_pd.delete_page(page)
        self.__obs_manager.obj_pd.delete_all_page_data(page)
            

    def add_page(self):
        self.__obs_manager.obj_l.debug_logger("TemplatesListDialogWindow add_page()")
        result = self.ned_page_dw("create")
        if result:
            item_template = self.ui.lw_templates.currentItem()
            if item_template is not None:
                template = item_template.data(0)
                name_template = template.get("name_template")
                id_parent_template = template.get("id_template")
                #
                data = self.__obs_manager.obj_ned_temp_dw.get_data()
                filename_page = data.get("filename_page")
                name_page = data.get("name_page")
                self.__obs_manager.obj_ffm.docx_from_temp_to_forms(
                    filename_page, name_template
                )
                order_page = self.get_max_order_page() + 1
                new_page = {
                    "id_parent_template": id_parent_template,
                    "name_page": name_page,
                    "filename_page": filename_page,
                    "order_page": order_page,
                    "included": 1,
                }
                self.__obs_manager.obj_pd.insert_page(new_page)
                self.reconfig()

    def get_max_order_page(self) -> int:
        self.__obs_manager.obj_l.debug_logger(
            "TemplatesListDialogWindow get_max_order_page()"
        )
        max_value = 0
        for page in self.__pages:
            if page.get("order_page") > max_value:
                max_value = page.get("order_page")
        return max_value

    def add_template(self):
        self.__obs_manager.obj_l.debug_logger(
            "TemplatesListDialogWindow add_template()"
        )
        result = self.ned_temp_dw("create")
        if result:
            data = self.__obs_manager.obj_ned_temp_dw.get_data()
            name_template = data.get("name_template")
            copy_template = data.get("copy_template")
            # добавить
            form = self.ui.combox_forms.currentData()
            id_new_template = self.__obs_manager.obj_pd.add_template(
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
                old_template = self.__obs_manager.obj_pd.get_template_by_id(
                    id_copy_template
                )
                self.copy_template(old_template, new_template)
            self.reconfig()

    def copy_template(self, old_template, new_template):
        self.copy_template_templates_data(old_template, new_template)
        old_to_new_pages = self.copy_template_pages(old_template, new_template)
        self.copy_template_pages_data(old_to_new_pages)

    def copy_template_templates_data(self, old_template, new_template):
        self.__obs_manager.obj_l.debug_logger(
            f"copy_template_templates_data():\nold_template = {old_template}\nnew_template = {new_template}"
        )
        td_pairs = self.__obs_manager.obj_pd.get_template_data(old_template)
        for td_pair in td_pairs:
            self.__obs_manager.obj_pd.insert_template_data(new_template, td_pair)

    def copy_template_pages(self, old_template, new_template) -> dict:
        self.__obs_manager.obj_l.debug_logger(
            f"copy_template_pages() -> dict:\nold_template = {old_template}\nnew_template = {new_template}"
        )
        old_to_new_pages = dict()
        p_pairs = self.__obs_manager.obj_pd.get_pages_by_template(old_template)
        for p_pair in p_pairs:
            old_page_filename = p_pair.get("filename_page")
            # копирование
            new_page_filename = (
                self.__obs_manager.obj_ffm.copynew_page_for_new_template(
                    old_page_filename
                )
            )
            # добавление в бд
            new_page = {
                "id_parent_template": new_template.get("id_template"),
                "name_page": p_pair.get("name_page"),
                "filename_page": new_page_filename,
                "order_page": p_pair.get("order_page"),
                "included": p_pair.get("included"),
            }
            new_id_page = self.__obs_manager.obj_pd.insert_page(new_page)
            old_to_new_pages[p_pair.get("id_page")] = new_id_page
        return old_to_new_pages

    def copy_template_pages_data(self, old_to_new_pages):
        self.__obs_manager.obj_l.debug_logger(
            f"copy_template_pages_data():\nold_to_new_pages = {old_to_new_pages}"
        )
        for old_id_page, new_id_page in old_to_new_pages.items():
            old_page = {
                "id_page": old_id_page,
            }
            new_page = {
                "id_page": new_id_page,
            }
            pd_pairs = self.__obs_manager.obj_pd.get_page_data(old_page)
            for pd_pair in pd_pairs:
                pair = {
                    "id_tag": pd_pair.get("id_tag"),
                }
                self.__obs_manager.obj_pd.insert_page_data(new_page, pair)

    def ned_temp_dw(self, type_ned, template=None) -> bool:
        self.__obs_manager.obj_l.debug_logger("TemplatesListDialogWindow ned_temp_dw()")
        self.__obs_manager.obj_ned_temp_dw = (
            nedtemplatedialogwindow.NedTemplateDialogWindow(
                self.__obs_manager, type_ned, self.__templates, template
            )
        )
        result = self.__obs_manager.obj_ned_temp_dw.exec()
        return result == QDialog.Accepted

    def ned_page_dw(self, type_ned, page=None) -> bool:
        self.__obs_manager.obj_l.debug_logger("TemplatesListDialogWindow ned_page_dw()")
        self.__obs_manager.obj_ned_page_dw = nedpagedialogwindow.NedPageDialogWindow(
            self.__obs_manager, type_ned, self.__pages, page
        )
        result = self.__obs_manager.obj_ned_page_dw.exec()
        return result == QDialog.Accepted
