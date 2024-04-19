from PySide6.QtWidgets import QWidget

import package.ui.formtext_ui as formtext_ui

import package.controllers.scrollareainput as scrollareainput

import package.modules.log as log


class FormText(QWidget):
    def __init__(self, config_content, value):
        super(FormText, self).__init__()
        self.ui = formtext_ui.Ui_FormTextWidget()
        self.ui.setupUi(self)

        # заголовок
        self.ui.title.setText(config_content['title_content'])
        # поле ввода
        self.ui.lineedit.setText(value)
        # описание
        description_content = config_content['description_content'] 
        if description_content:
            self.ui.textbrowser.setHtml(config_content['description_content'])
        else:
            self.ui.textbrowser.hide()

        # connect
        self.ui.lineedit.textChanged.connect(lambda text: FormText.set_value_in_data(config_content, text))

    @staticmethod
    def set_value_in_data(config_content, value):
        log.Log.debug_logger(f"set_value_in_data(config_content, value): config_content = {config_content}, value = {value}")
        scrollareainput.ScroolAreaInput.get_data()[config_content['name_content']] = value
