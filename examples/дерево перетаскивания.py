import sys
from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem

class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()

        self.setDragEnabled(True)
        self.setDragDropMode(QTreeWidget.InternalMove)

        for i in range(3):
            parent = QTreeWidgetItem(self, [f'Parent {i}'])
            for j in range(3):
                QTreeWidgetItem(parent, [f'Child {i}-{j}'])

        self.setHeaderLabels(['Tree'])

    def dropEvent(self, event):
        super().dropEvent(event)
        item = self.itemAt(event.position().toPoint())
        if item:
            print(f'Item dropped: {item.text(0)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tree = TreeWidget()
    tree.show()
    sys.exit(app.exec())
