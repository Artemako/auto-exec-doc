from PySide6.QtWidgets import (
    QWidget
)

import package.ui.nedtabletag_ui as nedtabletag_ui


class NedTableTag(QWidget):
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger("NedTableTag __init__(obs_manager)")
        super(NedTableTag, self).__init__()
        self.ui = nedtabletag_ui.Ui_NedTableTag()
        self.ui.setupUi(self)

    