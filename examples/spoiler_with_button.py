from PySide2.QtWidgets import QApplication, QMainWindow, QGroupBox, QVBoxLayout, QPushButton, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Spoiler Widget")

        # Create the spoiler group box
        self.spoiler_group_box = QGroupBox("Click to reveal content")
        layout = QVBoxLayout()
        self.spoiler_group_box.setLayout(layout)

        # Create a label to hold the content
        self.content_label = QLabel("This is the spoiler content.")
        layout.addWidget(self.content_label)

        # Create a button to toggle the visibility of the content
        self.toggle_button = QPushButton("Show/Hide")
        self.toggle_button.clicked.connect(self.toggle_content)
        layout.addWidget(self.toggle_button)

        # Hide the content initially
        self.content_label.hide()

        # Set the central widget
        self.setCentralWidget(self.spoiler_group_box)

    def toggle_content(self):
        if self.content_label.isVisible():
            self.content_label.hide()
            self.toggle_button.setText("Show")
        else:
            self.content_label.show()
            self.toggle_button.setText("Hide")

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
