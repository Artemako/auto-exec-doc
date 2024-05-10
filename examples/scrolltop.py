from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QScrollArea, QVBoxLayout, QWidget, QPushButton

app = QApplication([])

# Create a QScrollArea
scroll_area = QScrollArea()

# Create a QWidget to put in the scroll area
widget = QWidget()

# Create a QVBoxLayout for the widget
layout = QVBoxLayout(widget)

# Add some widgets to the layout
layout.addWidget(QPushButton("Button 1"))
layout.addWidget(QPushButton("Button 2"))
layout.addWidget(QPushButton("Button 3"))

# Set the widget of the QScrollArea
scroll_area.setWidget(widget)

# Set the alignment of the QScrollArea
#scroll_area.setAlignment(Qt.AlignTop)

# Show the QScrollArea
scroll_area.show()

app.exec()