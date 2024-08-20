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
        self.__data = {}
        self.__config_dict = dict()
        if self.__tag:
            self.__config_tag = self.__tag.get("config_tag")
            if self.__config_tag:
                self.__config_dict = json.loads(self.__config_tag)
        # config
        self.config_combox_units()
        self.config_combox_sms()
        self.config_by_type_window()
        #
        self.connecting_actions()

    def config_combox_units(self):
        self.__osbm.obj_logg.debug_logger("NedImageTag config_combox_units()")
        combobox = self.ui.combox_units
        combobox.blockSignals(True)
        combobox.clear()
        units = self.__osbm.obj_comwith.units.get_units()
        for unit in units:
            combobox.addItem(unit.name, unit.data)
        combobox.blockSignals(False)

    def config_combox_sms(self):
        self.__osbm.obj_logg.debug_logger("NedImageTag config_combox_sms()")
        combobox = self.ui.combox_sms
        combobox.blockSignals(True)
        combobox.clear()
        sizing_modes = self.__osbm.obj_comwith.sizing_modes.get_sizing_modes()
        for sizing_mode in sizing_modes:
            combobox.addItem(sizing_mode.name, sizing_mode.data)
        combobox.blockSignals(False)

    def config_by_type_window(self):
        self.__osbm.obj_logg.debug_logger("NedImageTag config_by_type_window()")
        if self.__type_window == "create":
            self.ui.combox_units.setCurrentIndex(0)
            self.ui.combox_sms.setCurrentIndex(0)
            self.set_enabled_for_width_height(False)

        elif self.__type_window == "edit":
            # получение данных
            unit = self.__config_dict.get("UNIT")
            sizing_mode = self.__config_dict.get("SIZINGMODE")
            width = self.__config_dict.get("WIDTH")
            height = self.__config_dict.get("HEIGHT")
            # узнаем индексы по значению для комбобоксов
            index_unit = self.__osbm.obj_comwith.units.get_unit_by_data(unit)
            index_unit = index_unit if index_unit else 0
            index_sizing_mode = self.__osbm.obj_comwith.sizing_modes.get_sizing_mode_by_data(sizing_mode)
            index_sizing_mode = index_sizing_mode if index_sizing_mode else 0
            #
            self.ui.combox_units.setCurrentIndex(index_unit)
            self.ui.combox_sms.setCurrentIndex(index_sizing_mode)
            # установка значений ширины и высоты
            if width:
                self.ui.dsb_width.setText(width)
            if height:
                self.ui.dsb_height.setText(height)
            # установка активности
            self.set_enabled_wh_by_index(index_sizing_mode)

    def set_enabled_for_width_height(self, state):
        self.ui.title_wh.setEnabled(state)
        self.ui.dsb_width.setEnabled(state)
        self.ui.dsb_height.setEnabled(state)

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("NedImageTag connecting_actions()")
        self.ui.combox_sms.currentIndexChanged.connect(self.set_enabled_wh_by_index)


    def set_enabled_wh_by_index(self, index): 
        self.__osbm.obj_logg.debug_logger(f"NedImageTag combox_sms_index_changed(index): index = {index}")
        is_wh = self.__osbm.obj_comwith.sizing_modes.get_is_wh_by_index(index)
        if is_wh:
            self.set_enabled_for_width_height(True)
        else:
            self.set_enabled_for_width_height(False)


    def get_save_data(self):
        self.save_data()
        self.__osbm.obj_logg.debug_logger(f"NedImageTag get_save_data():\nself.__data = {self.__data}")
        return self.__data


    def save_data(self):
        self.__osbm.obj_logg.debug_logger("NedImageTag save_data()")
        unit_data = self.ui.combox_units.currentData()
        sizing_mode_data = self.ui.combox_sms.currentData()
        width = float(self.ui.dsb_width.text().replace(",","."))
        height = float(self.ui.dsb_height.text().replace(",","."))
        self.__data = {
            "UNIT": unit_data,
            "SIZINGMODE": sizing_mode_data,
            "WIDTH": width,
            "HEIGHT": height,
        }


