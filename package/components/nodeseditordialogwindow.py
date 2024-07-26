from PySide6.QtWidgets import (QDialog, QWidget, QVBoxLayout, QPushButton, QTreeWidget, QTreeWidgetItem, QMessageBox)
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon

import package.ui.nodeseditordialogwindow_ui as nodeseditordialogwindow_ui

import resources_rc


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
        self.__obs_manager.obj_l.debug_logger(f"IN dfs(parent_node):\nparent_node = {parent_node}")
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
        self.__obs_manager.obj_l.debug_logger(f"IN set_item_in_nodes_to_items(node):\nnode = {node}")
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

    

    def add_group(self):
        self.__obs_manager.obj_l.debug_logger("IN add_group()")
        tree_widget = self.ui.tw_nodes
        current_item = tree_widget.currentItem()
        if current_item:
            self.add_item
        self.add_item_after_selected()

    def add_form(self):
        self.__obs_manager.obj_l.debug_logger("IN add_form()")
        tree_widget = self.ui.tw_nodes
        self.add_item_after_selected()

    def add_item_after_selected(self):
        self.__obs_manager.obj_l.debug_logger("IN add_item_after_selected()")
        tree_widget = self.ui.tw_nodes
        
    # TODO Сделать ВСЁ



        # if current_item:
        #     # Получаем родительский элемент текущего элемента
        #     parent_item = current_item.parent()
        #     if parent_item:  # Если текущий элемент не на верхнем уровне
        #         index = parent_item.indexOfChild(current_item)
        #         new_item = QTreeWidgetItem(parent_item, [f"Элемент после {current_item.text(0)}"])
        #         parent_item.insertChild(index + 1, new_item)  # Вставка после текущего элемента
        #     else:  # Если текущий элемент на верхнем уровне
        #         index = tree_widget.indexOfTopLevelItem(current_item)
        #         new_item = QTreeWidgetItem(tree_widget, [f"Элемент после {current_item.text(0)}"])
        #         tree_widget.insertTopLevelItem(index + 1, new_item)  # Вставка после текущего элемента
        # else:
        #     new_item = QTreeWidgetItem(tree_widget, "Элемент")
        #     tree_widget.insertTopLevelItem(0, new_item)  # Вставка после текущего элемента


    def delete_item(self):
        pass
    #     tree_widget = self.ui.tw_nodes
    #     current_item = tree_widget.currentItem()
    #     if current_item:
    #         index = tree_widget.indexOfTopLevelItem(current_item)
    #         if index != -1:  # Удаление группы
    #             tree_widget.takeTopLevelItem(index)
    #         else:  # Удаление элемента
    #             parent_item = current_item.parent()
    #             if parent_item:
    #                 parent_item.removeChild(current_item)
    #     else:
    #         print(self, "Ошибка", "Сначала выберите элемент или группу.")

    # def move_up(self):
    #     tree_widget = self.ui.tw_nodes
    #     current_item = tree_widget.currentItem()
    #     if current_item:
    #         index = tree_widget.indexOfTopLevelItem(current_item)
    #         if index > 0:  # Перемещение группы вверх
    #             tree_widget.insertTopLevelItem(
    #                 index - 1, tree_widget.takeTopLevelItem(index)
    #             )
    #         else:
    #             parent_item = current_item.parent()
    #             if parent_item:
    #                 parent_index = parent_item.indexOfChild(current_item)
    #                 if parent_index > 0:
    #                     parent_item.insertChild(
    #                         parent_index - 1, parent_item.takeChild(parent_index)
    #                     )

    # def move_down(self):
    #     tree_widget = self.ui.tw_nodes
    #     current_item = tree_widget.currentItem()
    #     if current_item:
    #         index = tree_widget.indexOfTopLevelItem(current_item)
    #         if (
    #             index < tree_widget.topLevelItemCount() - 1
    #         ):  # Перемещение группы вниз
    #             tree_widget.insertTopLevelItem(
    #                 index + 1, tree_widget.takeTopLevelItem(index)
    #             )
    #         else:
    #             parent_item = current_item.parent()
    #             if parent_item:
    #                 parent_index = parent_item.indexOfChild(current_item)
    #                 if parent_index < parent_item.childCount() - 1:
    #                     parent_item.insertChild(
    #                         parent_index + 1, parent_item.takeChild(parent_index)
    #                     )
