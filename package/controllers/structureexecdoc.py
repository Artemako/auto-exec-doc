import package.modules.log as log
import package.modules.projectdatabase as projectdatabase
import package.modules.project as project

from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt


class StructureExecDoc:
    _treewidget_structure_execdoc = None
    _nodes_to_items = dict()

    def __init__(self):
        pass

    @staticmethod
    def set_tr_sed(tr_sed):
        log.Log.get_logger().debug("set_tr_sed()")
        StructureExecDoc._treewidget_structure_execdoc = tr_sed

    @staticmethod
    def get_tr_sed() -> object:
        log.Log.get_logger().debug("get_tr_sed() -> object")
        return StructureExecDoc._treewidget_structure_execdoc

    def set_nodes_to_items(nodes):
        log.Log.get_logger().debug("set_nodes_to_items()")
        StructureExecDoc._nodes_to_items = nodes

    def get_nodes_to_items() -> dict:
        log.Log.get_logger().debug("get_nodes_to_items()")
        return StructureExecDoc._nodes_to_items

    @staticmethod
    def connect_structureexecdoc(tr_sed):
        """
        Подключить tr_sed к контроллеру.
        """
        log.Log.get_logger().debug("IN connect_structureexecdoc()")
        StructureExecDoc.set_tr_sed(tr_sed)
        # Очистить при запуске
        StructureExecDoc.clear_tr_sed()

    @staticmethod
    def clear_tr_sed():
        """
        Очистить дерево
        """
        log.Log.get_logger().debug("IN clear_tr_sed()")
        StructureExecDoc.get_tr_sed().clear()
        StructureExecDoc.get_tr_sed().setHeaderLabels([""])
        


    @staticmethod
    def create_structure_exec_doc():
        """
        Создает структуру дерева ИД
        """
        log.Log.get_logger().debug("IN create_structure_exec_doc()")
        # Задать название столбца
        title = f"Проект: {project.Project.get_current_name()}"
        StructureExecDoc.get_tr_sed().setHeaderLabels([title])
        # Работа с Project_structure_of_nodes
        StructureExecDoc.dfs(projectdatabase.Database.get_project_node())


    @staticmethod
    def dfs(parent_node):
        """
        Проход по всем вершинам.
        """
        log.Log.get_logger().debug(f"IN dfs({parent_node})")
        childs = projectdatabase.Database.get_childs(parent_node)
        if childs:
            for child in childs:
                # действие
                StructureExecDoc.set_item_in_nodes_to_items(child)
                # проход по дочерним вершинам
                StructureExecDoc.dfs(child)

    @staticmethod
    def set_item_in_nodes_to_items(node):
        """
        Поставить item в nodes_to_items.
        """
        log.Log.get_logger().debug(f"IN set_item_in_nodes_to_items({node})")
        item = None
        if node.get("id_parent") == 0:
            item = QTreeWidgetItem(StructureExecDoc.get_tr_sed())
        else:            
            item = QTreeWidgetItem(StructureExecDoc.get_nodes_to_items()[node.get("id_parent")])
        item.setText(0, node.get("name_node"))
        # С галочкой по умолчанию
        item.setCheckState(0, Qt.Checked)
        StructureExecDoc.get_nodes_to_items()[node.get("id_node")] = item
