from PySide6.QtWidgets import QWidget

import package.ui.formtable_ui as formtable_ui


class FormTable(QWidget):
    def __init__(self):
        super(FormTable, self).__init__()
        self.ui = formtable_ui.Ui_FormTableWidget()
        self.ui.setupUi(self)
