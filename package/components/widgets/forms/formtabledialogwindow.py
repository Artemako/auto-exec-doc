import json

from PySide6.QtWidgets import (
    QDialog,
    QTableWidget,
    QMenu,
    QApplication,
    QTableWidgetItem,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

import package.ui.formtabledialogwindow_ui as formtabledialogwindow_ui

# TODO ФОРМА ТАБЛИЦЫ


class FormTableDialogWindow(QDialog):
    def __init__(self, osbm, current_variable, config_dict, value_pair):
        self.__osbm = osbm
        self.__current_variable = current_variable
        self.__config_dict = config_dict
        self.__value_pair = value_pair
        self.__osbm.obj_logg.debug_logger(
            f"FormTableDialogWindow __init__(osbm, current_variable, config_dict, value_pair): \n current_variable = {current_variable}, \n config_dict = {config_dict}, \n value_pair = {value_pair}"
        )
        super(FormTableDialogWindow, self).__init__()
        self.ui = formtabledialogwindow_ui.Ui_FormTableDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__typetable = None
        self.__rowc
        #
        self.config()
        self.config_tw()
        self.config_context_menu()
        #
        # self.connecting_actions()


    # current_variable = (
        #     {
        #         "id_variable": 7,
        #         "name_variable": "таблица",
        #         "type_variable": "TABLE",
        #         "title_variable": "Таблица",
        #         "order_variable": 6,
        #         "config_variable": '{"TYPETABLE": "ROW", "ROWCOLS": [{"ID": "7c90b765640811ef90f1dce9947e4a05", "ATTR": "\\u043c\\u0430\\u0448\\u0438\\u043d\\u0430", "TITLE": "\\u041c\\u0430\\u0448\\u0438\\u043d\\u0430", "ORDER": 0}, {"ID": "850e17de640811ef88cbdce9947e4a05", "ATTR": "\\u0441\\u043a\\u043e\\u0440\\u043e\\u0441\\u0442\\u044c", "TITLE": "\\u0421\\u043a\\u043e\\u0440\\u043e\\u0441\\u0442\\u044c", "ORDER": 1}, {"ID": "8c4b4f4a640811efb62ddce9947e4a05", "ATTR": "\\u043a\\u0438\\u043b\\u043e\\u043c\\u0435\\u0442\\u0440\\u0430\\u0436", "TITLE": "\\u043a\\u0438\\u043b\\u043e\\u043c\\u0435\\u0442\\u0440\\u0430\\u0436", "ORDER": 2}]}',
        #         "description_variable": "",
        #         "is_global": None,
        #     },
        # )
        # config_dict = (
        #     {
        #         "TYPETABLE": "ROW",
        #         "ROWCOLS": [
        #             {
        #                 "ID": "7c90b765640811ef90f1dce9947e4a05",
        #                 "ATTR": "машина",
        #                 "TITLE": "Машина",
        #                 "ORDER": 0,
        #             },
        #             {
        #                 "ID": "850e17de640811ef88cbdce9947e4a05",
        #                 "ATTR": "скорость",
        #                 "TITLE": "Скорость",
        #                 "ORDER": 1,
        #             },
        #             {
        #                 "ID": "8c4b4f4a640811efb62ddce9947e4a05",
        #                 "ATTR": "километраж",
        #                 "TITLE": "километраж",
        #                 "ORDER": 2,
        #             },
        #         ],
        #     },
        # )
        # value_pair = None

    def config(self):
        self.__osbm.obj_logg.debug_logger("FormTable config()")
        #
        self.ui.label_nametable.setText(self.__current_variable.get("name_variable", "Таблица"))

    def config_tw(self):
        # ОСОБЕННОСТИ из self.config_dict
        
        

        # создать столбцы таблицы
        self.ui.table.setColumnCount(len(headers))
        self.ui.table.setHorizontalHeaderLabels(headers)
        # поставить значения из таблицы
        self.create_table_from_value(self.pair.get("value_pair"))

    def config_context_menu(self):
        self.__osbm.obj_logg.debug_logger("FormTable config_context_menu()")
        # контекстное меню
        self.context_menu = QMenu(self)
        # Копировать - copy_values_to_clipboard
        self.copy_action = QAction("Копировать", self)
        self.copy_action.triggered.connect(lambda: self.copy_values_to_clipboard())
        self.context_menu.addAction(self.copy_action)
        # Вставить - paste_values_from_clipboard
        self.paste_action = QAction("Вставить", self)
        self.paste_action.triggered.connect(lambda: self.paste_values_from_clipboard())
        self.context_menu.addAction(self.paste_action)
        # контекстное меню по правой кнопкой мыши по таблице.
        self.ui.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.table.customContextMenuRequested.connect(self.show_context_menu)

    # TODO ниже
    def connect_actions(self):
        self.__osbm.obj_logg.debug_logger("FormTable connect_actions()")
        self.ui.add_button.clicked.connect(self.add_row)
        self.ui.delete_button.clicked.connect(self.delete_row)
        self.ui.table.cellChanged.connect(
            lambda: self.set_new_value_in_pair(self.__pair, self.get_data_from_table())
        )

    def show_context_menu(self, position):
        # Show the context menu at the mouse position
        self.__osbm.obj_logg.debug_logger(
            f"FormTable show_context_menu(position):\nposition = {position}"
        )
        self.context_menu.exec_(self.ui.table.mapToGlobal(position))

    def add_row(self):
        self.__osbm.obj_logg.debug_logger("FormTable add_row()")
        row_count = self.ui.table.rowCount()
        self.ui.table.insertRow(row_count)
        for column in range(self.ui.table.columnCount()):
            item = QTableWidgetItem()
            self.ui.table.setItem(row_count, column, item)
        self.set_new_value_in_pair(self.__pair, self.get_data_from_table())

    def delete_row(self):
        self.__osbm.obj_logg.debug_logger("FormTable delete_row()")
        current_row = self.ui.table.currentRow()
        if current_row >= 0:
            self.ui.table.removeRow(current_row)
        self.set_new_value_in_pair(self.__pair, self.get_data_from_table())

    # def update_cell(self, row, column):
    #     item = self.ui.table.item(row, column)
    #     if item:
    #         print(f"Cell ({row}, {column}) changed to {item.text()}")

    def copy_values_to_clipboard(self):
        """
        Копирование значения в буфер обмена
        """
        self.__osbm.obj_logg.debug_logger("FormTable copy_values_to_clipboard()")
        selected_items = self.ui.table.selectedItems()
        # values = []
        # for item in selected_items:
        #     values.append('\t'.join(item.text()))
        # text = '\n'.join(values)
        text = str()
        selected_items = self.ui.table.selectedItems()
        col = -1
        for item in selected_items:
            new_col = item.column()
            if new_col > col:
                col = new_col
                text += item.text() + "\t"
            else:
                col = new_col
                text += "\n" + item.text() + "\t"
        if text[-1] == "\t":
            text = text[:-1]
        clipboard = QApplication.clipboard()
        clipboard.clear()
        clipboard.setText(text)
        print(f"text = {text}")

    def paste_values_from_clipboard(self):
        """
        Вставка значений из буфера обмена
        """
        self.__osbm.obj_logg.debug_logger("FormTable paste_values_from_clipboard()")
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        rows = text.split("\n")
        selected_items = self.ui.table.selectedItems()
        start_row = selected_items[0].row() if selected_items else 0
        start_col = selected_items[0].column() if selected_items else 0
        # print(f"rows = {rows}")
        for i, row in enumerate(rows):
            columns = row.split("\t")
            # print(f"columns = {columns}")
            if start_row + i < self.ui.table.rowCount():
                for j, value in enumerate(columns):
                    if start_col + j < self.ui.table.columnCount():
                        item = self.ui.table.item(start_row + i, start_col + j)
                        if item:
                            item.setText(value)

    def create_table_from_value(self, json_data):
        self.__osbm.obj_logg.debug_logger(
            f"FormTable create_table_from_value(self, json_data):\ndata = {json_data}"
        )
        if json_data:
            data = json.loads(json_data)
            self.ui.table.setRowCount(len(data))
            self.ui.table.setColumnCount(len(data[0]))
            for row, row_data in enumerate(data):
                for column, value in enumerate(row_data):
                    item = QTableWidgetItem(value)
                    self.ui.table.setItem(row, column, item)

    def get_data_from_table(self) -> list:
        self.__osbm.obj_logg.debug_logger("FormTable to_json(self) -> list:")
        table_data = []
        for row in range(self.ui.table.rowCount()):
            print("row = ", row)
            row_data = []
            for column in range(self.ui.table.columnCount()):
                print("column = ", column)
                item = self.ui.table.item(row, column)
                if item:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            table_data.append(row_data)
        print(f"table_data = {table_data}")
        return json.dumps(table_data)
