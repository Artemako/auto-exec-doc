from PySide6.QtWidgets import (
    QWidget
)
from PySide6.QtGui import QFont



class Style:

    def __init__(self):
        self.__font = QFont()
        self.__font.setFamily("Open Sans")
    
    def set_style_for(self, widget):
        widget.setFont(self.__font)
        widget.setStyleSheet(qss)


qss = """

"""