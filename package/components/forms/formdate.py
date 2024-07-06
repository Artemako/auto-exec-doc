import json

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QDate

import package.ui.formdate_ui as formdate_ui



class FormDate(QWidget):
    def __init__(self, obs_manager, pair, config_content, config_date):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger(
            f"FormDate(self, pair, config_content, config_date): pair = {pair}, config_content = {config_content}, config_date = {config_date}"
        )

        super(FormDate, self).__init__()
        self.ui = formdate_ui.Ui_FormDateWidget()
        self.ui.setupUi(self)

        # формат по умолчанию
        self.str_format = "dd.MM.yyyy"

        # ПО УМОЛЧАНИЮ из config_content
        # заголовок
        self.ui.title.setText(config_content["title_tag"])

        # описание
        description_tag = config_content["description_tag"]
        if description_tag: 
            self.ui.textbrowser.setHtml(description_tag)
        else:
            self.ui.textbrowser.hide()

        # ОСОБЕННОСТИ из config_date
        for config in config_date:
            type_config = config.get("type_config")
            value_config = config.get("value_config")
            if type_config == "FORMAT":
                self.str_format = value_config
        
        # поле ввода
        value = pair.get("value")
        if value:
            self.ui.dateedit.setDate(self.string_to_qdate(value, self.str_format))
        else:
            self.ui.dateedit.setDate(QDate.currentDate())
        self.ui.dateedit.setDisplayFormat(self.str_format)         

        self.ui.dateedit.editingFinished.connect(
            lambda: self.set_new_value_in_pair(pair, self.qdate_to_string(self.ui.dateedit.date(), self.str_format))
        )

    def string_to_qdate(self, str_date, str_format) -> object:
        self.__obs_manager.obj_l.debug_logger(
            f"string_to_date(self, str_date, str_format): str_date = {str_date}, str_format = {str_format}"
        )
        return QDate.fromString(str_date, str_format)

    def qdate_to_string(self, date, str_format) -> str:
        self.__obs_manager.obj_l.debug_logger(
            f"date_to_string(self, date) -> str: date = {date}"
        )
        return str(date.toString(str_format))

    def set_new_value_in_pair(self, pair, new_value):
        self.__obs_manager.obj_l.debug_logger(
            f"set_new_value_in_pair(self, pair, new_value): pair = {pair}, new_value = {new_value}"
        )
        pair["value"] = new_value
        print(f"pair = {pair}")
