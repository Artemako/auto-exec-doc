from PySide6.QtWidgets import QWidget

import package.ui.formtext_ui as formtext_ui

import package.controllers.scrollareainput as scrollareainput


class FormText(QWidget):
    def __init__(self, obs_manager, pair, config_content):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger(f"FormText(self, pair, config_content): pair = {pair}, config_content = {config_content}")        
        
        super(FormText, self).__init__()
        self.ui = formtext_ui.Ui_FormTextWidget()
        self.ui.setupUi(self)

        # заголовок
        self.ui.title.setText(config_content['title_tag'])
        # поле ввода
        self.ui.lineedit.setText(pair.get("value"))
        # описание
        description_tag = config_content['description_tag'] 
        if description_tag:
            self.ui.textbrowser.setHtml(description_tag)
        else:
            self.ui.textbrowser.hide()

        # connect
        self.ui.lineedit.textChanged.connect(lambda text: self.set_new_value_in_pair(pair, text))

    def set_new_value_in_pair(self, pair, new_value):
        self.__obs_manager.obj_l.debug_logger(f"set_new_value_in_pair(self, pair, new_value): pair = {pair}, new_value = {new_value}")
        pair["value"] = new_value
        print(pair)