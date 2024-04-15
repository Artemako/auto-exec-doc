from PySide6.QtWidgets import QWidget

import package.ui.formimage_ui as formimage_ui


class FormImage(QWidget):
    def __init__(self):
        super(FormImage, self).__init__()
        self.ui = formimage_ui.Ui_FormImageWidget()
        self.ui.setupUi(self)
