import json

from PySide6.QtWidgets import (
    QWidget
)

import package.ui.neddatetag_ui as neddatetag_ui
# TODO РАБОТА С ДАТАМИ
class NedDateTag(QWidget):
    def __init__(self, obs_manager, type_window, tag=None):
        self.__obs_manager = obs_manager
        self.__type_window = type_window
        self.__tag = tag
        self.__obs_manager.obj_l.debug_logger(f"NedDateTag __init__(obs_manager, type_window, tag=None):\ntype_window = {type_window}\ntag = {tag}")
        super(NedDateTag, self).__init__()
        self.ui = neddatetag_ui.Ui_NedDateTag()
        self.ui.setupUi(self)
        #
        self.__config_tag = self.__tag.get("config_tag")
        self.__config_dict = dict()
        if self.__config_tag:
            self.__config_dict = json.loads(self.__config_tag)
        # 
        self.__data = {
            "FORMAT": None
        }
        #
        self.config_lineedit_format()

    def get_save_data(self):
        self.save_data()
        self.__obs_manager.obj_l.debug_logger(f"NedDateTag get_save_data():\nself.__data = {self.__data}")
        return self.__data

    def config_lineedit_format(self):
        str_format = self.__config_dict.get("FORMAT", "dd.MM.yyyy")
        self.ui.lineedit_format.setText(str_format)

    def save_data(self):
        str_format = self.ui.lineedit_format.text()
        self.__data["FORMAT"] = str_format

