import sys
from PySide6.QtWidgets import QApplication, QListWidget, QListWidgetItem, QVBoxLayout, QPushButton, QWidget
from PySide6.QtCore import Qt

class EditableListWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editable List Widget")
        self.layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        self.add_button = QPushButton("Add Item")
        self.add_button.clicked.connect(self.add_item)
        self.layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Delete Item")
        self.delete_button.clicked.connect(self.delete_item)
        self.layout.addWidget(self.delete_button)

        self.move_up_button = QPushButton("Move Up")
        self.move_up_button.clicked.connect(self.move_item_up)
        self.layout.addWidget(self.move_up_button)

        self.move_down_button = QPushButton("Move Down")
        self.move_down_button.clicked.connect(self.move_item_down)
        self.layout.addWidget(self.move_down_button)

        self.setLayout(self.layout)

    def add_item(self):
        item_text = f"Item {self.list_widget.count() + 1}"  # Предустановленный текст
        new_item = QListWidgetItem(item_text)
        new_item.setFlags(new_item.flags() | Qt.ItemIsEditable)  # Устанавливаем флаг редактируемости
        
        current_row = self.list_widget.currentRow()
        
        if current_row != -1:  # Если элемент выделен
            self.list_widget.insertItem(current_row + 1, new_item)  # Вставляем после выделенного элемента
        else:
            self.list_widget.addItem(new_item)  # В противном случае добавляем в конец

    def delete_item(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            self.list_widget.takeItem(self.list_widget.row(current_item))

    def move_item_up(self):
        current_row = self.list_widget.currentRow()
        if current_row > 0:
            item = self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(current_row - 1, item)
            self.list_widget.setCurrentRow(current_row - 1)

    def move_item_down(self):
        current_row = self.list_widget.currentRow()
        if current_row < self.list_widget.count() - 1:
            item = self.list_widget.takeItem(current_row)
            self.list_widget.insertItem(current_row + 1, item)
            self.list_widget.setCurrentRow(current_row + 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditableListWidget()
    window.show()
    sys.exit(app.exec())
