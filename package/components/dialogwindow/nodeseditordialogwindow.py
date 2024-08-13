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

import package.components.dialogwindow.nednodedialogwindow as nednodedialogwindow

import resources_rc

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
        self.reconfig()
        #
        self.connecting_actions()
   

    def reconfig(self):
        self.__obs_manager.obj_l.debug_logger("NodesEditorDialogWindow reconfig()")
        #
        self.__nodes_to_items = dict()
        # очистка tw_nodes
        self.ui.tw_nodes.blockSignals(True)
        self.ui.tw_nodes.clear()
        self.ui.tw_nodes.setHeaderLabels(["Проект"])     
        # заполнения вершинами
        self.__nodes = self.__obs_manager.obj_pd.get_nodes()
        print(f"NodesEditorDialogWindow self.__nodes = {self.__nodes}")
        # запуск
        project_node = self.find_project_node()
        self.dfs(project_node)
        # включение сигналов
        self.ui.tw_nodes.expandAll()   
        self.ui.tw_nodes.blockSignals(False)

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
        childs.sort(key=lambda node: int(node.get("order_node")))
        
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
            item = QTreeWidgetItem(tree_widget)
            item.setData(0, Qt.UserRole, node)
        else:
            item = QTreeWidgetItem(self.__nodes_to_items[node.get("id_parent")])
            item.setData(0, Qt.UserRole, node)
        item.setText(0, self.get_text_by_node(node))
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

    def update_edit_nodes(self):
        self.__obs_manager.obj_l.debug_logger(
            "NodesEditorDialogWindow update_bd()"
        )
        edit_nodes = self.__obs_manager.obj_nedndw.get_data()
        # for edit_node in edit_nodes:
        #     print(f"-> edit_node = {edit_node}")
        for edit_node in edit_nodes:
            id_node = edit_node.get("id_node")
            if id_node == -1:
                # print(f"ADD, edit_node = {edit_node}")
                self.__obs_manager.obj_pd.add_node(edit_node)
            else:
                # update данные по id
                # print(f"UPDATE, edit_node = {edit_node}")
                self.__obs_manager.obj_pd.update_node(edit_node)

    def edit_current(self):
        self.__obs_manager.obj_l.debug_logger(
            "NodesEditorDialogWindow edit_current()"
        )
        tree_widget = self.ui.tw_nodes
        current_item = tree_widget.currentItem()
        if current_item is not None:
            node = current_item.data(0, Qt.UserRole)
            result = self.ned_node_dw("edit", node.get("type_node"), node)
            if result:
                # обновление данных в БД
                self.update_edit_nodes()
                # перерисовка
                self.reconfig()
        else:
            self.__obs_manager.obj_dw.warning_message("Выберите элемент для редактирования!")

    def delete_item(self):
        tree_widget = self.ui.tw_nodes
        current_item = tree_widget.currentItem()
        if current_item is not None:
            node = current_item.data(0, Qt.UserRole)
            type_node = node.get("type_node")
            name_node = node.get("name_node")
            result = self.__obs_manager.obj_dw.question_message(f"Вы точно хотите удалить {name_node}?")
            if result:
                if type_node == "GROUP":
                    self.delete_group_node(node)
                else:
                    self.__obs_manager.obj_pd.delete_node(node)
                self.reconfig()
                print("УДАЛЕНИЕ")
        else:
            self.__obs_manager.obj_dw.warning_message("Выберите элемент для удаления!")

    def delete_group_node(self, node):
        self.__obs_manager.obj_l.debug_logger(
            f"NodesEditorDialogWindow delete_group_node(node):\nnode = {node}"
        )

        childs = self.get_childs(node)
        if childs:
            # переопределяем родительскую вершину для дочерних вершин
            for child in childs:
                self.__obs_manager.obj_pd.set_new_parent_for_child_node(node, child)
            # удаляем вершину из БД
            self.__obs_manager.obj_pd.delete_node(node)
            # перевыставляем order_node соседям вершины
            parent_node = self.__obs_manager.obj_pd.get_node_parent(node)
            parent_childs = self.__obs_manager.obj_pd.get_childs(parent_node)
            if parent_childs:
                for index, parent_child in enumerate(parent_childs):
                    self.__obs_manager.obj_pd.set_order_for_node(parent_child, index)
        else:
            self.__obs_manager.obj_pd.delete_node(node) 
        


    def add_group(self):
        self.__obs_manager.obj_l.debug_logger("NodesEditorDialogWindow add_group()")
        tree_widget = self.ui.tw_nodes
        current_item = tree_widget.currentItem()
        result = False
        if current_item is not None:
            node = current_item.data(0, Qt.UserRole)
            result = self.ned_node_dw("create", "GROUP", node)
        else:
            result = self.ned_node_dw("create", "GROUP")
        if result:
            # обновление данных в БД
            self.update_edit_nodes()
            # перерисовка
            self.reconfig()

    def add_form(self):
        self.__obs_manager.obj_l.debug_logger("NodesEditorDialogWindow add_form()")
        tree_widget = self.ui.tw_nodes
        current_item = tree_widget.currentItem()
        result = False
        if current_item is not None:
            node = current_item.data(0, Qt.UserRole)
            result = self.ned_node_dw("create", "FORM", node)
        else:
            result = self.ned_node_dw("create", "FORM")
        if result:
            # обновление данных в БД
            self.update_edit_nodes()
            # перерисовка
            self.reconfig()

    def ned_node_dw(self, type_window, type_node, node=None) -> bool:
        self.__obs_manager.obj_l.debug_logger(
            "NodesEditorDialogWindow ned_node_dw()"
        )
        self.__obs_manager.obj_nedndw = nednodedialogwindow.NedNodeDialogWindow(
            self.__obs_manager, type_window, type_node, self.__nodes, node
        )
        result = self.__obs_manager.obj_nedndw.exec()
        return result == QDialog.Accepted
            


        
