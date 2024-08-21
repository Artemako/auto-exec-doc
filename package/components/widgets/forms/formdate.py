import json

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QDate

import package.ui.formdate_ui as formdate_ui


class FormDate(QWidget):
    def __init__(self, osbm, pair, current_variable, config_dict):
        self.__osbm = osbm
        self.__pair = pair
        self.__current_variable = current_variable
        self.__config_dict = config_dict
        self.__osbm.obj_logg.debug_logger(
            f"FormDate __init__(self, pair, current_variable, config_dict):\npair = {pair},\ncurrent_variable = {current_variable},\nconfig_dict = {config_dict}"
        )
        super(FormDate, self).__init__()
        self.ui = formdate_ui.Ui_FormDateWidget()
        self.ui.setupUi(self)
        # ИКОНКИ
        self.__icons = self.__osbm.obj_icons.get_icons()
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__str_format = "dd.MM.yyyy"
        #
        self.config()
        
        

    def config(self):
        self.__osbm.obj_logg.debug_logger("FormDate config()")
        # ПО УМОЛЧАНИЮ из current_variable
        # тип переменной
        key_icon = self.__osbm.obj_icons.get_key_icon_by_type_variable(self.__current_variable.get("type_variable"))
        qicon_type_variable = self.__icons.get(key_icon)
        self.ui.label_typevariable.setPixmap(qicon_type_variable)
        # заголовок
        self.ui.title.setText(self.__current_variable.get("title_variable"))

        # описание
        description_variable = self.__current_variable.get("description_variable")
        if description_variable:
            self.ui.textbrowser.setHtml(description_variable)
        else:
            self.ui.textbrowser.hide()

        # ОСОБЕННОСТИ из config_dict
        format_date = self.__config_dict.get("FORMAT")
        if format_date:
            self.__str_format = format_date

        # поле ввода
        value = self.__pair.get("value_pair")
        if value:
            self.ui.dateedit.setDate(self.string_to_qdate(value, self.__str_format))
        else:
            self.ui.dateedit.setDate(QDate.currentDate())
        self.ui.dateedit.setDisplayFormat(self.__str_format)

        self.ui.dateedit.editingFinished.connect(
            lambda: self.set_new_value_in_pair(
                self.qdate_to_string(self.ui.dateedit.date(), self.__str_format)
            )
        )

    def string_to_qdate(self, str_date, str_format) -> object:
        self.__osbm.obj_logg.debug_logger(
            f"FormDate string_to_date(self, str_date, str_format):\nstr_date = {str_date},\nstr_format = {str_format}"
        )
        return QDate.fromString(str_date, str_format)

    def qdate_to_string(self, date, str_format) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"FormDate date_to_string(self, date) -> str:\ndate = {date}"
        )
        return str(date.toString(str_format))

    def set_new_value_in_pair(self, new_value):
        self.__osbm.obj_logg.debug_logger(
            f"FormDate set_new_value_in_pair(self, pair, new_value):\nnew_value = {new_value}"
        )
        self.__pair["value_pair"] = new_value
        print(f"pair = {self.__pair}")
