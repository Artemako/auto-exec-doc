import json

from PySide6.QtWidgets import QWidget, QTableWidgetItem, QApplication, QMenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QAction

import package.modules.log as log

import package.ui.formtable_ui as formtable_ui



class FormTable(QWidget):
    def __init__(self, pair, config_content, config_table):
        super(FormTable, self).__init__()
        self.ui = formtable_ui.Ui_FormTableWidget()
        self.ui.setupUi(self)

        # заголовок
        self.ui.title.setText(config_content["title_content"])

        # описание
        description_content = config_content["description_content"]
        if description_content:
            self.ui.textbrowser.setHtml(description_content)
        else:
            self.ui.textbrowser.hide()

        # ОСОБЕННОСТИ из self.config_table
        labels = []
        # content = []
        for config in config_table:
            type_config = config.get("type_config")
            value_config = config.get("value_config")
            if type_config == "HEADER":
                labels.append(value_config)
            # elif type_config == "CONTENT":
            #     content.append(value_config)
        # создать столбцы таблицы
        self.ui.table.setColumnCount(len(labels))
        self.ui.table.setHorizontalHeaderLabels(labels)
        # поставить значения из таблицы
        self.create_table_from_value(pair.get("value"))
        # вставка из буфера обмена
        self.context_menu = QMenu(self)
        self.paste_action = QAction("Paste", self)
        self.paste_action.triggered.connect(self.paste_values_from_clipboard)
        self.context_menu.addAction(self.paste_action)
        # Connect the context menu to the table's right-click event
        self.ui.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.table.customContextMenuRequested.connect(self.show_context_menu)
        # connect
        self.ui.add_button.clicked.connect(self.add_row)
        self.ui.delete_button.clicked.connect(self.delete_row)
        self.ui.table.cellChanged.connect(
            lambda: self.set_new_value_in_pair(pair, self.get_data_from_table())
        )

    def show_context_menu(self, position):
        # Show the context menu at the mouse position
        self.context_menu.exec_(self.ui.table.mapToGlobal(position))

    def add_row(self):
        row_count = self.ui.table.rowCount()
        self.ui.table.insertRow(row_count)
        for column in range(self.ui.table.columnCount()):
            item = QTableWidgetItem()
            self.ui.table.setItem(row_count, column, item)

    def delete_row(self):
        current_row = self.ui.table.currentRow()
        if current_row >= 0:
            self.ui.table.removeRow(current_row)

    # def update_cell(self, row, column):
    #     item = self.ui.table.item(row, column)
    #     if item:
    #         print(f"Cell ({row}, {column}) changed to {item.text()}")

        

    def paste_values_from_clipboard(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        rows = text.split('\n')
        selected_rows = self.ui.table.selectedItems()
        start_row = selected_rows[0].row() if selected_rows else 0
        start_col = selected_rows[0].column() if selected_rows else 0
        for i, row in enumerate(rows):
            if start_row + i >= self.ui.table.rowCount():
                break
            columns = row.split('\t')
            for j, value in enumerate(columns):
                if start_col + j >= self.ui.table.columnCount():
                    break
                item = self.ui.table.item(start_row + i, start_col + j)
                if item is None:
                    item = QTableWidgetItem(value)
                    self.table_widget.setItem(start_row + i, start_col + j, item)
                else:
                    item.setText(value)

        # Clearing the selection after pasting
        self.ui.table.clearSelection()


    def create_table_from_value(self, json_data):
        log.Log.debug_logger(f"create_table_from_value(self, json_data): data = {json_data}")
        if json_data:
            data = json.loads(json_data)
            self.ui.table.setRowCount(len(data))
            self.ui.table.setColumnCount(len(data[0]))
            for row, row_data in enumerate(data):
                for column, value in enumerate(row_data):
                    item = QTableWidgetItem(value)
                    self.ui.table.setItem(row, column, item)

    def get_data_from_table(self) -> list:
        log.Log.debug_logger("IN to_json(self) -> list:")
        data = []
        for row in range(self.ui.table.rowCount()):
            row_data = []
            for column in range(self.ui.table.columnCount()):
                item = self.ui.table.item(row, column)
                if item:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            data.append(row_data)
        return json.dumps(data)

    def set_new_value_in_pair(self, pair, new_value):
        log.Log.debug_logger(
            f"set_new_value_in_pair(self, pair, new_value): pair = {pair}, new_value = {new_value}"
        )
        pair["value"] = new_value
        print(pair)


    # TODO sqlite3.ProgrammingError: Error binding parameter 1: type 'list' is not supported