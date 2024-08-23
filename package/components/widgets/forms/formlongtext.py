from PySide6.QtWidgets import QWidget

import package.ui.formlongtext_ui as formlongtext_ui


class FormLongTextWidget(QWidget):
    def __init__(self, osbm, pair, current_variable):
        self.__osbm = osbm
        self.__pair = pair
        self.__current_variable = current_variable
        self.__osbm.obj_logg.debug_logger(f"FormLongTextWidget __init__(pair, current_variable): pair = {pair},\ncurrent_variable = {current_variable}")        
        
        super(FormLongTextWidget, self).__init__()
        self.ui = formlongtext_ui.Ui_FormLongTextWidget()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__icons = self.__osbm.obj_icons.get_icons()
        # 
        self.config()

    def config(self):
        # тип переменной
        key_icon = self.__osbm.obj_icons.get_key_icon_by_type_variable(self.__current_variable.get("type_variable"))
        qicon_type_variable = self.__icons.get(key_icon)
        self.ui.label_typevariable.setPixmap(qicon_type_variable)
        # заголовок 
        self.ui.title.setText(self.__current_variable.get('title_variable'))
        # поле ввода
        self.ui.textedit.setText(self.__pair.get("value_pair"))
        # описание
        description_variable = self.__current_variable.get('description_variable')
        if description_variable:
            self.ui.textbrowser.setHtml(description_variable)
        else:
            self.ui.textbrowser.hide()

        # connect
        self.ui.textedit.textChanged.connect(self.set_new_value_in_pair)

    def set_new_value_in_pair(self):
        self.__osbm.obj_logg.debug_logger(f"FormText set_new_value_in_pair(pair, new_value):\nnew_value = {self.ui.textedit.toPlainText()}")
        self.__pair["value_pair"] = self.ui.textedit.toPlainText()
