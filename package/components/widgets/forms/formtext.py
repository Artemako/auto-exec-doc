from PySide6.QtWidgets import QWidget

import package.ui.formtext_ui as formtext_ui

import package.controllers.tabwinputforms as tabwinputforms


class FormText(QWidget):
    def __init__(self, osbm, pair, current_variable):
        self.__osbm = osbm
        self.__pair = pair
        self.__current_variable = current_variable
        self.__osbm.obj_logg.debug_logger(f"FormText __init__(pair, current_variable): pair = {pair},\ncurrent_variable = {current_variable}")        
        
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
        # тип переменной
        qicon_type_variable = self.__osbm.obj_comwith.variable_types.get_icon_by_type_variable(self.__current_variable.get("type_variable"))
        self.ui.label_typevariable.setPixmap(qicon_type_variable)
        # заголовок + перменная
        self.ui.title.setText(self.__current_variable.get('title_variable'))
        self.ui.label_variable.setText(f"<i>{self.__current_variable.get('name_variable')}</i>")
        # поле ввода
        self.ui.lineedit.setText(self.__pair.get("value_pair"))
        # описание
        description_variable = self.__current_variable.get('description_variable')
        if description_variable:
            self.ui.textbrowser.setHtml(description_variable)
        else:
            self.ui.textbrowser.hide()
        # connect
        self.ui.lineedit.textChanged.connect(lambda text: self.set_new_value_in_pair(text))

    def set_new_value_in_pair(self, new_value):
        self.__pair["value_pair"] = new_value