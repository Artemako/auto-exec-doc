from PySide6.QtWidgets import QWidget

import package.ui.formtext_ui as formtext_ui

import package.controllers.scrollareainput as scrollareainput

import package.modules.log as log


class FormText(QWidget):
    def __init__(self, section_index, config_content, value):
        super(FormText, self).__init__()
        self.ui = formtext_ui.Ui_FormTextWidget()
        self.ui.setupUi(self)

        self.section_index = section_index

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
        self.ui.lineedit.textChanged.connect(lambda text: self.set_value_in_sections_info(config_content, text))

    staticmethod
    def set_value_in_sections_info(self, config_content, value):
        log.Log.debug_logger(f"set_value_in_sections_info(self, config_content, value): config_content = {config_content}, value = {value}")
        sections_info = scrollareainput.ScroolAreaInput.get_sections_info()
        section_info = sections_info[self.section_index]
        section_data = section_info.get("data")
        section_data[config_content.get('name_content')] = value