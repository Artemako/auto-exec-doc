from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt

class StructureExecDoc:
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__treewidget_structure_execdoc = None
        self.__title_sed = None
        self.__nodes_to_items = dict()

    def connect_structureexecdoc(self, tr_sed, title_sed):
        """
        Подключить tr_sed к контроллеру.
        """
        self.__obs_manager.obj_l.debug_logger("IN connect_structureexecdoc(tr_sed, title_sed)")
        self.__treewidget_structure_execdoc = tr_sed
        self.__title_sed = title_sed
        # Очистить при запуске
        self.clear_sed()

        # Подключение сигналов
        self.__treewidget_structure_execdoc.currentItemChanged.connect(
            lambda current: self.__obs_manager.obj_pt.update_pages_template(
                current.data(0, Qt.UserRole)
            )
        )
        self.__treewidget_structure_execdoc.itemChanged.connect(
            lambda item: self.item_changed(item)
        )

    def item_changed(self, item):
        node = item.data(0, Qt.UserRole)
        state = int(item.checkState(0) == Qt.Checked)
        self.set_state_included_for_child(node, item.checkState(0) == Qt.Checked)
        self.__obs_manager.obj_pd.set_included_for_node(node, state)

    def clear_sed(self):
        """
        Очистить дерево
        """
        self.__obs_manager.obj_l.debug_logger("IN clear_tr_sed()")
        self.__treewidget_structure_execdoc.clear()
        self.__treewidget_structure_execdoc.setHeaderLabels([""])
        self.__title_sed.setText("Проект не выбран")

    def update_structure_exec_doc(self):
        """
        Создает структуру дерева ИД
        """
        self.__obs_manager.obj_l.debug_logger("IN update_structure_exec_doc()")
        # очистка
        self.clear_sed()
        # Задать название столбца
        title = f"{self.__obs_manager.obj_p.get_current_name()}"
        self.__treewidget_structure_execdoc.setHeaderLabels(["Проект"])
        self.__title_sed.setText(title)
        # проход по вершинам
        self.dfs(self.__obs_manager.obj_pd.get_project_node())

    def dfs(self, parent_node):
        """
        Проход по всем вершинам.
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
        Поставить item в nodes_to_items.
        """
        self.__obs_manager.obj_l.debug_logger(f"IN set_item_in_nodes_to_items(node):\nnode = {node}")
        tree_widget = self.__treewidget_structure_execdoc
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


# obj_sed = StructureExecDoc()
