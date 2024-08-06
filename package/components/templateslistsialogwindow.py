from PySide6.QtWidgets import QDialog, QListWidgetItem

from functools import partial

import package.ui.templateslistsialogwindow_ui as templateslistsialogwindow_ui

import package.components.nedtemplatedialogwindow as nedtemplatedialogwindow
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
        # конфигурация
        self.config_forms()
        self.config_templates()
        self.config_pages()
        # # подключаем деействия
        self.connecting_actions()

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
        self.ui.lw_templates.currentItemChanged.connect(self.config_pages())

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
        # todo
        if type_window == "TEMPLATE":
            result = self.ned_temp_dw("create")
            if result:
                ...

        elif type_window == "PAGE":
            ...

    def delete_item(self, type_window, data):
        self.__obs_manager.obj_l.debug_logger(
            f"TemplatesListDialogWindow delete_item(btn):\ntype_window = {type_window}\n data = {data}"
        )
        # todo
        if type_window == "TEMPLATE":
            self.__obs_manager.obj_pd.delete_template(data)
        elif type_window == "PAGE":
            self.__obs_manager.obj_pd.delete_page(data)

    def add_page(self):
        self.__obs_manager.obj_l.debug_logger("TemplatesListDialogWindow add_page()")
        # todo окно
        # вызов окна
        # получение данных
        # сохранение и обновление данных

    def add_template(self):
        self.__obs_manager.obj_l.debug_logger(
            "TemplatesListDialogWindow add_template()"
        )
        # todo окно
        # вызов окна
        result = self.ned_temp_dw("create")
        if result:
            ...
        # получение данных
        # сохранение и обновление данных

    def ned_temp_dw(self, type_ned) -> bool:
        self.__obs_manager.obj_l.debug_logger("TemplatesListDialogWindow ned_temp_dw()")
        self.__obs_manager.obj_ned_temp_dw = (
            nedtemplatedialogwindow.NedTemplateDialogWindow(self.__obs_manager, type_ned)
        )
        result = self.__obs_manager.obj_templdw.exec()
        return result == QDialog.Accepted
