import package.modules.log as log
import package.modules.projectdatabase as projectdatabase

from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt


class StructureExecDoc:
    _treewidget_structure_execdoc = None
    _nodes = dict()

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

    def set_nodes(nodes):
        log.Log.get_logger().debug("set_nodes()")
        StructureExecDoc._nodes = nodes

    def get_nodes() -> dict:
        log.Log.get_logger().debug("get_nodes()")
        return StructureExecDoc._nodes

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

    @staticmethod
    def add_datas_to_tr_sed():
        log.Log.get_logger().debug("IN add_datas_to_tr_sed()")
        projectdatabase.Database.add_tables_and_datas_to_empty_db_project()

        # tree_widget = StructureExecDoc.get_tr_sed()

        # # Add items to the tree
        # item1 = QTreeWidgetItem(tree_widget)
        # item1.setText(0, "Item 1")
        # item1.setCheckState(0, Qt.Unchecked)

        # item2 = QTreeWidgetItem(tree_widget)
        # item2.setText(0, "Item 2")
        # item2.setCheckState(0, Qt.Unchecked)

        # item3 = QTreeWidgetItem(tree_widget)
        # item3.setText(0, "Item 3")
        # item3.setCheckState(0, Qt.Unchecked)

        # item1_1 = QTreeWidgetItem(item1)
        # item1_1.setText(0, "Item 1.1")
        # item1_1.setCheckState(0, Qt.Unchecked)

        # item1_2 = QTreeWidgetItem(item1)
        # item1_2.setText(0, "Item 1.2")
        # item1_2.setCheckState(0, Qt.Unchecked)

        # item2_1 = QTreeWidgetItem(item2)
        # item2_1.setText(0, "Item 2.1")
        # item2_1.setCheckState(0, Qt.Unchecked)

        # # Show the tree
        # tree_widget.show()

    @staticmethod
    def create_structure_exec_doc():
        """
        Создает структуру дерева ИД
        """
        log.Log.get_logger().debug("IN create_structure_exec_doc()")
        # TODO Раюота с Project_structure_of_nodes

