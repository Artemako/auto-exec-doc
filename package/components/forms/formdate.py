from PySide6.QtWidgets import QWidget

import package.ui.formdate_ui as formdate_ui


class FormDate(QWidget):
    def __init__(self):
        super(FormDate, self).__init__()
        self.ui = formdate_ui.Ui_FormDateWidget()
        self.ui.setupUi(self)
