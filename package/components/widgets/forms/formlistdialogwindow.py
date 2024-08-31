import json

from PySide6.QtWidgets import QDialog, QListWidget, QListWidgetItem, QAbstractItemView
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

import package.ui.formlistdialogwindow_ui as formlistdialogwindow_ui


class FormListDialogWindow(QDialog):
    def __init__(self, osbm, current_variable, value_pair):
        self.__osbm = osbm
        self.__current_variable = current_variable
        self.__value_pair = value_pair
        self.__osbm.obj_logg.debug_logger(
            f"FormListDialogWindow __init__(osbm, current_variable, value_pair): \n current_variable = {current_variable}, \n value_pair = {value_pair}"
        )
        super(FormListDialogWindow, self).__init__()
        self.ui = formlistdialogwindow_ui.Ui_FormListDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__data = []
        #
        self.config_and_lw()
        #
        self.connecting_actions()

    def get_data(self):
        self.__osbm.obj_logg.debug_logger(
            f"FormTableDialogWindow get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def config_and_lw(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow config_and_lw()")
        #
        self.ui.label_nametable.setText(
            self.__current_variable.get("name_variable", "Список")
        )
        #
        self.ui.lw.blockSignals(True)
        self.ui.lw.clear()
        #
        list_data = self.get_list_data_from_value_pair()
        for data in list_data:
            self.ui.lw.addItem(data)
        if list_data:
            self.ui.lw.setCurrentRow(0)
        #
        self.ui.lw.blockSignals(False)
        #
        self.edit_all_items()
        


    def edit_all_items(self):
        self.__osbm.obj_logg.debug_logger("FormListDialogWindow edit_all_items()")
        for index in range(self.ui.lw.count()):
            item = self.ui.lw.item(index)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
        #

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("FormListDialogWindow connecting_actions()")
        #
        self.ui.add_button.clicked.connect(self.add_item)
        self.ui.delete_button.clicked.connect(self.delete_item)
        self.ui.btn_up.clicked.connect(self.move_item_up)
        self.ui.btn_down.clicked.connect(self.move_item_down)
        #
        self.ui.btn_save.clicked.connect(self.save)
        self.ui.btn_save.setShortcut("Ctrl+S")
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")

    def add_item(self):
        self.__osbm.obj_logg.debug_logger("FormListDialogWindow add_item()")
        item_text = f"Элемент {self.ui.lw.count() + 1}"  # Предустановленный текст
        new_item = QListWidgetItem(item_text)
        current_row = self.ui.lw.currentRow()
        if current_row != -1:  # Если элемент выделен
            self.ui.lw.insertItem(
                current_row + 1, new_item
            )  # Вставляем после выделенного элемента
        else:
            self.ui.lw.addItem(new_item)  # В противном случае добавляем в конец
        #
        self.edit_all_items()

    def delete_item(self):
        self.__osbm.obj_logg.debug_logger("FormListDialogWindow delete_item()")
        current_item = self.ui.lw.currentItem()
        if current_item:
            self.ui.lw.takeItem(self.ui.lw.row(current_item))

    def move_item_up(self):
        self.__osbm.obj_logg.debug_logger("FormListDialogWindow move_item_up()")
        current_row = self.ui.lw.currentRow()
        if current_row > 0:
            item = self.ui.lw.takeItem(current_row)
            self.ui.lw.insertItem(current_row - 1, item)
            self.ui.lw.setCurrentRow(current_row - 1)

    def move_item_down(self):
        self.__osbm.obj_logg.debug_logger("FormListDialogWindow move_item_down()")
        current_row = self.ui.lw.currentRow()
        if current_row < self.ui.lw.count() - 1:
            item = self.ui.lw.takeItem(current_row)
            self.ui.lw.insertItem(current_row + 1, item)
            self.ui.lw.setCurrentRow(current_row + 1)

    def get_list_data_from_value_pair(self):
        self.__osbm.obj_logg.debug_logger(
            "FormListDialogWindow get_list_data_from_value_pair()"
        )
        json_data = self.__value_pair
        if json_data:
            data = json.loads(json_data)
        else:
            data = []
        return data

    def get_data_from_list(self):
        self.__osbm.obj_logg.debug_logger("FormListDialogWindow get_data_from_list()")
        data = []
        for i in range(self.ui.lw.count()):
            data.append(self.ui.lw.item(i).text())
        return json.dumps(data)

    def save(self):
        self.__osbm.obj_logg.debug_logger("FormListDialogWindow save()")
        self.__data = self.get_data_from_list()
        self.accept()
