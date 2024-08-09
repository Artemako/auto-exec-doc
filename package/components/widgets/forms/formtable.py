import json

from PySide6.QtWidgets import QWidget, QTableWidgetItem, QApplication, QMenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QAction

import package.ui.formtable_ui as formtable_ui


class FormTable(QWidget):
    def __init__(self, obs_manager, pair, config_tag, config_table):
        self.__obs_manager = obs_manager
        self.__pair = pair
        self.__config_tag = config_tag
        self.__config_table = config_table
        self.__obs_manager.obj_l.debug_logger(f"FormTable(pair, config_tag, config_table):\npair = {pair},\nconfig_tag = {config_tag},\nconfig_table = {config_table}")
        super(FormTable, self).__init__()
        self.ui = formtable_ui.Ui_FormTableWidget()
        self.ui.setupUi(self)
        self.config()
        self.connect_actions()

    def config(self):
        # заголовок
        self.ui.title.setText(self.__config_tag["title_tag"])
        # описание
        description_tag = self.__config_tag["description_tag"]
        if description_tag:
            self.ui.textbrowser.setHtml(description_tag)
        else:
            self.ui.textbrowser.hide()

        # ОСОБЕННОСТИ из self.config_table
        labels = []
        # content = []
        for config in self.config_table:
            type_config = config.get("type_config")
            value_config = config.get("value_config")
            # TODO
            if type_config == "HEADER":
                labels.append(value_config)
            # elif type_config == "ATTRIBUTE":
            #     content.append(value_config)
        # создать столбцы таблицы
        self.ui.table.setColumnCount(len(labels))
        self.ui.table.setHorizontalHeaderLabels(labels)
        # поставить значения из таблицы
        self.create_table_from_value(self.pair.get("value"))
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

    def connect_actions(self):
        self.__obs_manager.obj_l.debug_logger("FormTable connect_actions()")
        self.ui.add_button.clicked.connect(self.add_row)
        self.ui.delete_button.clicked.connect(self.delete_row)
        self.ui.table.cellChanged.connect(
            lambda: self.set_new_value_in_pair(self.__pair, self.get_data_from_table())
        )

    def show_context_menu(self, position):
        # Show the context menu at the mouse position
        self.__obs_manager.obj_l.debug_logger(f"FormTable show_context_menu(position):\nposition = {position}")
        self.context_menu.exec_(self.ui.table.mapToGlobal(position))

    def add_row(self):
        self.__obs_manager.obj_l.debug_logger("FormTable add_row()")
        row_count = self.ui.table.rowCount()
        self.ui.table.insertRow(row_count)
        for column in range(self.ui.table.columnCount()):
            item = QTableWidgetItem()
            self.ui.table.setItem(row_count, column, item)
        self.set_new_value_in_pair(self.__pair, self.get_data_from_table())
        

    def delete_row(self):
        self.__obs_manager.obj_l.debug_logger("FormTable delete_row()")
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
        self.__obs_manager.obj_l.debug_logger("FormTable copy_values_to_clipboard()")
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
        self.__obs_manager.obj_l.debug_logger("FormTable paste_values_from_clipboard()")
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        rows = text.split("\n")
        selected_items = self.ui.table.selectedItems()
        start_row = selected_items[0].row() if selected_items else 0
        start_col = selected_items[0].column() if selected_items else 0
        #print(f"rows = {rows}")
        for i, row in enumerate(rows):
            columns = row.split("\t")
            #print(f"columns = {columns}")
            if start_row + i < self.ui.table.rowCount():
                for j, value in enumerate(columns):
                    if start_col + j < self.ui.table.columnCount():
                        item = self.ui.table.item(start_row + i, start_col + j)
                        if item:
                            item.setText(value)


    def create_table_from_value(self, json_data):
        self.__obs_manager.obj_l.debug_logger(
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
        self.__obs_manager.obj_l.debug_logger("FormTable to_json(self) -> list:")
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

    def set_new_value_in_pair(self, pair, new_value):
        self.__obs_manager.obj_l.debug_logger(
            f"FormTable set_new_value_in_pair(pair, new_value):\npair = {pair},\nnew_value = {new_value}"
        )
        pair["value"] = new_value
        print(pair)
