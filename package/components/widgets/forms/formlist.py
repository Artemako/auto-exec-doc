from PySide6.QtWidgets import QWidget, QDialog

import package.ui.formlist_ui as formlist_ui
import package.components.widgets.forms.formlistdialogwindow as formlistdialogwindow


class FormList(QWidget):
    def __init__(self, osbm, pair, current_variable):
        self.__osbm = osbm
        self.__pair = pair
        self.__current_variable = current_variable
        self.__osbm.obj_logg.debug_logger(
            f"FormList(pair, current_variable):\n pair = {pair}, \n current_variable = {current_variable}"
        )
        super(FormList, self).__init__()
        self.ui = formlist_ui.Ui_FormListWidget()
        self.ui.setupUi(self)
        # ИКОНКИ
        self.__icons = self.__osbm.obj_icons.get_icons()
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.config()
        #
        self.ui.btn_edittable.clicked.connect(self.btn_edittable_clicked)

    def btn_edittable_clicked(self):
        result = self.formlistdw()
        if result:
            data = self.__osbm.obj_formlistdw.get_data()
            print(f"obj_formlistdw data = {data}")
            self.set_new_value_in_pair(data)

    def config(self):
        # тип переменной
        qicon_type_variable = (
            self.__osbm.obj_comwith.variable_types.get_icon_by_type_variable(
                self.__current_variable.get("type_variable")
            )
        )
        self.ui.label_typevariable.setPixmap(qicon_type_variable)
        # заголовок + перменная
        self.ui.title.setText(self.__current_variable.get("title_variable"))
        self.ui.label_variable.setText(
            f"<i>{self.__current_variable.get('name_variable')}</i>"
        )
        # описание
        description_variable = self.__current_variable.get("description_variable")
        if description_variable:
            self.ui.textbrowser.setHtml(description_variable)
        else:
            self.ui.textbrowser.hide()

    def formlistdw(self) -> bool:
        self.__osbm.obj_logg.debug_logger("FormList formlistdw()")
        self.__osbm.obj_formlistdw = formlistdialogwindow.FormListDialogWindow(
            self.__osbm, self.__current_variable, self.__pair.get("value_pair")
        )
        result = self.__osbm.obj_formlistdw.exec_()
        return result == QDialog.Accepted

    def set_new_value_in_pair(self, new_value):
        self.__osbm.obj_logg.debug_logger(
            f"FormList set_new_value_in_pair(new_value):\nnew_value = {new_value}"
        )
        self.__pair["value_pair"] = new_value
        print(self.__pair)
