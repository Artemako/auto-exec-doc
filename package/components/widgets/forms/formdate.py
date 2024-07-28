import json

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QDate

import package.ui.formdate_ui as formdate_ui


class FormDate(QWidget):
    def __init__(self, obs_manager, pair, config_tag, config_date):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger(
            f"FormDate __init__(self, pair, config_tag, config_date):\npair = {pair},\nconfig_tag = {config_tag},\nconfig_date = {config_date}"
        )

        super(FormDate, self).__init__()
        self.ui = formdate_ui.Ui_FormDateWidget()
        self.ui.setupUi(self)

        # формат по умолчанию
        self.str_format = "dd.MM.yyyy"

        # ПО УМОЛЧАНИЮ из config_tag
        # заголовок
        self.ui.title.setText(config_tag["title_tag"])

        # описание
        description_tag = config_tag["description_tag"]
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
            lambda: self.set_new_value_in_pair(
                pair, self.qdate_to_string(self.ui.dateedit.date(), self.str_format)
            )
        )

    def string_to_qdate(self, str_date, str_format) -> object:
        self.__obs_manager.obj_l.debug_logger(
            f"FormDate string_to_date(self, str_date, str_format):\nstr_date = {str_date},\nstr_format = {str_format}"
        )
        return QDate.fromString(str_date, str_format)

    def qdate_to_string(self, date, str_format) -> str:
        self.__obs_manager.obj_l.debug_logger(
            f"FormDate date_to_string(self, date) -> str:\ndate = {date}"
        )
        return str(date.toString(str_format))

    def set_new_value_in_pair(self, pair, new_value):
        self.__obs_manager.obj_l.debug_logger(
            f"FormDate set_new_value_in_pair(self, pair, new_value):\npair = {pair},\nnew_value = {new_value}"
        )
        pair["value"] = new_value
        print(f"pair = {pair}")
