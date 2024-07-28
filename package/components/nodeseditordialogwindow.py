from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QMessageBox,
)
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon

import package.ui.nodeseditordialogwindow_ui as nodeseditordialogwindow_ui

import package.components.nednodedialogwindow as nednodedialogwindow

import resources_rc

node = {
    "id_active_template": 1,
    "id_node": 10,
    "id_parent": 0,
    "included": 1,
    "name_node": "Титульный лист",
    "order_node": "1",
    "type_node": "FORM",
}


class NodesEditorDialogWindow(QDialog):
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger(
            "NodesEditorDialogWindow __init__(obs_manager)"
        )
        super(NodesEditorDialogWindow, self).__init__()
        self.ui = nodeseditordialogwindow_ui.Ui_NodesEditorDialogWindow()
        self.ui.setupUi(self)
        #
        self.config()
        #
        self.connecting_actions()

    def config(self):
        self.__obs_manager.obj_l.debug_logger("NodesEditorDialogWindow config()")
        #
        self.__nodes_to_items = dict()
        # очистка tw_nodes
        self.ui.tw_nodes.clear()
        self.ui.tw_nodes.setHeaderLabels(["Проект"])
        self.ui.tw_nodes.expandAll()
        # заполнения вершинами
        self.__nodes = self.__obs_manager.obj_pd.get_nodes()
        print(f"NodesEditorDialogWindow self.__nodes = {self.__nodes}")
        # запуск
        project_node = self.find_project_node()
        self.dfs(project_node)

    def find_project_node(self):
        self.__obs_manager.obj_l.debug_logger(
            "NodesEditorDialogWindow find_project_node()"
        )
        for node in self.__nodes:
            if node.get("type_node") == "PROJECT":
                return node
        return None

    def get_text_by_node(self, node):
        self.__obs_manager.obj_l.debug_logger(
            f"NodesEditorDialogWindow get_text_by_node(node):\nnode = {node}"
        )
        text = str()
        if node.get("type_node") == "FORM":
            text = "Ф: " + node.get("name_node")
        elif node.get("type_node") == "GROUP":
            text = "ГР: " + node.get("name_node")
        return text

    def dfs(self, parent_node):
        """
        АНАЛОГ (почти). Проход по всем вершинам.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"NodesEditorDialogWindow dfs(parent_node):\nparent_node = {parent_node}"
        )
        childs = self.get_childs(parent_node)
        if childs:
            for child in childs:
                # действие
                self.set_item_in_nodes_to_items(child)
                # проход по дочерним вершинам
                self.dfs(child)

    def get_childs(self, parent_node):
        childs = list(
            filter(
                lambda node: node.get("id_parent") == parent_node.get("id_node"),
                self.__nodes,
            )
        )
        self.__obs_manager.obj_l.debug_logger(
            f"NodesEditorDialogWindow get_childs(parent_node):\nparent_node = {parent_node}\nchilds = {childs}"
        )
        return childs

    def set_item_in_nodes_to_items(self, node):
        """
        АНАЛОГ. Поставить item в nodes_to_items.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"NodesEditorDialogWindow set_item_in_nodes_to_items(node):\nnode = {node}"
        )
        tree_widget = self.ui.tw_nodes
        item = None
        if node.get("id_parent") == 0:
            print("QTreeWidgetItem(tree_widget)")
            item = QTreeWidgetItem(tree_widget)
            item.setData(0, Qt.UserRole, node)
        else:
            print('QTreeWidgetItem(self.__nodes_to_items[node.get("id_parent")])')
            item = QTreeWidgetItem(self.__nodes_to_items[node.get("id_parent")])
            item.setData(0, Qt.UserRole, node)
        item.setText(0, self.get_text_by_node(node))
        # С галочкой по умолчанию
        item.setCheckState(0, Qt.Checked)
        self.__nodes_to_items[node.get("id_node")] = item

    def connecting_actions(self):
        self.__obs_manager.obj_l.debug_logger(
            "NodesEditorDialogWindow config_actions()"
        )
        self.ui.btn_add_form.clicked.connect(self.add_form)
        self.ui.btn_add_group.clicked.connect(self.add_group)
        self.ui.btn_delete_item.clicked.connect(self.delete_item)
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_edit.clicked.connect(self.edit_current)

    def edit_current(self):
        self.__obs_manager.obj_l.debug_logger(
            "NodesEditorDialogWindow edit_current()"
        )
        tree_widget = self.ui.tw_nodes
        # TODO ???
        current_item = tree_widget.currentItem()
        if current_item:
            node = current_item.data(0, Qt.UserRole)
            self.ned_node_dw("edit", node.get("type_node"), node)
            # TODO
        else:
            self.__obs_manager.obj_dw.warning_message("Выберите элемент для редактирования!")

    def add_group(self):
        self.__obs_manager.obj_l.debug_logger("NodesEditorDialogWindow add_group()")
        # откртыь диалоговое окно
        self.ned_node_dw("create", "GROUP")
        # new_node = self.__obs_manager.obj_nedndw.get_data()
        # добавление
        # TODO

    def add_form(self):
        self.__obs_manager.obj_l.debug_logger("NodesEditorDialogWindow add_form()")
        # откртыь диалоговое окно
        self.ned_node_dw("create", "FORM")
        # new_node = self.__obs_manager.obj_nedndw.get_data()
        # добавление
        # TODO

    def ned_node_dw(self, type_window, type_node, node=None):
        self.__obs_manager.obj_l.debug_logger(
            "NodesEditorDialogWindow ned_node_dw()"
        )
        self.__obs_manager.obj_nedndw = nednodedialogwindow.NedNodeDialogWindow(
            self.__obs_manager, type_window, type_node, self.__nodes, node
        )
        self.__obs_manager.obj_nedndw.exec()

    def delete_item(self):
        # TODO сделать удаление
        pass
