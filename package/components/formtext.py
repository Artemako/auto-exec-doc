from PySide6.QtWidgets import QWidget

import package.ui.formtext_ui as formtext_ui


class FormText(QWidget):
    def __init__(self):
        super(FormText, self).__init__()
        self.ui = formtext_ui.Ui_FormTextWidget()
        self.ui.setupUi(self)
