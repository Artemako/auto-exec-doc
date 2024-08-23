from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QTimer, Qt

import re

import package.ui.nedvariabledialogwindow_ui as nedvariabledialogwindow_ui

import package.components.widgets.nedvariables.neddatevariable as neddatevariable
import package.components.widgets.nedvariables.nedtablevariable as nedtablevariable
import package.components.widgets.nedvariables.nedimagevariable as nedimagevariable

class NedVariableDialogWindow(QDialog):
    def __init__(self, osbm, type_window, variables, variable=None, name_variable = None):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger(
            f"NedVariableDialogWindow(osbm, type_window):\ntype_window = {type_window}\nvariable = {variable}"
        )
        self.__type_window = type_window
        self.__variables = variables
        self.__variable = variable
        self.__name_variable = name_variable
        super(NedVariableDialogWindow, self).__init__()
        self.ui = nedvariabledialogwindow_ui.Ui_NedVariableDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        # одноразовые действия
        self.__additional_widget = None
        self.__data = {
            "NAME": None,
            "TYPE": None,
            "TITLE": None,
            "ORDER": None,
            "CONFIG": {},
            "DESCRIPTION": {},
        }
        #
        self.config_combox_typevariable()
        self.config_combox_neighboor()
        self.config_by_type_window()
        # многоразовые действия
        self.update_additional_info()
        # подключаем действия
        self.connecting_actions()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Игнорируем нажатие Enter
            event.ignore()
        else:
            super().keyPressEvent(event)

    def get_data(self):
        self.__osbm.obj_logg.debug_logger(
            f"NedVariableDialogWindow get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def config_combox_neighboor(self):
        self.__osbm.obj_logg.debug_logger(
            "NedVariableDialogWindow config_combox_neighboor()"
        )
        combobox = self.ui.combox_neighboor
        combobox.blockSignals(True)
        combobox.clear()
        # по умолчанию - в конец
        current_index = 0
        flag = True
        combobox.addItem("- В начало -", "START")
        for index, variable in enumerate(self.__variables):
            if self.__variable and self.__variable.get("id_variable") == variable.get("id_variable"):
                flag = False
            else:
                combobox.addItem(f'{variable.get("order_variable")+1}) {variable.get("name_variable")}', variable)
            if flag:
                current_index = index + 1
        combobox.setCurrentIndex(current_index)
        combobox.blockSignals(False)


    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("NedVariableDialogWindow connecting_actions()")
        self.ui.combox_typevariable.currentIndexChanged.connect(
            self.on_combox_typevariable_changed
        )
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")
        self.ui.btn_nesvariable.clicked.connect(self.btn_nesvariable_clicked)
        self.ui.btn_nesvariable.setShortcut("Ctrl+S")


    def get_is_valid_jinja_variable(self, name_variable):
        pattern = r'[А-яЁёA-z0-9_-]+' 
        result = bool(re.match(pattern, name_variable))
        self.__osbm.obj_logg.debug_logger(
            f"NedVariableDialogWindow get_is_valid_jinja_variable(name_variable):\name_variable = {name_variable}\n result = {result}"
        )
        return result


    def btn_nesvariable_clicked(self):
        self.__osbm.obj_logg.debug_logger("NedVariableDialogWindow btn_nesvariable_clicked()")
        le_namevariable = self.ui.lineedit_namevariable.text()
        le_titlevariable = self.ui.lineedit_titlevariable.text()
        # проверка на пустоту (уникальность присутствует)
        is_valid_jinja_variable = self.get_is_valid_jinja_variable(le_namevariable)
        if len(le_namevariable) > 0 and len(le_titlevariable) > 0 and is_valid_jinja_variable:
            # получит config_data в зависимости от типа переменной
            type_variable = self.ui.combox_typevariable.currentData()
            if type_variable == "TEXT" or type_variable == "LONGTEXT":
                config_data = {}
            else:
                config_data = self.__additional_widget.get_save_data()
            #
            neighboor_data = self.ui.combox_neighboor.currentData()
            print(f"neighboor_data = {neighboor_data}")
            order_variable = int(neighboor_data.get("order_variable")) + 1 if neighboor_data != "START" else 0
            self.__data = {
                "NAME": le_namevariable,
                "TYPE": type_variable,
                "TITLE": le_titlevariable,
                "ORDER": order_variable,
                "CONFIG": config_data,
                "DESCRIPTION": "",
            }
            # пытаемся accept
            if self.__type_window == "create":
                self.add_new_variable()
            elif self.__type_window == "edit":
                self.save_edit_variable()
        elif le_namevariable == "" and le_titlevariable == "" and is_valid_jinja_variable:
            self.__osbm.obj_dw.warning_message("Заполните все поля.")
        elif le_namevariable == "":
            self.__osbm.obj_dw.warning_message("Заполните поле переменной.")
        elif le_titlevariable == "":
            self.__osbm.obj_dw.warning_message("Заполните поле названия переменной.")
        elif not is_valid_jinja_variable:
            self.__osbm.obj_dw.warning_message("Переменная содержит недопустимые символы.")

    def add_new_variable(self):
        self.__osbm.obj_logg.debug_logger("NedVariableDialogWindow add_new_variable()")
        # проверка на уникальность
        le_namevariable = self.ui.lineedit_namevariable.text()
        name_variable = self.__osbm.obj_prodb.get_variable_by_name(le_namevariable)
        if name_variable:
            self.__osbm.obj_dw.warning_message("Переменная с таким именем уже существует.")
        else:
            self.accept()

    def save_edit_variable(self):
        self.__osbm.obj_logg.debug_logger("NedVariableDialogWindow save_edit_variable()")
        # проверка на уникальность
        le_namevariable = self.ui.lineedit_namevariable.text()
        old_name_variable = self.__variable.get("name_variable")
        name_variable = self.__osbm.obj_prodb.get_variable_by_name(le_namevariable)
        if le_namevariable == old_name_variable:
            # ↑ если имя переменной не изменилось
            self.accept()
        elif name_variable:
            self.__osbm.obj_dw.warning_message("Переменная с таким именем уже существует.")
        else:
            self.accept()

    def on_combox_typevariable_changed(self, index):
        self.__osbm.obj_logg.debug_logger(
            f"NedVariableDialogWindow on_combox_typevariable_changed(index):\nindex = {index}"
        )
        self.update_additional_info(index)

    def config_combox_typevariable(self):
        self.__osbm.obj_logg.debug_logger("NedVariableDialogWindow config_combox_typevariable()")
        self.ui.combox_typevariable.blockSignals(True)
        self.ui.combox_typevariable.clear()
        variable_types = self.__osbm.obj_comwith.variable_types.get_variable_types()
        for variable in variable_types:
            self.ui.combox_typevariable.addItem(variable.icon, variable.name, variable.data)
        #
        if self.__variable:
            index = self.__osbm.obj_comwith.variable_types.get_index_by_data(
                self.__variable.get("type_variable")
            )
            self.ui.combox_typevariable.setCurrentIndex(index)
        self.ui.combox_typevariable.blockSignals(False)

    def config_by_type_window(self):
        self.__osbm.obj_logg.debug_logger("NedVariableDialogWindow config_by_type_window()")
        if self.__type_window == "create":
            self.ui.btn_nesvariable.setText("Добавить переменную")
            # для NedPageDialogWindow
            if self.__name_variable:
                self.ui.lineedit_namevariable.setText(self.__name_variable)

        elif self.__type_window == "edit":
            self.ui.btn_nesvariable.setText("Сохранить переменную")
            self.ui.lineedit_namevariable.setText(self.__variable.get("name_variable"))
            self.ui.lineedit_titlevariable.setText(self.__variable.get("title_variable"))



    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())

    def update_additional_info(self, index=None):
        self.__osbm.obj_logg.debug_logger(
            f"NedVariableDialogWindow config_additional_info(index):\nindex = {index}"
        )
        if index is None:
            if self.__variable:
                index = self.__osbm.obj_comwith.variable_types.get_index_by_data(
                    self.__variable.get("type_variable")
                )
            else:
                index = 0
        self.clear_layout(self.ui.vbl_additional_info)
        self.__additional_widget = None
        #
        data = self.__osbm.obj_comwith.variable_types.get_data_by_index(index)
        if data == "DATE":
            self.__additional_widget = neddatevariable.NedDateVariable(
                self.__osbm, self.__type_window, self.__variable
            )
            self.ui.vbl_additional_info.addWidget(self.__additional_widget)
        elif data == "TABLE":
            self.__additional_widget = nedtablevariable.NedTableVariable(
                self.__osbm, self.__type_window, self.__variable
            )
            self.ui.vbl_additional_info.addWidget(self.__additional_widget)
        elif data == "IMAGE":
            self.__additional_widget = nedimagevariable.NedImageVariable(
                self.__osbm, self.__type_window, self.__variable
            )
            self.ui.vbl_additional_info.addWidget(self.__additional_widget)
        #
        QTimer.singleShot(
            0, self, lambda: self.__osbm.obj_comwith.resizeqt.set_temp_max_height(self)
        )
