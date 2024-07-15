from PySide6.QtWidgets import (
    QWidget
)

import package.ui.neddatetag_ui as neddatetag_ui


class NedDateTag(QWidget):
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        super(NedDateTag, self).__init__()
        self.ui = neddatetag_ui.Ui_NedDateTag()
        self.ui.setupUi(self)

    