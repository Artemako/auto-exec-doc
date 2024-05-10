from PySide2.QtWidgets import (
    QApplication,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QInputDialog,
)

class TableEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])
        self.add_button = QPushButton("Add Row")
        self.delete_button = QPushButton("Delete Row")
        #self.edit_button = QPushButton("Edit Cell")
        self.to_json_button = QPushButton("to_json_button")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        hbox = QHBoxLayout()
        hbox.addWidget(self.add_button)
        hbox.addWidget(self.delete_button)
        #hbox.addWidget(self.edit_button)
        hbox.addWidget(self.to_json_button)
        self.layout.addLayout(hbox)
        self.setLayout(self.layout)
        self.add_button.clicked.connect(self.add_row)
        self.delete_button.clicked.connect(self.delete_row)
        #self.edit_button.clicked.connect(self.edit_cell)
        self.table.cellChanged.connect(self.update_cell)
        self.to_json_button.clicked.connect(self.to_json)

    def add_row(self):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        for column in range(self.table.columnCount()):
            item = QTableWidgetItem()
            self.table.setItem(row_count, column, item)

    def delete_row(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)

    # def edit_cell(self):
    #     current_row = self.table.currentRow()
    #     current_column = self.table.currentColumn()
    #     if current_row >= 0 and current_column >= 0:
    #         item = self.table.item(current_row, current_column)
    #         if item:
    #             text, ok = QInputDialog.getText(
    #                 self, "Edit Cell", "Enter new value:", QLineEdit.Normal, item.text()
    #             )
    #             if ok and text != "":
    #                 item.setText(text)

    def update_cell(self, row, column):
        item = self.table.item(row, column)
        if item:
            print(f"Cell ({row}, {column}) changed to {item.text()}")

    def to_json(self):
        data = []
        for row in range(self.table.rowCount()):
            row_data = []
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            data.append(row_data)
        print(f"data = {data}")

    

if __name__ == "__main__":
    app = QApplication([])
    table_editor = TableEditor()
    table_editor.show()
    app.exec()
