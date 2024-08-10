from PySide6.QtWidgets import (
    QWidget
)

import package.ui.neddatetag_ui as neddatetag_ui
# TODO РАБОТА С ДАТАМИ
class NedDateTag(QWidget):
    def __init__(self, obs_manager, type_window):
        self.__obs_manager = obs_manager
        self.__type_window = type_window
        self.__obs_manager.obj_l.debug_logger("NedDateTag __init__(obs_manager, type_window)")
        super(NedDateTag, self).__init__()
        self.ui = neddatetag_ui.Ui_NedDateTag()
        self.ui.setupUi(self)

    