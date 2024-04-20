from PySide6.QtWidgets import QWidget, QTableWidgetItem

import package.modules.log as log

import package.ui.formtable_ui as formtable_ui


class FormTable(QWidget):
    def __init__(self, section_index, config_content, config_table, value):
        log.Log.debug_logger(
            f"FormTable(self, section_index, config_content, config_table, value): section_index = {section_index}, config_content = {config_content}, config_table = {config_table}, value = {value}"
        )

        super(FormTable, self).__init__()
        self.ui = formtable_ui.Ui_FormTableWidget()
        self.ui.setupUi(self)
        # TABLE EDITOR
        self.config_tableeditor()

        self.section_index = section_index
        # заголовок
        self.ui.title.setText(config_content["title_content"])

        # описание
        description_content = config_content["description_content"]
        if description_content:
            self.ui.textbrowser.setHtml(description_content)
        else:
            self.ui.textbrowser.hide()

    def config_tableeditor(self):
        self.ui.table.setColumnCount(3)
        self.ui.table.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])
        # connect
        self.ui.add_button.clicked.connect(self.add_row)
        self.ui.delete_button.clicked.connect(self.delete_row)
        self.ui.table.cellChanged.connect(self.update_cell)


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

    def update_cell(self, row, column):
        item = self.ui.table.item(row, column)
        if item:
            print(f"Cell ({row}, {column}) changed to {item.text()}")