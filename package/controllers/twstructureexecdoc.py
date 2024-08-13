from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt


class TWStructureExecDoc:
    def __init__(self):
        self.__tw = None
        self.__title_sed = None
        self.__nodes_to_items = dict()
        self.__expanded_states = dict()

    def setting_all_obs_manager(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger(
            "TWStructureExecDoc setting_all_obs_manager()"
        )

    def connect_structureexecdoc(self, tr_sed, title_sed):
        """
        Подключить tr_sed к контроллеру.
        """
        self.__obs_manager.obj_l.debug_logger(
            "TWStructureExecDoc connect_structureexecdoc(tr_sed, title_sed)"
        )
        self.__tw = tr_sed
        self.__title_sed = title_sed
        # Очистить при запуске
        self.clear_sed()

        self.__tw.currentItemChanged.connect(
            lambda current: current and self.current_item_changed(current)
        )
        self.__tw.itemChanged.connect(lambda item: item and self.item_changed(item))
        # раскрытие/свертывание элементов
        self.__tw.itemExpanded.connect(self.on_item_expanded)
        self.__tw.itemCollapsed.connect(self.on_item_collapsed)

    def get_current_node(self):
        self.__obs_manager.obj_l.debug_logger("TWStructureExecDoc get_current_node()")
        current_item = self.__tw.currentItem()
        if current_item is None:
            return None
        else:
            return current_item.data(0, Qt.UserRole)

    def current_item_changed(self, current):
        self.__obs_manager.obj_l.debug_logger(
            f"TWStructureExecDoc current_item_changed(current):\ncurrent = {current}"
        )
        node = current.data(0, Qt.UserRole)
        # обновить combobox -> страницы
        self.__obs_manager.obj_comboxts.update_combox_templates(node)

    def item_changed(self, item):
        self.__obs_manager.obj_l.debug_logger(
            f"TWStructureExecDoc item_changed(item):\nitem = {item}"
        )
        if item is not None:
            self.__tw.blockSignals(True)
            node = item.data(0, Qt.UserRole)
            state = int(item.checkState(0) == Qt.Checked)
            self.set_state_included_for_child(node, item.checkState(0) == Qt.Checked)
            self.__obs_manager.obj_pd.set_included_for_node(node, state)
            self.__tw.blockSignals(False)

    def clear_sed(self):
        """
        Очистить дерево
        """
        self.__obs_manager.obj_l.debug_logger("TWStructureExecDoc clear_tr_sed()")
        self.__tw.blockSignals(True)
        self.__tw.clear()
        self.__tw.setHeaderLabels([""])
        self.__tw.blockSignals(False)
        self.__title_sed.setText("Проект не выбран")

    def update_structure_exec_doc(self):
        """
        Создает структуру дерева ИД
        """
        self.__obs_manager.obj_l.debug_logger(
            "TWStructureExecDoc update_structure_exec_doc()"
        )
        # очистка
        self.clear_sed()
        # Задать название столбца
        title = f"{self.__obs_manager.obj_sd.get_project_current_name()}"
        self.__tw.setHeaderLabels(["Проект"])
        self.__title_sed.setText(title)
        # проход по вершинам
        self.dfs(self.__obs_manager.obj_pd.get_project_node())

    def dfs(self, parent_node):
        """
        Проход по всем вершинам.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"TWStructureExecDoc dfs(parent_node):\nparent_node = {parent_node}"
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
        Поставить item в nodes_to_items.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"TWStructureExecDoc set_item_in_nodes_to_items(node):\nnode = {node}"
        )
        self.__tw.blockSignals(True)
        # добавляем вершину
        item = self.add_item_in_tree_widget(node)
        # текст в зависимости от типа
        self.set_text_for_item(item, node)
        # раскрытие вершины
        self.set_expanded_for_item(item, node)
        # С галочкой по умолчанию
        item.setCheckState(0, Qt.Checked)
        self.__nodes_to_items[node.get("id_node")] = item
        self.__tw.blockSignals(False)

    def add_item_in_tree_widget(self, node) -> object:
        self.__obs_manager.obj_l.debug_logger(
            f"TWStructureExecDoc add_item_in_tree_widget(node):\nnode = {node}"
        )
        item = None
        if node.get("id_parent") == 0:
            item = QTreeWidgetItem(self.__tw)
            item.setData(0, Qt.UserRole, node)
        else:
            item = QTreeWidgetItem(self.__nodes_to_items[node.get("id_parent")])
            item.setData(0, Qt.UserRole, node)
        return item

    def set_text_for_item(self, item, node):
        self.__obs_manager.obj_l.debug_logger(
            f"TWStructureExecDoc set_text_for_item(item, node):\nitem = {item},\nnode = {node}"
        )
        name_node = node.get("name_node")
        if node.get("type_node") == "FORM":
            item.setText(0, "Ф: " + name_node)
        elif node.get("type_node") == "GROUP":
            item.setText(0, "ГР: " + name_node)
        else:
            item.setText(0, name_node)

    def set_expanded_for_item(self, item, node):
        self.__obs_manager.obj_l.debug_logger(
            f"TWStructureExecDoc set_expanded_for_item(item, node):\nitem = {item},\nnode = {node}"
        )
        id_node = node.get("id_node")
        value_expand = self.__expanded_states.get(id_node)
        if value_expand is not None:
            item.setExpanded(value_expand)
        else:
            self.__expanded_states["id_node"] = False
            item.setExpanded(False)

    def set_state_included_for_child(self, node, state):
        self.__obs_manager.obj_l.debug_logger(
            f"""TWStructureExecDoc set_state_included_for_childs(node, state):\nid_node = {node.get("id_node")},\nstate = {state}"""
        )
        item = self.__nodes_to_items.get(node.get("id_node"))
        if item is not None:
            item.setCheckState(0, Qt.Checked if state else Qt.Unchecked)
            childs = self.__obs_manager.obj_pd.get_childs(node)
            if childs:
                for child in childs:
                    self.set_state_included_for_child(child, state)

    def on_item_expanded(self, item):
        """Элемент раскрыт"""
        node = item.data(0, Qt.UserRole)
        id_node = node.get("id_node")
        self.__expanded_states[id_node] = True

    def on_item_collapsed(self, item):
        """Элемент свернут"""
        node = item.data(0, Qt.UserRole)
        id_node = node.get("id_node")
        self.__expanded_states[id_node] = False


# obj_twsed = TWStructureExecDoc()
