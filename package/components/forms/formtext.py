from PySide6.QtWidgets import QWidget

import package.ui.formtext_ui as formtext_ui

import package.controllers.scrollareainput as scrollareainput

import package.modules.log as log


class FormText(QWidget):
    def __init__(self, pair, config_content):
        log.obj_l.debug_logger(f"FormText(self, pair, config_content): pair = {pair}, config_content = {config_content}")        
        
        super(FormText, self).__init__()
        self.ui = formtext_ui.Ui_FormTextWidget()
        self.ui.setupUi(self)

        # заголовок
        self.ui.title.setText(config_content['title_content'])
        # поле ввода
        self.ui.lineedit.setText(pair.get("value"))
        # описание
        description_content = config_content['description_content'] 
        if description_content:
            self.ui.textbrowser.setHtml(description_content)
        else:
            self.ui.textbrowser.hide()

        # connect
        self.ui.lineedit.textChanged.connect(lambda text: self.set_new_value_in_pair(pair, text))

    staticmethod
    def set_new_value_in_pair(self, pair, new_value):
        log.obj_l.debug_logger(f"set_new_value_in_pair(self, pair, new_value): pair = {pair}, new_value = {new_value}")
        pair["value"] = new_value
        print(pair)