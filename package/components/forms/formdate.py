from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QDateTime

import package.ui.formdate_ui as formdate_ui

import package.controllers.scrollareainput as scrollareainput

import package.modules.log as log


class FormDate(QWidget):
    def __init__(self, section_index, config_content, config_date, value):
        super(FormDate, self).__init__()
        self.ui = formdate_ui.Ui_FormDateWidget()
        self.ui.setupUi(self)

        self.section_index = section_index

        # ПО УМОЛЧАНИЮ из config_content
        # заголовок
        self.ui.title.setText(config_content["title_content"])
        # поле ввода
        self.ui.dateedit.setDateTime(QDateTime.currentDateTime())
        self.ui.dateedit.setDisplayFormat("dd.MM.yyyy")
        # описание
        self.ui.textbrowser.hide()

        # ОСОБЕННОСТИ из config_date
        for config in config_date:
            type_config = config.get("type_config")
            value_config = config.get("value_config")
            if type_config == "FORMAT":
                self.ui.dateedit.setDisplayFormat(value_config)
            print(f"""
                ПРИВЕТ ВСЕМ
                type_config = {type_config}
                value_config = {value_config}
                """)

        # connect
        self.ui.dateedit.dateChanged.connect(
            lambda date: self.set_value_in_sections_info(config_content, date)
        )

    def set_value_in_sections_info(self, config_content, value):
        log.Log.debug_logger(
            f"set_value_in_sections_info(self, config_content, value): config_content = {config_content}, value = {value}"
        )
        # TODO
        sections_info = scrollareainput.ScroolAreaInput.get_sections_info()
        section_info = sections_info[self.section_index]
        section_data = section_info.get("data")
        section_data[config_content.get("name_content")] = value
