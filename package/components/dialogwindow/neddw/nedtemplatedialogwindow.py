from PySide6.QtWidgets import QDialog

import package.ui.nedtemplatedialogwindow_ui as nedtemplatedialogwindow_ui

# TODO ПОДУМАТЬ ПРО PDF 

class NedTemplateDialogWindow(QDialog):
    def __init__(self, osbm, type_ned, templates, template=None):
        self.__osbm = osbm
        self.__type_ned = type_ned
        self.__templates = templates
        self.__template = template
        self.__osbm.obj_logg.debug_logger(
            f"NedTemplateDialogWindow __init__(osbm, type_ned):\ntype_ned = {type_ned},\ntemplates = {templates}\ntemplate = {template}"
        )
        super(NedTemplateDialogWindow, self).__init__()
        self.ui = nedtemplatedialogwindow_ui.Ui_NedTemplateDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        self.__osbm.obj_comwith.resizeqt.set_temp_max_height(self)
        #
        self.__data = dict()
        # одноразовые действия
        self.config_by_type_window()
        self.connecting_actions()

    def get_data(self):
        self.__osbm.obj_logg.debug_logger(
            f"NedTemplateDialogWindow get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def config_by_type_window(self):
        self.__osbm.obj_logg.debug_logger(
            "NedTemplateDialogWindow config_by_type_window()"
        )
        if self.__type_ned == "create":
            self.ui.label_nametemplate.setText("Название нового шаблона")
            self.ui.btn_nestag.setText("Добавить шаблон")
            # предложение включено
            self.ui.label_copyfrom.setEnabled(True)
            self.ui.combox_templates.setEnabled(True)
            # заполнить комбобокс
            self.config_combox_templates()
        elif self.__type_ned == "edit":
            self.ui.label_nametemplate.setText("Название шаблона")
            self.ui.lineedit_nametemplate.setText(self.__template.get("name_template"))
            self.ui.btn_nestag.setText("Сохранить шаблон")
            # предложение отключено
            self.ui.label_copyfrom.setEnabled(False)
            self.ui.combox_templates.setEnabled(False)
    
    def config_combox_templates(self):
        self.__osbm.obj_logg.debug_logger(
            "NedTemplateDialogWindow config_combox_templates()"
        )
        combobox = self.ui.combox_templates
        combobox.blockSignals(True)
        combobox.clear()
        combobox.addItem("- Пустой шаблон -", "empty")
        for elem in self.__templates:
            combobox.addItem(elem.get("name_template"), elem)
        combobox.blockSignals(False)


    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger(
            "NedTemplateDialogWindow connecting_actions()"
        )
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")
        self.ui.btn_nestag.clicked.connect(self.btn_nestag_clicked)
        self.ui.btn_nestag.setShortcut("Ctrl+S")

    def btn_nestag_clicked(self):
        self.__osbm.obj_logg.debug_logger(
            "NedTemplateDialogWindow btn_nestag_clicked()"
        )
        nametemplate = self.ui.lineedit_nametemplate.text()
        self.__data["name_template"] = nametemplate
        # для create
        if self.__type_ned == "create":
            copytemplate = self.ui.combox_templates.currentData()
            if copytemplate:
                self.__data["copy_template"] = copytemplate
        # проверка ОБЩАЯ
        if len(nametemplate) > 0:
            self.accept()
        else:
            self.__osbm.obj_dw.warning_message("Заполните поле названия")