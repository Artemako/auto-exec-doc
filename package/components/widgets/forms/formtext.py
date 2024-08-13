from PySide6.QtWidgets import QWidget

import package.ui.formtext_ui as formtext_ui

import package.controllers.sainputforms as sainputforms


class FormText(QWidget):
    def __init__(self, obs_manager, pair, current_tag):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger(f"FormText __init__(pair, current_tag): pair = {pair},\ncurrent_tag = {current_tag}")        
        
        super(FormText, self).__init__()
        self.ui = formtext_ui.Ui_FormTextWidget()
        self.ui.setupUi(self)

        # заголовок
        self.ui.title.setText(current_tag.get('title_tag'))
        # поле ввода
        self.ui.lineedit.setText(pair.get("value"))
        # описание
        description_tag = current_tag.get('description_tag')
        if description_tag:
            self.ui.textbrowser.setHtml(description_tag)
        else:
            self.ui.textbrowser.hide()

        # connect
        self.ui.lineedit.textChanged.connect(lambda text: self.set_new_value_in_pair(pair, text))

    def set_new_value_in_pair(self, pair, new_value):
        self.__obs_manager.obj_l.debug_logger(f"FormText set_new_value_in_pair(pair, new_value):\npair = {pair},\nnew_value = {new_value}")
        pair["value"] = new_value
        print(pair)