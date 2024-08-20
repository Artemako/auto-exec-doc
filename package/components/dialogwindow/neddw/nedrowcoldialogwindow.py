import re

from PySide6.QtWidgets import QDialog

import package.ui.nedrowcoldialogwindow_ui as nedrowcoldialogwindow_ui

class NedRowcolDialogWindow(QDialog):
    def __init__(self, osbm, type_ned, type_rowcol, rowcols, rowcol=None):
        self.__osbm = osbm
        self.__type_ned = type_ned
        self.__type_rowcol = type_rowcol
        self.__rowcols = rowcols
        self.__rowcol = rowcol
        self.__osbm.obj_logg.debug_logger(
            f"NedRowcolDialogWindow __init__(osbm, type_ned, rowcols, rowcol): \n self.__type_ned = {self.__type_ned} \n self.__rowcols = {self.__rowcols} \n self.__rowcol = {self.__rowcol}"
        )
        super(NedRowcolDialogWindow, self).__init__()
        self.ui = nedrowcoldialogwindow_ui.Ui_NedRowcolDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__data = {"ID": None, "ATTR": None, "TITLE": None}
        # одноразовые действия
        self.config_by_type_window()
        self.config_combox_neighboor()
        self.connecting_actions()

    def get_data(self):
        self.__osbm.obj_logg.debug_logger(
            f"NedRowcolDialogWindow get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def config_by_type_window(self):
        self.__osbm.obj_logg.debug_logger(
            "NedRowcolDialogWindow config_by_type_window()"
        )
        if self.__type_ned == "create":
            if self.__type_rowcol == "row":
                self.ui.label_rowcol.setText("Название новой строки")
                self.ui.btn_nestag.setText("Добавить строку")
            elif self.__type_rowcol == "col":
                self.ui.label_nametemplate.setText("Название нового столбца")
                self.ui.btn_nestag.setText("Добавить столбец")
        elif self.__type_ned == "edit":
            if self.__type_rowcol == "row":
                self.ui.label_rowcol.setText("Название строки")
                self.ui.btn_nestag.setText("Изменить строку")
            elif self.__type_rowcol == "col":
                self.ui.label_nametemplate.setText("Название столбца")
                self.ui.btn_nestag.setText("Изменить столбец")
            #
            self.ui.lineedit_attr.setText(self.__rowcol.get("ATTR"))
            self.ui.lineedit_rowcoltitle.setText(self.__rowcol.get("TITLE"))

    def get_order_rowcol(self, current_rowcol):
        result = -1
        for index, rowcol in self.__rowcols:
            if rowcol.get("ID") == current_rowcol.get("ID"):
                result = index
                break
        self.__osbm.obj_logg.debug_logger(
            f"NedRowcolDialogWindow get_order_rowcol():\n current_rowcol = {current_rowcol} \n result = {result}"
        )
        return result

    def config_combox_neighboor(self):
        self.__osbm.obj_logg.debug_logger(
            "NedRowcolDialogWindow config_combox_templates()"
        )
        combobox = self.ui.combox_neighboor
        combobox.blockSignals(True)
        combobox.clear()
        if self.__rowcol and self.get_order_rowcol(self.__rowcol) == 0:
            pass
        else:
            combobox.addItem("- В начало -", "START")
        for rowcol in self.__rowcols:
            if rowcol.get("ID") == self.__rowcol.get("ID"):
                continue
            combobox.addItem(rowcol.get("NAME"), rowcol)
        combobox.blockSignals(False)

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("NedRowcolDialogWindow connecting_actions()")
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")
        self.ui.btn_nestag.clicked.connect(self.btn_nestag_clicked)
        self.ui.btn_nestag.setShortcut("Ctrl+S")

    def get_is_valid_jinja_attr(self, name_attr):
        pattern = r"^[\w-]+$"  # эквивалентно [a-zA-Z0-9_-]
        result = bool(re.match(pattern, name_attr))
        self.__osbm.obj_logg.debug_logger(
            f"NedRowcolDialogWindow get_is_valid_jinja_attr(name_tag):\n name_attr = {name_attr} \n result = {result}"
        )
        return result

    def btn_nestag_clicked(self):
        self.__osbm.obj_logg.debug_logger("NedRowcolDialogWindow btn_nestag_clicked()")
        le_attr = self.ui.lineedit_attr.text()
        le_rowcoltitle = self.ui.lineedit_rowcoltitle.text()
        # проверка на пустоту (уникальность присутствует)
        is_valid_jinja_attr = self.get_is_valid_jinja_attr(le_attr)
        if len(le_attr) > 0 and len(le_rowcoltitle) > 0 and is_valid_jinja_attr:
            # заполняем словарь
            order = self.ui.combox_neighboor.currentData()
            order = order + 1 if order != "START" else 0
            self.__data = {
                "ATTR": le_attr,
                "TITLE": le_rowcoltitle,
                "_ORDER": order
            }
            # пытаемся accept()
            if self.__type_window == "create":
                self.add_new_rowcol()
            elif self.__type_window == "edit":
                self.save_edit_rowcol()
        elif le_attr == "" and le_rowcoltitle == "" and is_valid_jinja_attr:
            self.__osbm.obj_dw.warning_message("Заполните все поля")
        elif le_attr == "":
            self.__osbm.obj_dw.warning_message("Заполните поле атрибута")
        elif le_rowcoltitle == "":
            self.__osbm.obj_dw.warning_message("Заполните поле названия атрибута")
        elif not is_valid_jinja_attr:
            self.__osbm.obj_dw.warning_message(
                "Атрибут тэга содержит недопустимые символы."
            )

    def get_rowcol_by_name(self, name_attr):
        for rowcol in self.__rowcols:
            if rowcol.get("ATTR") == name_attr:
                return rowcol
        return None

    def add_new_rowcol(self):
        self.__osbm.obj_logg.debug_logger("NedRowcolDialogWindow add_new_rowcol()")
        le_attr = self.ui.lineedit_attr.text()
        # Проверка на уникальность
        name_attr = self.get_tag_by_name(le_attr)
        if name_attr:
            self.__osbm.obj_dw.warning_message("Такой атрибут уже существует.")
        else:
            self.accept()

    def save_edit_rowcol(self):
        self.__osbm.obj_logg.debug_logger("NedRowcolDialogWindow save_edit_rowcol()")
        # Проверка на уникальность
        le_attr = self.ui.lineedit_attr.text()
        old_le_attr = self.__rowcol.get("ATTR")
        name_attr = self.get_tag_by_name(le_attr)
        if le_attr == old_le_attr:
            # ↑ если имя тега не изменилось
            self.accept()
        elif name_attr:
            self.__osbm.obj_dw.warning_message("Такой атрибут уже существует.")
        else:
            self.accept()
