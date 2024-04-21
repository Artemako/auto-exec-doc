from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QDateTime

import package.ui.formdate_ui as formdate_ui

import package.controllers.scrollareainput as scrollareainput

import package.modules.log as log


class FormDate(QWidget):
    def __init__(self, pair, config_content, config_date):
        log.Log.debug_logger(f"FormDate(self, pair, config_content, config_date): pair = {pair}, config_content = {config_content}, config_date = {config_date}" )
        
        super(FormDate, self).__init__()
        self.ui = formdate_ui.Ui_FormDateWidget()
        self.ui.setupUi(self)


        # ПО УМОЛЧАНИЮ из config_content
        # заголовок
        self.ui.title.setText(config_content["title_content"])
        # поле ввода
        self.ui.dateedit.setDateTime(pair.get("value") if pair.get("value") else QDateTime.currentDateTime())
        self.ui.dateedit.setDisplayFormat("dd.MM.yyyy")
        # описание
        description_content = config_content['description_content'] 
        if description_content:
            self.ui.textbrowser.setHtml(description_content)
        else:
            self.ui.textbrowser.hide()


        # ОСОБЕННОСТИ из config_date
        for config in config_date:
            type_config = config.get("type_config")
            value_config = config.get("value_config")
            if type_config == "FORMAT":
                self.ui.dateedit.setDisplayFormat(value_config)

        # connect
        self.ui.dateedit.dateChanged.connect(
            lambda date: self.set_new_value_in_pair(pair, date)
        )

    def set_new_value_in_pair(self, pair, new_value):
        log.Log.debug_logger(f"set_new_value_in_pair(self, pair, new_value): pair = {pair}, new_value = {new_value}")
        pair["value"] = new_value
        print(pair)