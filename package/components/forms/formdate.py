from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QDateTime

import package.ui.formdate_ui as formdate_ui

import package.controllers.scrollareainput as scrollareainput

import package.modules.log as log

class FormDate(QWidget):
    def __init__(self, config_content, config_date, value):
        super(FormDate, self).__init__()
        self.ui = formdate_ui.Ui_FormDateWidget()
        self.ui.setupUi(self)

        # ПО УМОЛЧАНИЮ из config_content
        # заголовок
        self.ui.title.setText(config_content['title_content'])
        # поле ввода
        self.ui.dateedit.setDateTime(QDateTime.currentDateTime())
        self.ui.dateedit.setDisplayFormat("dd.MM.yyyy")
        # описание
        self.ui.textbrowser.hide()

        # ОСОБЕННОСТИ из config_date


        # connect
        self.ui.dateedit.dateChanged.connect(lambda date: FormDate.set_value_in_data(config_content, date))

    @staticmethod
    def set_value_in_data(config_content, value):
        log.Log.debug_logger(f"set_value_in_data(config_content, value): config_content = {config_content}, value = {value}")
        scrollareainput.ScroolAreaInput.get_data()[config_content['name_content']] = value