import json

from PySide6.QtWidgets import (
    QWidget
)

import package.ui.neddatevariable_ui as neddatevariable_ui
# TODO РАБОТА С ДАТАМИ
class NedDateVariable(QWidget):
    def __init__(self, osbm, type_window, variable=None):
        self.__osbm = osbm
        self.__type_window = type_window
        self.__variable = variable
        self.__osbm.obj_logg.debug_logger(f"NedDateVariable __init__(osbm, type_window, variable=None):\ntype_window = {type_window}\nvariable = {variable}")
        super(NedDateVariable, self).__init__()
        self.ui = neddatevariable_ui.Ui_NedDateVariable()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__config_dict = dict()
        if self.__variable and self.__variable.get("type_variable") == "DATE":
            self.__config_variable = self.__variable.get("config_variable")
            if self.__config_variable:
                self.__config_dict = json.loads(self.__config_variable)
        #
        #
        self.config_lineedit_format()
        self.text_changed()

    def get_save_data(self):
        self.save_data()
        self.__osbm.obj_logg.debug_logger(f"NedDateVariable get_save_data():\nself.__data = {self.__data}")
        return self.__data
    
    def save_data(self):
        str_format = self.ui.lineedit_format.text()
        self.__data = {
            "FORMAT": str_format
        }

    def config_lineedit_format(self):
        self.__osbm.obj_logg.debug_logger("NedDateVariable config_lineedit_format()")
        if self.__type_window == "create":
            str_format = "dd.MM.yyyy"
        elif self.__type_window == "edit":
            str_format = self.__config_dict.get("FORMAT")
        self.ui.lineedit_format.setText(str_format)
        # события
        self.ui.lineedit_format.textChanged.connect(self.text_changed)
        self.ui.dateedit_check.dateChanged.connect(self.text_changed)

    def text_changed(self):
        try:
            self.ui.dateedit_check.setDisplayFormat(self.ui.lineedit_format.text())
            self.ui.label_result.setText(self.ui.dateedit_check.text())
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"NedDateVariable text_changed():\n{e}")


    

