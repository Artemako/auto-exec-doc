from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QSizePolicy

import package.ui.customitemqlistwidget_ui as customitemqlistwidget_ui


class CustomItemQListWidget(QWidget):
    def __init__(self, obs_manager, type_window, data):
        self.__obs_manager = obs_manager
        self.__type_window = type_window
        self.__data = data
        self.__obs_manager.obj_l.debug_logger(
            f"CustomItemQListWidget __init__(obs_manager, data):\nobs_manager = {obs_manager}\ntype_window = {type_window}\ndata = {data}"
        )
        super(CustomItemQListWidget, self).__init__()
        self.ui = customitemqlistwidget_ui.Ui_CustomItemQListWidget()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__obs_manager.obj_style.set_style_for(self)
        # конфигурация
        self.config()
        # # подключаем деействия
        # self.connecting_actions()

    def config(self):
        if self.__type_window == "TEMPLATE":
            self.ui.label_text.setText(self.__data.get("name_template"))
        elif self.__type_window == "PAGE":
            self.ui.label_text.setText(self.__data.get("name_page"))

    def get_btn_edit(self):
        self.__obs_manager.obj_l.debug_logger("CustomItemQListWidget get_btn_edit()")
        return self.ui.btn_edit

    def get_btn_delete(self):
        self.__obs_manager.obj_l.debug_logger("CustomItemQListWidget get_btn_delete()")
        return self.ui.btn_delete

    def get_type_window(self):
        self.__obs_manager.obj_l.debug_logger(
            f"CustomItemQListWidget get_type_window():\nself.__type_window = {self.__type_window}"
        )
        return self.__type_window

    def get_data(self):
        self.__obs_manager.obj_l.debug_logger(
            f"CustomItemQListWidget get_data():\nself.__data = {self.__data}"
        )
        return self.__data
