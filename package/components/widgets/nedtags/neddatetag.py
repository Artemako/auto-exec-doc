import json

from PySide6.QtWidgets import (
    QWidget
)

import package.ui.neddatetag_ui as neddatetag_ui
# TODO РАБОТА С ДАТАМИ
class NedDateTag(QWidget):
    def __init__(self, osbm, type_window, tag=None):
        self.__osbm = osbm
        self.__type_window = type_window
        self.__tag = tag
        self.__osbm.obj_logg.debug_logger(f"NedDateTag __init__(osbm, type_window, tag=None):\ntype_window = {type_window}\ntag = {tag}")
        super(NedDateTag, self).__init__()
        self.ui = neddatetag_ui.Ui_NedDateTag()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        
        self.__config_dict = dict()
        if self.__tag:
            self.__config_tag = self.__tag.get("config_tag")
            if self.__config_tag:
                self.__config_dict = json.loads(self.__config_tag)
        #
        self.config_lineedit_format()

    def get_save_data(self):
        self.save_data()
        self.__osbm.obj_logg.debug_logger(f"NedDateTag get_save_data():\nself.__data = {self.__data}")
        return self.__data

    def config_lineedit_format(self):
        self.__osbm.obj_logg.debug_logger("NedDateTag config_lineedit_format()")
        str_format = self.__config_dict.get("FORMAT", "dd.MM.yyyy")
        self.ui.lineedit_format.setText(str_format)

    def save_data(self):
        str_format = self.ui.lineedit_format.text()
        self.__data = {
            "FORMAT": str_format
        }

