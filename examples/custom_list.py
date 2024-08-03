import sys
from PySide6.QtWidgets import QApplication, QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel

class ListItem(QWidget):
    def __init__(self, text):
        super().__init__()
        
        layout = QHBoxLayout()
        
        # Текстовый элемент
        self.label = QLabel(text)
        
        # Кнопка в конце
        self.button = QPushButton("Click Me")
        
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        
        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.list_widget = QListWidget()

        for i in range(5):
            item = ListItem(f"Item {i + 1}")
            list_widget_item = QListWidgetItem()
            list_widget_item.setSizeHint(item.sizeHint())
            
            self.list_widget.addItem(list_widget_item)
            self.list_widget.setItemWidget(list_widget_item, item)

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    main_window = MainWindow()
    main_window.resize(300, 400)
    main_window.show()
    
    sys.exit(app.exec())
