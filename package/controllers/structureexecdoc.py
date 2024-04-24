import package.modules.log as log
import package.modules.projectdatabase as projectdatabase
import package.modules.project as project
import package.controllers.pagestemplate as pagestemplate

from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt


class MyTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None, node=None):
        super().__init__(parent)
        self.node = node

    def get_node(self):
        return self.node


class StructureExecDoc:
    __treewidget_structure_execdoc = None
    __title_sed = None

    __nodes_to_items = dict()

    def __init__(self):
        pass

    @staticmethod
    def connect_structureexecdoc(tr_sed, title_sed):
        """
        Подключить tr_sed к контроллеру.
        """
        log.Log.debug_logger("IN connect_structureexecdoc(tr_sed, title_sed)")
        StructureExecDoc.__treewidget_structure_execdoc = tr_sed
        StructureExecDoc.__title_sed = title_sed
        # Очистить при запуске
        StructureExecDoc.clear_sed()

        # Подключение сигналов
        StructureExecDoc.__treewidget_structure_execdoc.currentItemChanged.connect(
            lambda current: pagestemplate.PagesTemplate.update_pages_template(
                current.get_node()
            )
        )
        StructureExecDoc.__treewidget_structure_execdoc.itemChanged.connect(
            lambda item: StructureExecDoc.item_changed(item)
        )

    @staticmethod
    def item_changed(item):
        node = item.get_node()
        state = item.checkState(0) == Qt.Checked
        StructureExecDoc.set_state_included_for_child(
                node,
                item.checkState(0) == Qt.Checked
            )
        projectdatabase.Database.set_included_for_node(node, state)



    @staticmethod
    def clear_sed():
        """
        Очистить дерево
        """
        log.Log.debug_logger("IN clear_tr_sed()")
        StructureExecDoc.__treewidget_structure_execdoc.clear()
        StructureExecDoc.__treewidget_structure_execdoc.setHeaderLabels([""])
        StructureExecDoc.__title_sed.setText("Проект не выбран")

    @staticmethod
    def update_structure_exec_doc():
        """
        Создает структуру дерева ИД
        """
        log.Log.debug_logger("IN update_structure_exec_doc()")
        # очистка
        StructureExecDoc.clear_sed()
        # Задать название столбца
        title = f"{project.Project.get_current_name()}"
        StructureExecDoc.__treewidget_structure_execdoc.setHeaderLabels(["Проект"])
        StructureExecDoc.__title_sed.setText(title)
        # проход по вершинам
        StructureExecDoc.dfs_exec_doc(projectdatabase.Database.get_project_node())

    @staticmethod
    def dfs_exec_doc(parent_node):
        """
        Проход по всем вершинам.
        """
        log.Log.debug_logger(f"IN dfs_exec_doc(parent_node): parent_node = {parent_node}")
        childs = projectdatabase.Database.get_childs(parent_node)
        if childs:
            for child in childs:
                # действие
                StructureExecDoc.set_item_in_nodes_to_items(child)
                # проход по дочерним вершинам
                StructureExecDoc.dfs_exec_doc(child)

    @staticmethod
    def set_item_in_nodes_to_items(node):
        """
        Поставить item в nodes_to_items.
        """
        log.Log.debug_logger(f"IN set_item_in_nodes_to_items(node): node = {node}")
        item = None
        if node.get("id_parent") == 0:
            item = MyTreeWidgetItem(
                StructureExecDoc.__treewidget_structure_execdoc, node
            )
        else:
            item = MyTreeWidgetItem(
                StructureExecDoc.__nodes_to_items[node.get("id_parent")], node
            )
        item.setText(0, node.get("name_node"))
        # С галочкой по умолчанию
        item.setCheckState(0, Qt.Checked)
        StructureExecDoc.__nodes_to_items[node.get("id_node")] = item


    @staticmethod
    def set_state_included_for_child(node, state):
        log.Log.debug_logger(f"IN set_state_included_for_childs(node, state): node = {node}, state = {state}")
        item = StructureExecDoc.__nodes_to_items.get(node.get("id_node"))
        if item:
            item.setCheckState(0, Qt.Checked if state else Qt.Unchecked)

            childs = projectdatabase.Database.get_childs(node)
            if childs:
                for child in childs:
                    StructureExecDoc.set_state_included_for_child(child, state)