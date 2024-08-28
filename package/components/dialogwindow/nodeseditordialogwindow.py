from PySide6.QtWidgets import QDialog, QTreeWidgetItem
from PySide6.QtCore import Qt

import package.ui.nodeseditordialogwindow_ui as nodeseditordialogwindow_ui

import package.components.dialogwindow.neddw.nednodedialogwindow as nednodedialogwindow


class NodesEditorDialogWindow(QDialog):
    def __init__(self, osbm, open_node):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger(
            f"NodesEditorDialogWindow __init__(osbm, open_node): \nopen_node = {open_node}"
        )
        super(NodesEditorDialogWindow, self).__init__()
        self.ui = nodeseditordialogwindow_ui.Ui_NodesEditorDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        self.__icons = self.__osbm.obj_icons.get_icons()
        self.setWindowIcon(self.__icons.get("logo"))
        #
        self.config()
        self.reconfig(open_node)
        #
        self.connecting_actions()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Игнорируем нажатие Enter
            event.ignore()
        else:
            super().keyPressEvent(event)

    def config(self):
        self.__osbm.obj_logg.debug_logger("NodesEditorDialogWindow config()")
        # свернуть/развернуть окно
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    def reconfig(self, open_node=None):
        self.__osbm.obj_logg.debug_logger("NodesEditorDialogWindow reconfig()")
        #
        tree_widget = self.ui.tw_nodes
        self.__nodes_to_items = dict()
        self.__open_node_flag = False
        # очистка tw_nodes
        tree_widget.blockSignals(True)
        tree_widget.clear()
        tree_widget.setHeaderLabels(["Проект"])
        # заполнения вершинами
        self.__nodes = self.__osbm.obj_prodb.get_nodes()
        print(f"NodesEditorDialogWindow self.__nodes = {self.__nodes}")
        # запуск
        project_node = self.find_project_node()
        self.dfs(project_node, open_node)
        #
        if tree_widget.topLevelItemCount() > 0 and not self.__open_node_flag:
            tree_widget.setCurrentItem(tree_widget.topLevelItem(0))
        # включение сигналов
        tree_widget.expandAll()
        tree_widget.blockSignals(False)

    def find_project_node(self):
        self.__osbm.obj_logg.debug_logger("NodesEditorDialogWindow find_project_node()")
        for node in self.__nodes:
            if node.get("type_node") == "PROJECT":
                return node
        return None

    def set_text_and_icon_for_item_by_node(self, item, node):
        self.__osbm.obj_logg.debug_logger(
            f"NodesEditorDialogWindow get_text_by_node(item, node):\nitem = {item},\nnode = {node}"
        )
        # иконки
        if node.get("type_node") == "FORM":
            icon = self.__icons.get("form")
            icon = item.setIcon(0, icon)
        elif node.get("type_node") == "GROUP":
            icon = self.__icons.get("group")
            icon = item.setIcon(0, icon)
        # текст
        text = node.get("name_node")
        item.setText(0, text)

    def dfs(self, parent_node, open_node=None):
        """
        АНАЛОГ (почти). Проход по всем вершинам.
        """
        self.__osbm.obj_logg.debug_logger(
            f"NodesEditorDialogWindow dfs(parent_node, open_node):\nparent_node = {parent_node}\nopen_node = {open_node}"
        )
        childs = self.get_childs(parent_node)
        if childs:
            for child in childs:
                # действие
                self.set_item_in_nodes_to_items(child, open_node)
                # проход по дочерним вершинам
                self.dfs(child, open_node)

    def get_childs(self, parent_node):
        childs = list(
            filter(
                lambda node: node.get("id_parent") == parent_node.get("id_node"),
                self.__nodes,
            )
        )
        childs.sort(key=lambda node: int(node.get("order_node")))

        self.__osbm.obj_logg.debug_logger(
            f"NodesEditorDialogWindow get_childs(parent_node):\nparent_node = {parent_node}\nchilds = {childs}"
        )
        return childs

    def set_item_in_nodes_to_items(self, node, open_node=None):
        """
        АНАЛОГ. Поставить item в nodes_to_items.
        """
        self.__osbm.obj_logg.debug_logger(
            f"NodesEditorDialogWindow set_item_in_nodes_to_items(node):\nnode = {node}\nopen_node = {open_node}"
        )
        tree_widget = self.ui.tw_nodes
        item = None
        if node.get("id_parent") == 0:
            item = QTreeWidgetItem(tree_widget)
            item.setData(0, Qt.UserRole, node)
        else:
            item = QTreeWidgetItem(self.__nodes_to_items[node.get("id_parent")])
            item.setData(0, Qt.UserRole, node)
        self.set_text_and_icon_for_item_by_node(item, node)
        self.__nodes_to_items[node.get("id_node")] = item
        # Выбор
        if open_node and node.get("id_node") == open_node.get("id_node"):
            tree_widget.setCurrentItem(item)
            self.__open_node_flag = True

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("NodesEditorDialogWindow config_actions()")
        self.ui.btn_add_form.clicked.connect(self.add_form)
        self.ui.btn_add_form.setShortcut("Ctrl+F")
        self.ui.btn_add_group.clicked.connect(self.add_group)
        self.ui.btn_add_group.setShortcut("Ctrl+G")
        self.ui.btn_delete_item.clicked.connect(self.delete_item)
        self.ui.btn_delete_item.setShortcut("Ctrl+D")
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")
        self.ui.btn_edit.clicked.connect(self.edit_current)
        self.ui.btn_edit.setShortcut("Ctrl+E")

    def update_edit_nodes(self):
        self.__osbm.obj_logg.debug_logger("NodesEditorDialogWindow update_bd()")
        edit_nodes = self.__osbm.obj_nedndw.get_data()
        # for edit_node in edit_nodes:
        #     print(f"-> edit_node = {edit_node}")
        for edit_node in edit_nodes:
            if edit_node != "WRAPPER":
                id_node = edit_node.get("id_node")
                if id_node == -111:
                    # print(f"ADD, edit_node = {edit_node}")
                    self.__osbm.obj_prodb.add_node(edit_node)
                else:
                    # update данные по id
                    # print(f"UPDATE, edit_node = {edit_node}")
                    self.__osbm.obj_prodb.update_node(edit_node)

    def edit_current(self):
        self.__osbm.obj_logg.debug_logger("NodesEditorDialogWindow edit_current()")
        tree_widget = self.ui.tw_nodes
        current_item = tree_widget.currentItem()
        if current_item is not None:
            node = current_item.data(0, Qt.UserRole)
            result = self.ned_node_dw("edit", node.get("type_node"), node)
            if result:
                # обновление данных в БД
                self.update_edit_nodes()
                # перерисовка
                self.reconfig(node)
        else:
            self.__osbm.obj_dw.warning_message("Выберите элемент для редактирования!")

    def delete_item(self):
        tree_widget = self.ui.tw_nodes
        current_item = tree_widget.currentItem()
        if current_item is not None:
            node = current_item.data(0, Qt.UserRole)
            type_node = node.get("type_node")
            name_node = node.get("name_node")
            result = self.__osbm.obj_dw.question_message(
                f'Вы действительно хотите удалить:\n"{name_node}"?'
            )
            if result:
                if type_node == "GROUP":
                    self.delete_group_node(node)
                else:
                    self.__osbm.obj_prodb.delete_node(node)
                self.reconfig(node)
                print("УДАЛЕНИЕ")
        else:
            self.__osbm.obj_dw.warning_message("Выберите элемент для удаления!")

    def delete_group_node(self, node):
        self.__osbm.obj_logg.debug_logger(
            f"NodesEditorDialogWindow delete_group_node(node):\nnode = {node}"
        )

        childs = self.get_childs(node)
        if childs:
            # переопределяем родительскую вершину для дочерних вершин
            for child in childs:
                self.__osbm.obj_prodb.set_new_parent_for_child_node(node, child)
            # удаляем вершину из БД
            self.__osbm.obj_prodb.delete_node(node)
            # дети не должны удаляться так как не прописан для id_parent ON DELETE CASCADE
            # перевыставляем order_node соседям вершины
            parent_node = self.__osbm.obj_prodb.get_node_parent(node)
            parent_childs = self.__osbm.obj_prodb.get_childs(parent_node)
            if parent_childs:
                for index, parent_child in enumerate(parent_childs):
                    self.__osbm.obj_prodb.set_order_for_node(parent_child, index)
        else:
            self.__osbm.obj_prodb.delete_node(node)

    def add_group(self):
        self.__osbm.obj_logg.debug_logger("NodesEditorDialogWindow add_group()")
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
        self.__osbm.obj_logg.debug_logger("NodesEditorDialogWindow add_form()")
        tree_widget = self.ui.tw_nodes
        current_item = tree_widget.currentItem()
        result = False
        node = None
        if current_item is not None:
            node = current_item.data(0, Qt.UserRole)
            result = self.ned_node_dw("create", "FORM", node)
        else:
            result = self.ned_node_dw("create", "FORM")
        if result:
            # обновление данных в БД
            self.update_edit_nodes()
            # перерисовка
            self.reconfig(node)

    def ned_node_dw(self, type_window, type_node, node=None) -> bool:
        self.__osbm.obj_logg.debug_logger("NodesEditorDialogWindow ned_node_dw()")
        self.__osbm.obj_nedndw = nednodedialogwindow.NedNodeDialogWindow(
            self.__osbm, type_window, type_node, self.__nodes, node
        )
        result = self.__osbm.obj_nedndw.exec()
        return result == QDialog.Accepted
