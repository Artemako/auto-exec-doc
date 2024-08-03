from PySide6.QtWidgets import QDialog, QListWidgetItem


import package.ui.templateslistsialogwindow_ui as templateslistsialogwindow_ui

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
                custom_widget = customitemqlistwidget.CustomItemQListWidget(self.__obs_manager, "TEMPLATE", template)
                item = QListWidgetItem()
                item.setData(0, template)
                # Указываем размер элемента
                item.setSizeHint(custom_widget.sizeHint())  
                list_widget.addItem(item)
                # Устанавливаем виджет для элемента
                list_widget.setItemWidget(item, custom_widget)
                # TODO Кнопки эдита и удаления
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
                custom_widget = customitemqlistwidget.CustomItemQListWidget(self.__obs_manager, "PAGE", page)
                item = QListWidgetItem()
                item.setData(0, page)
                # Указываем размер элемента
                item.setSizeHint(custom_widget.sizeHint())  
                list_widget.addItem(item)
                # Устанавливаем виджет для элемента
                list_widget.setItemWidget(item, custom_widget) 
            list_widget.setCurrentRow(0) 
            list_widget.blockSignals(False)


    def connecting_actions(self):
        self.ui.combox_forms.currentIndexChanged.connect(self.combox_forms_index_changed)
        self.ui.lw_templates.currentItemChanged.connect(self.config_pages())
        # self.ui.lw_pages.currentItemChanged.connect()

    def combox_forms_index_changed(self):
        self.__obs_manager.obj_l.debug_logger("TemplatesListDialogWindow combox_forms_index_changed()")
        self.config_templates()
        self.config_pages()
        
    
        