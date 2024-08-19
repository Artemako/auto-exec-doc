import json

from PySide6.QtWidgets import (
    QWidget
)

import package.ui.nedimagetag_ui as nedimagetag_ui
# TODO РАБОТА С ИЗОБРАЖЕНИЯМИ
class NedImageTag(QWidget):
    def __init__(self, osbm, type_window, tag=None):
        self.__osbm = osbm
        self.__type_window = type_window
        self.__tag = tag
        self.__osbm.obj_logg.debug_logger(f"NedImageTag __init__(osbm, type_window, tag=None):\ntype_window = {type_window}\ntag = {tag}")
        super(NedImageTag, self).__init__()
        self.ui = nedimagetag_ui.Ui_NedImageTag()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__config_tag = self.__tag.get("config_tag")
        self.__config_dict = dict()
        if self.__config_tag:
            self.__config_dict = json.loads(self.__config_tag)
        # 
        # SIZINGMODE = []
        self.__data = {
            "UNIT": None,
            "SIZINGMODE": None,
            "WIDTH": None,
            "HEIGHT": None,
        }
        # config
        self.config_combox_units()
        self.config_by_type_window()

    def config_combox_units(self):
        combobox = self.ui.combox_units
        combobox.blockSignals(True)
        combobox.clear()
        # TODO единицы измерения
        combobox.addItem("", "empty")
        combobox.addItem("", "empty")
        combobox.addItem("", "empty")


    def config_by_type_window(self):
        self.__osbm.obj_logg.debug_logger(f"NedImageTag config_by_type_window():")
        if self.__type_window == "create":
            self.ui.btn_nestag.setText("Добавить изображение")

        elif self.__type_window == "edit":
            self.ui.btn_nestag.setText("Сохранить изображение")
        

    def get_save_data(self):
        self.save_data()
        self.__osbm.obj_logg.debug_logger(f"NedImageTag get_save_data():\nself.__data = {self.__data}")
        return self.__data


    def save_data(self):
        pass

