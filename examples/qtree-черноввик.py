import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, 
    QTreeWidget, QTreeWidgetItem, QMessageBox
)

class TreeEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tree Editor")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout(self)

        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderLabels(["Items"])
        self.layout.addWidget(self.tree_widget)

        self.add_group_button = QPushButton("Добавить группу", self)
        self.add_group_button.clicked.connect(self.add_group)
        self.layout.addWidget(self.add_group_button)

        self.add_item_button = QPushButton("Добавить элемент", self)
        self.add_item_button.clicked.connect(self.add_item)
        self.layout.addWidget(self.add_item_button)

        self.remove_button = QPushButton("Удалить", self)
        self.remove_button.clicked.connect(self.remove_item)
        self.layout.addWidget(self.remove_button)

        self.move_up_button = QPushButton("Переместить вверх", self)
        self.move_up_button.clicked.connect(self.move_up)
        self.layout.addWidget(self.move_up_button)

        self.move_down_button = QPushButton("Переместить вниз", self)
        self.move_down_button.clicked.connect(self.move_down)
        self.layout.addWidget(self.move_down_button)

    def add_group(self):
        name = f"Группа {self.tree_widget.topLevelItemCount() + 1}"
        QTreeWidgetItem(self.tree_widget, [name])

    def add_item(self):
        current_item = self.tree_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите группу.")
            return
        name = f"Элемент {current_item.childCount() + 1}"
        QTreeWidgetItem(current_item, [name])

    def remove_item(self):
        current_item = self.tree_widget.currentItem()
        if current_item:
            index = self.tree_widget.indexOfTopLevelItem(current_item)
            if index != -1:  # Удаление группы
                self.tree_widget.takeTopLevelItem(index)
            else:  # Удаление элемента
                parent_item = current_item.parent()
                if parent_item:
                    parent_item.removeChild(current_item)
        else:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите элемент или группу.")

    def move_up(self):
        current_item = self.tree_widget.currentItem()
        if current_item:
            index = self.tree_widget.indexOfTopLevelItem(current_item)
            if index > 0:  # Перемещение группы вверх
                self.tree_widget.insertTopLevelItem(index - 1, self.tree_widget.takeTopLevelItem(index))
            else:  
                parent_item = current_item.parent()
                if parent_item:
                    parent_index = parent_item.indexOfChild(current_item)
                    if parent_index > 0:
                        parent_item.insertChild(parent_index - 1, parent_item.takeChild(parent_index))

    def move_down(self):
        current_item = self.tree_widget.currentItem()
        if current_item:
            index = self.tree_widget.indexOfTopLevelItem(current_item)
            if index < self.tree_widget.topLevelItemCount() - 1:  # Перемещение группы вниз
                self.tree_widget.insertTopLevelItem(index + 1, self.tree_widget.takeTopLevelItem(index))
            else:  
                parent_item = current_item.parent()
                if parent_item:
                    parent_index = parent_item.indexOfChild(current_item)
                    if parent_index < parent_item.childCount() - 1:
                        parent_item.insertChild(parent_index + 1, parent_item.takeChild(parent_index))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = TreeEditor()
    editor.show()
    sys.exit(app.exec())
