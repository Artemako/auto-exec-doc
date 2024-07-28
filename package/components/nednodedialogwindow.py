from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QTimer, QSize
from PySide6.QtGui import QIcon

import package.ui.nednodedialogwindow_ui as nednodedialogwindow_ui

import resources_rc


class NedNodeDialogWindow(QDialog):
    def __init__(self, obs_manager, type_window, type_node, node=None):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger(
            f"IN NedNodeDialogWindow(obs_manager, type_window):\ntype_window = {type_window}"
        )
        self.__type_window = type_window
        self.__type_node = type_node
        self.__node = node
        super(NedNodeDialogWindow, self).__init__()
        self.ui = nednodedialogwindow_ui.Ui_NedNodeDialogWindow()
        self.ui.setupUi(self)
        # 
        self.__data = {
            "id_active_template": None,
            "id_node": None,
            "id_parent": None,
            "included": None,
            "name_node": None,
            "order_node": None,
            "type_node": None,
        }
        # одноразовые действия
        self.config_maindata()
        self.connecting_actions()

    def get_data(self):
        self.__obs_manager.obj_l.debug_logger(
            f"get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def config_maindata(self):
        if self.__type_window == "create":
            if self.__type_node == "FORM":
                self.ui.namenode.setText("Название формы")
                self.ui.btn_nestag.setText("Добавить форму")
            elif self.__type_node == "GROUP":
                self.ui.namenode.setText("Название группы")
                self.ui.btn_nestag.setText("Добавить группу")
        elif self.__type_window == "edit":
            self.ui.namenode.setText(self.__node.get("name_node"))
            if self.__type_node == "FORM":
                self.ui.namenode.setText("Название формы")
            elif self.__type_node == "GROUP":
                self.ui.namenode.setText("Название группы")
            self.ui.btn_nestag.setText("Сохранить")

    def connecting_actions(self):
        self.ui.btn_nestag.clicked.connect(self.action_nestag)
        self.ui.btn_close.clicked.connect(self.close)

    def action_nestag(self):
        self.__obs_manager.obj_l.debug_logger("IN action_nestag()")
        if self.__type_window == "create":
            self.add_new_node()
        elif self.__type_window == "edit":
            self.save_edit_node()
        self.close()

    def save_edit_node(self):
        self.__obs_manager.obj_l.debug_logger("IN save_edit_node()")
        self.__data["name_node"] = self.ui.namenode.text()

    def add_new_node(self):
        self.__obs_manager.obj_l.debug_logger("IN add_new_node()")
        self.__data = {
            "id_active_template": None,
            "id_node": None,
            "id_parent": None,
            "included": None,
            "name_node": None,
            "order_node": None,
            "type_node": None,
        }
        self.__data["included"] = 1
        self.__data["name_node"] = self.ui.namenode.text()
        self.__data["type_node"] = self.__type_node
