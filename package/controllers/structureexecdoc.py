import package.modules.log as log

from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt

class StructureExecdoc:
    _treewidget_structure_execdoc = None

    def __init__(self):
        pass

    @staticmethod
    def set_tr_sed(tr_sed):
        log.Log.get_logger().debug("set_tr_sed()")
        StructureExecdoc._treewidget_structure_execdoc = tr_sed

    @staticmethod
    def get_tr_sed() -> object:
        log.Log.get_logger().debug("get_tr_sed() -> object")
        return StructureExecdoc._treewidget_structure_execdoc

    @staticmethod
    def connect_structureexecdoc(tr_sed):
        """
        Подключить tr_sed к контроллеру.
        """
        log.Log.get_logger().debug("IN connect_structureexecdoc()")
        StructureExecdoc.set_tr_sed(tr_sed)

        # TODO Убрать потом
        StructureExecdoc.clear_tr_sed()
        StructureExecdoc.add_datas_to_tr_sed()

    @staticmethod
   
    def clear_tr_sed():
        """
        Очистить дерево 
        """
        log.Log.get_logger().debug("IN clear_tr_sed()")
        StructureExecdoc.get_tr_sed().clear()

    @staticmethod
    def add_datas_to_tr_sed():
        log.Log.get_logger().debug("IN add_datas_to_tr_sed()")

        # tree_widget = StructureExecdoc.get_tr_sed()

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
