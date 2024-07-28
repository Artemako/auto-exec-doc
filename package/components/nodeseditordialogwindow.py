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
        self.__obs_manager.obj_l.debug_logger("IN NodesEditorDialogWindow(obs_manager)")
        super(NodesEditorDialogWindow, self).__init__()
        self.ui = nodeseditordialogwindow_ui.Ui_NodesEditorDialogWindow()
        self.ui.setupUi(self)
        #
        self.config()
        #
        self.connecting_actions()

    def config(self):
        #
        self.__nodes_to_items = dict()
        # очистка tw_nodes
        self.ui.tw_nodes.clear()
        self.ui.tw_nodes.setHeaderLabels(["Проект"])
        self.ui.tw_nodes.expandAll()
        # запуск заполнения
        self.dfs(self.__obs_manager.obj_pd.get_project_node())

    def dfs(self, parent_node):
        """
        АНАЛОГ. Проход по всем вершинам.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"IN dfs(parent_node):\nparent_node = {parent_node}"
        )
        childs = self.__obs_manager.obj_pd.get_childs(parent_node)
        if childs:
            for child in childs:
                # действие
                self.set_item_in_nodes_to_items(child)
                # проход по дочерним вершинам
                self.dfs(child)

    def set_item_in_nodes_to_items(self, node):
        """
        АНАЛОГ. Поставить item в nodes_to_items.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"IN set_item_in_nodes_to_items(node):\nnode = {node}"
        )
        tree_widget = self.ui.tw_nodes
        item = None
        if node.get("id_parent") == 0:
            item = QTreeWidgetItem(tree_widget)
            item.setData(0, Qt.UserRole, node)
        else:
            item = QTreeWidgetItem(self.__nodes_to_items[node.get("id_parent")])
            item.setData(0, Qt.UserRole, node)
        item.setText(0, node.get("name_node"))
        # С галочкой по умолчанию
        item.setCheckState(0, Qt.Checked)
        self.__nodes_to_items[node.get("id_node")] = item

    def set_state_included_for_child(self, node, state):
        """
        АНАЛОГ
        """
        self.__obs_manager.obj_l.debug_logger(
            f"""IN set_state_included_for_childs(node, state):\nid_node = {node.get("id_node")},\nstate = {state}"""
        )
        item = self.__nodes_to_items.get(node.get("id_node"))
        if item:
            item.setCheckState(0, Qt.Checked if state else Qt.Unchecked)
            childs = self.__obs_manager.obj_pd.get_childs(node)
            if childs:
                for child in childs:
                    self.set_state_included_for_child(child, state)

    def connecting_actions(self):
        self.__obs_manager.obj_l.debug_logger("IN config_actions()")
        self.ui.btn_add_form.clicked.connect(self.add_form)
        self.ui.btn_add_group.clicked.connect(self.add_group)
        self.ui.btn_delete_item.clicked.connect(self.delete_item)
        self.ui.btn_close.clicked.connect(self.close)
        # TODO верх вниз + изменить названия

    def add_group(self):
        self.__obs_manager.obj_l.debug_logger("IN add_group()")
        # откртыь диалоговое окно
        new_node = self.ned_node_dw("create", "GROUP")
        # добавление 
        tree_widget = self.ui.tw_nodes
        current_item = tree_widget.currentItem()
        if current_item:
            self.add_item_after_selected("GROUP", new_node)
        else:
            self.add_item_to_end("GROUP", new_node)

    def add_form(self):
        self.__obs_manager.obj_l.debug_logger("IN add_form()")
        # откртыь диалоговое окно
        new_node = self.ned_node_dw("create", "GROUP")
        # добавление 
        tree_widget = self.ui.tw_nodes
        current_item = tree_widget.currentItem()
        if current_item:
            self.add_item_after_selected("FORM", new_node)
        else:
            self.add_item_to_end("FORM", new_node)

    def ned_node_dw(self, type_window, type_node, node=None) -> dict:
        self.__obs_manager.obj_l.debug_logger("IN ned_node_dw()")
        self.__obs_manager.obj_nedndw = nednodedialogwindow.NedNodeDialogWindow(
            self.__obs_manager, type_window, type_node, node
        )
        self.__obs_manager.obj_nedndw.exec()
        new_node = self.__obs_manager.obj_nedndw.get_data()
        print(f"new_node = {new_node}")
        return new_node

    def add_item_after_selected(self, node_type, new_node):
        """
        Добавление элемента после текущего выбранного элемента.
        """
        # TODO Проверить работоспособность (тут что-то не так)
        self.__obs_manager.obj_l.debug_logger(f"IN add_item_after_selected(node_type={node_type}, new_node={new_node})")
        tree_widget = self.ui.tw_nodes
        current_item = tree_widget.currentItem()
        parent_item = current_item.parent() if current_item.parent() else tree_widget
        new_item = QTreeWidgetItem(parent_item)
        new_item.setData(0, Qt.UserRole, new_node)
        new_item.setText(0, new_node.get("name_node"))
        new_item.setCheckState(0, Qt.Checked)
        # вставка после текущего элемента
        current_index = parent_item.indexOfChild(current_item)
        parent_item.insertChild(current_index + 1, new_item)
        # self.__nodes_to_items[new_node.get("id_node")] = new_item

    def add_item_to_end(self, node_type, new_node):
        """
        Добавление элемента в конец списка.
        """
        self.__obs_manager.obj_l.debug_logger(f"IN add_item_to_end(node_type={node_type}, new_node={new_node})")
        tree_widget = self.ui.tw_nodes
        # Если текущее значение None, добавляем в корень
        new_item = QTreeWidgetItem(tree_widget)
        new_item.setData(0, Qt.UserRole, new_node)
        new_item.setText(0, new_node.get("name_node"))
        new_item.setCheckState(0, Qt.Checked)
        # добавление в корень
        tree_widget.addTopLevelItem(new_item)
        # self.__nodes_to_items[new_node.get("id_node")] = new_item

    def delete_item(self):
        # TODO
        pass