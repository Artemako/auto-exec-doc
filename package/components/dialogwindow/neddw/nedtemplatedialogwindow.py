from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt

import package.ui.nedtemplatedialogwindow_ui as nedtemplatedialogwindow_ui

class NedTemplateDialogWindow(QDialog):
    def __init__(self, osbm, type_ned, templates, template=None, is_active = False):
        self.__osbm = osbm
        self.__type_ned = type_ned
        self.__templates = templates
        self.__template = template
        self.__is_active = is_active
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
        self.config_is_active()
        self.connecting_actions()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Игнорируем нажатие Enter
            event.ignore()
        else:
            super().keyPressEvent(event)

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
            self.ui.btn_nesvariable.setText("Добавить шаблон")
            # предложение включено
            self.ui.label_copyfrom.setEnabled(True)
            self.ui.combox_templates.setEnabled(True)
            # заполнить комбобокс
            self.config_combox_templates()
        elif self.__type_ned == "edit":
            self.ui.label_nametemplate.setText("Название шаблона")
            self.ui.lineedit_nametemplate.setText(self.__template.get("name_template"))
            self.ui.btn_nesvariable.setText("Сохранить шаблон")
            # предложение отключено
            self.ui.label_copyfrom.setEnabled(False)
            self.ui.combox_templates.setEnabled(False)

    def config_is_active(self):
        self.__osbm.obj_logg.debug_logger(
            "NedTemplateDialogWindow config_is_active()"
        )
        if self.__type_ned == "create":
            if self.__templates:
                self.ui.checkbox_is_active.setChecked(False)
                self.ui.checkbox_is_active.setEnabled(True)
            else:
                # если self.__templates пуст, то автоматически включено
                self.ui.checkbox_is_active.setChecked(True)
                self.ui.checkbox_is_active.setEnabled(False)

        elif self.__type_ned == "edit":
            if self.__is_active:
                self.ui.checkbox_is_active.setChecked(True)
                self.ui.checkbox_is_active.setEnabled(False)
            else:
                self.ui.checkbox_is_active.setChecked(False)
                self.ui.checkbox_is_active.setEnabled(True)

            
            
            # id_template = template.get("id_template")
            
    
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
        self.ui.btn_nesvariable.clicked.connect(self.btn_nesvariable_clicked)
        self.ui.btn_nesvariable.setShortcut("Ctrl+S")

    def btn_nesvariable_clicked(self):
        self.__osbm.obj_logg.debug_logger(
            "NedTemplateDialogWindow btn_nesvariable_clicked()"
        )
        nametemplate = self.ui.lineedit_nametemplate.text()
        self.__data["IS_ACTIVE"] = self.ui.checkbox_is_active.isChecked()
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