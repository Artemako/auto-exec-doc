import json

from PySide6.QtWidgets import (
    QWidget
)
from PySide6.QtCore import QDate, QLocale

import package.ui.neddatevariable_ui as neddatevariable_ui

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
        self.config_by_type()
        self.config_lineedit_format()  
        self.config_combox_language()      
        self.text_changed()

    def get_save_data(self):
        self.save_data()
        self.__osbm.obj_logg.debug_logger(f"NedDateVariable get_save_data():\nself.__data = {self.__data}")
        return self.__data
    
    def save_data(self):
        str_format = self.ui.lineedit_format.text()
        language = self.ui.combox_language.currentData()
        self.__data = {
            "FORMAT": str_format,
            "LANGUAGE": language,
        }

    def config_by_type(self):
        if self.__type_window == "create":
            self.__str_format = "dd.MM.yyyy"
            self.__language = "ru_RU"
        elif self.__type_window == "edit":
            self.__str_format = self.__config_dict.get("FORMAT")
            self.__language = self.__config_dict.get("LANGUAGE")

    def config_lineedit_format(self):
        self.__osbm.obj_logg.debug_logger("config_lineedit_format config()")
        
        self.ui.lineedit_format.setText(self.__str_format)
        # события
        self.ui.lineedit_format.textChanged.connect(self.text_changed)
        self.ui.dateedit_check.dateChanged.connect(self.text_changed)

    def config_combox_language(self):
        self.__osbm.obj_logg.debug_logger("NedDateVariable config_combox_language()")
        combobox = self.ui.combox_language
        combobox.blockSignals(True)
        combobox.clear()
        languages = self.__osbm.obj_comwith.languages.get_languages()
        for language in languages:
            combobox.addItem(language.name, language.data)
        #
        if self.__type_window == "create":
            combobox.setCurrentIndex(0)
        elif self.__type_window == "edit":
            index_by_data = combobox.findData(self.__language)
            combobox.setCurrentIndex(index_by_data)
        #
        combobox.blockSignals(False)
        #
        self.language_changed()
        combobox.currentIndexChanged.connect(self.language_changed)

    def language_changed(self, index = None):
        print("language_changed КОКОКОКО")
        self.ui.dateedit_check.setLocale(QLocale(self.ui.combox_language.currentData()))

    def text_changed(self):
        try:
            self.ui.dateedit_check.setDisplayFormat(self.ui.lineedit_format.text())
            self.ui.label_result.setText(self.ui.dateedit_check.text())
        except Exception as e:
            self.__osbm.obj_logg.error_logger(f"NedDateVariable text_changed():\n{e}")


    

