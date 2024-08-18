from PySide6.QtWidgets import QWidget

import package.ui.formtext_ui as formtext_ui

import package.controllers.sainputforms as sainputforms


class FormText(QWidget):
    def __init__(self, osbm, pair, current_tag):
        self.__osbm = osbm
        self.__pair = pair
        self.__current_tag = current_tag
        self.__osbm.obj_logg.debug_logger(f"FormText __init__(pair, current_tag): pair = {pair},\ncurrent_tag = {current_tag}")        
        
        super(FormText, self).__init__()
        self.ui = formtext_ui.Ui_FormTextWidget()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__icons = self.__osbm.obj_icons.get_icons()
        # 
        self.config()

    def config(self):
        # тип тега
        key_icon = self.__osbm.obj_icons.get_key_icon_by_type_tag(self.__current_tag.get("type_tag"))
        qicon_type_tag = self.__icons.get(key_icon)
        self.ui.label_typetag.setPixmap(qicon_type_tag)
        # заголовок 
        self.ui.title.setText(self.__current_tag.get('title_tag'))
        # поле ввода
        self.ui.lineedit.setText(self.__pair.get("value_pair"))
        # описание
        description_tag = self.__current_tag.get('description_tag')
        if description_tag:
            self.ui.textbrowser.setHtml(description_tag)
        else:
            self.ui.textbrowser.hide()

        # connect
        self.ui.lineedit.textChanged.connect(lambda text: self.set_new_value_in_pair(text))

    def set_new_value_in_pair(self, new_value):
        self.__osbm.obj_logg.debug_logger(f"FormText set_new_value_in_pair(pair, new_value):\nnew_value = {new_value}")
        self.__pair["value_pair"] = new_value