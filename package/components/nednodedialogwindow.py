from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QTimer, QSize
from PySide6.QtGui import QIcon

import package.ui.nednodedialogwindow_ui as nednodedialogwindow_ui

import resources_rc


class NedNodeDialogWindow(QDialog):
    def __init__(self, obs_manager, type_window, type_node, nodes, node=None):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger(
            f"NedNodeDialogWindow __init__(obs_manager, type_window, type_node, nodes, node):\ntype_window = {type_window}\ntype_node = {type_node}\nnodes = {nodes}\nnode = {node}"
        )
        self.__type_window = type_window
        self.__type_node = type_node
        self.__nodes = nodes
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
        self.config_placementdata()
        self.connecting_actions()

    def get_data(self):
        self.__obs_manager.obj_l.debug_logger(
            f"NedNodeDialogWindow get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def get_project_and_group_nodes(self) -> list:
        nodes = []
        for node in self.__nodes:
            if node.get("type_node") == "PROJECT" or node.get("type_node") == "GROUP":
                nodes.append(node)
        self.__obs_manager.obj_l.debug_logger(f"NedNodeDialogWindow get_project_and_group_nodes nodes = {nodes}")
        return nodes

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

    def config_placementdata(self):
        # TODO
        # заполняем combobox'ы
        if self.__type_window == "create":
            self.fill_combox_parent(False)
            self.fill_combox_neighboor(False)
        elif self.__type_window == "edit":
            self.fill_combox_parent(True)
            self.fill_combox_neighboor(True)
        
    def fill_combox_parent(self, is_edit = False):
        self.__obs_manager.obj_l.debug_logger("NedNodeDialogWindow fill_combox_parent()")
        combobox = self.ui.combox_parent
        combobox.blockSignals(True)
        combobox.clear()
        current_index = 0
        project_and_group_nodes = self.get_project_and_group_nodes()
        for index, node in enumerate(project_and_group_nodes):
            combobox.addItem(node.get("name_node"), node)
            if is_edit and node.get("id_node") == self.__node.get("id_parent"):
                current_index = index
        combobox.setCurrentIndex(current_index)
        combobox.blockSignals(False)

    def get_childs(self, parent_node):
        childs = list(
            filter(lambda node: node.get("id_parent") == parent_node.get("id_node"), self.__nodes)
        )
        self.__obs_manager.obj_l.debug_logger(
            f"NedNodeDialogWindow get_childs(parent_node):\nparent_node = {parent_node}\nchilds = {childs}"
        )
        return childs

    def fill_combox_neighboor(self, is_edit = False):
        self.__obs_manager.obj_l.debug_logger("NedNodeDialogWindow combox_neighboor()")
        combobox = self.ui.combox_neighboor
        combobox.blockSignals(True)
        combobox.clear()
        current_index = 0
        parent_node = self.ui.combox_parent.currentData()
        combobox.addItem("- В начало -", "start")
        childs_nodes = self.get_childs(parent_node)
        for index, child_node in enumerate(childs_nodes):
            if self.__node.get("id_node") != child_node.get("id_node"): 
                combobox.addItem("После " + child_node.get("name_node"), child_node)
                print("СЮДА")
            else:
                current_index = index
                print("ТУДА", current_index)
        combobox.setCurrentIndex(current_index)
        combobox.blockSignals(False)

    def connecting_actions(self):
        self.ui.btn_nestag.clicked.connect(self.action_nestag)
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.combox_parent.currentIndexChanged.connect(self.fill_combox_neighboor)

    def action_nestag(self):
        self.__obs_manager.obj_l.debug_logger("NedNodeDialogWindow action_nestag()")
        if self.__type_window == "create":
            self.add_new_node()
        elif self.__type_window == "edit":
            self.save_edit_node()
        self.close()

    def save_edit_node(self):
        self.__obs_manager.obj_l.debug_logger("NedNodeDialogWindow save_edit_node()")
        self.__data["name_node"] = self.ui.namenode.text()

    def add_new_node(self):
        self.__obs_manager.obj_l.debug_logger("NedNodeDialogWindow add_new_node()")
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
