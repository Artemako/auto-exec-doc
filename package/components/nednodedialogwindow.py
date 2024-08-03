from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QTimer, QSize
from PySide6.QtGui import QIcon

import package.ui.nednodedialogwindow_ui as nednodedialogwindow_ui

import copy

import resources_rc

# TODO ПОДУМАТЬ ПРО PDF 

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
        self.__data = []
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
        # сортирока
        nodes.sort(key=lambda node: int(node.get("order_node")))
        self.__obs_manager.obj_l.debug_logger(
            f"NedNodeDialogWindow get_project_and_group_nodes nodes = {nodes}"
        )
        return nodes

    def config_maindata(self):
        self.__obs_manager.obj_l.debug_logger("NedNodeDialogWindow config_maindata()")
        if self.__type_window == "create":
            if self.__type_node == "FORM":
                self.ui.namenode.setText("Название формы")
                self.ui.btn_nestag.setText("Добавить форму")
            elif self.__type_node == "GROUP":
                self.ui.namenode.setText("Название группы")
                self.ui.btn_nestag.setText("Добавить группу")
        elif self.__type_window == "edit":
            if self.__type_node == "FORM":
                self.ui.namenode.setText("Название формы")
            elif self.__type_node == "GROUP":
                self.ui.namenode.setText("Название группы")
            self.ui.btn_nestag.setText("Сохранить")
            # заполняем форму
            self.ui.lineedit_namenode.setText(self.__node.get("name_node"))

    def config_placementdata(self):
        self.__obs_manager.obj_l.debug_logger("NedNodeDialogWindow config_placementdata()")
        # заполняем combobox'ы
        if self.__type_window == "create":
            self.fill_combox_parent()
            self.fill_combox_neighboor()
        elif self.__type_window == "edit":
            self.fill_combox_parent()
            self.fill_combox_neighboor()

    def fill_combox_parent(self):
        self.__obs_manager.obj_l.debug_logger(
            "NedNodeDialogWindow fill_combox_parent()"
        )
        combobox = self.ui.combox_parent
        combobox.blockSignals(True)
        combobox.clear()
        current_index = 0
        project_and_group_nodes = self.get_project_and_group_nodes()
        for index, prgr_node in enumerate(project_and_group_nodes):
            combobox.addItem(prgr_node.get("name_node"), prgr_node)
            print(f"prgr_node = {prgr_node}")
            print(f"self.__node = {self.__node}")
            if self.__node:
                if prgr_node.get("id_node") == self.__node.get("id_parent"):
                    current_index = index
                    print('TRUE prgr_node.get("id_node") == self.__node.get("id_parent")')
                    print(f"current_index = {index}")
        combobox.setCurrentIndex(current_index)
        combobox.blockSignals(False)

    def get_childs(self, parent_node):
        self.__obs_manager.obj_l.debug_logger(
            f"NedNodeDialogWindow get_childs(parent_node):\nparent_node = {parent_node}"
        )
        # сортировка была сделана при получении данных с БД
        childs = list(
            filter(
                lambda node: node.get("id_parent") == parent_node.get("id_node"),
                self.__nodes,
            )
        )
        # сортировка тут нужна из-за reconfig()
        childs.sort(key=lambda node: int(node.get("order_node")))

        self.__obs_manager.obj_l.debug_logger(
            f"NedNodeDialogWindow get_childs(parent_node):\nparent_node = {parent_node}\nchilds = {childs}"
        )
        return childs

    def fill_combox_neighboor(self):
        self.__obs_manager.obj_l.debug_logger("NedNodeDialogWindow combox_neighboor()")
        combobox = self.ui.combox_neighboor
        combobox.blockSignals(True)
        combobox.clear()
        current_index = 0
        parent_node = self.ui.combox_parent.currentData()
        combobox.addItem("- В начало -", "start")
        childs_nodes = self.get_childs(parent_node)
        if self.__type_window == "create":
            for index, child_node in enumerate(childs_nodes):
                combobox.addItem("После " + child_node.get("name_node"), child_node)
        else:
            for index, child_node in enumerate(childs_nodes):
                if self.__node.get("id_node") != child_node.get("id_node"):
                    combobox.addItem("После " + child_node.get("name_node"), child_node)
                else:
                    current_index = index
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
        self.accept()

    def save_edit_node(self):
        self.__obs_manager.obj_l.debug_logger("NedNodeDialogWindow save_edit_node()")
        self.__data = []
        self.edit_data_old_group()
        self.edit_data_new_group()

    def edit_data_old_group(self):
        self.__obs_manager.obj_l.debug_logger(
            "NedNodeDialogWindow edit_data_old_group()"
        )
        # подготовка данных
        flag_old = False
        # обертка для функции
        old_parent_node = {
            "id_node": self.__node.get("id_parent"),
            "type_node": "WRAPPER",
        }
        old_childs_nodes = self.get_childs(old_parent_node)
        # цикл по старой группе
        for index, child_node in enumerate(old_childs_nodes):
            if flag_old:
                child_node["order_node"] = index - 1
                self.__data.append(child_node)
            elif child_node.get("id_node") == self.__node.get("id_node"):
                # убрать main из старой группы
                flag_old = True
                child_node["id_parent"] = -1

    def edit_data_new_group(self):
        self.__obs_manager.obj_l.debug_logger(
            "NedNodeDialogWindow edit_data_new_group()"
        )
        # подготовка данных
        parent_node = self.ui.combox_parent.currentData()
        childs_nodes = self.get_childs(parent_node)
        # найти соседа в новой группе
        neighboor_index = int()
        neighboor_node = self.ui.combox_neighboor.currentData()
        if neighboor_node == "start":
            neighboor_index = -1
        else:
            neighboor_index = int(neighboor_node.get("order_node"))
        # цикл по новой группе
        print(f"neighboor_index = {neighboor_index}")
        for index, child_node in enumerate(childs_nodes):
            print(f"index, child_node = {index}, {child_node}")
            if neighboor_index < index:
                child_node["order_node"] = index + 1
                # print("child_node = ", child_node)
                self.__data.append(child_node)
        # выставляем новые значения для __node
        self.__node["order_node"] = neighboor_index + 1
        self.__node["id_parent"] = parent_node.get("id_node")
        self.__node["name_node"] = self.ui.lineedit_namenode.text()
        print(f"УРА self.__node = {self.__node}")
        print(f"УРА parent_node = {parent_node}")
        self.__data.append(self.__node)
        print(f"self.__data = {self.__data}")

    def add_new_node(self):
        self.__obs_manager.obj_l.debug_logger("NedNodeDialogWindow add_new_node()")
        # подготовка данных
        self.__node = {
            "id_active_template": None,
            "id_node": -1,
            "id_parent": None,
            "included": 1,
            "name_node": None,
            "order_node": None,
            "type_node": self.__type_node,
        }
        # 
        self.__data = []
        self.edit_data_new_group()
        print("DATA")
        for item in self.__data:
            print(sorted(item.items()))
