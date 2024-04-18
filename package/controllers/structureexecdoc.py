import package.modules.log as log
import package.modules.projectdatabase as projectdatabase
import package.modules.project as project
import package.controllers.pagestemplate as pagestemplate

from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt, Slot


class MyTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None, node=None):
        super().__init__(parent)
        self.node = node

    def get_node(self):
        return self.node


class StructureExecDoc:
    _treewidget_structure_execdoc = None
    _title_sed = None

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

    @staticmethod
    def set_title_sed(title):
        log.Log.get_logger().debug("set_title_sed()")
        StructureExecDoc._title_sed = title

    @staticmethod
    def get_title_sed() -> object:
        log.Log.get_logger().debug("get_title_sed()")
        return StructureExecDoc._title_sed

    @staticmethod
    def set_nodes_to_items(nodes):
        log.Log.get_logger().debug("set_nodes_to_items()")
        StructureExecDoc._nodes_to_items = nodes

    @staticmethod
    def get_nodes_to_items() -> dict:
        log.Log.get_logger().debug("get_nodes_to_items()")
        return StructureExecDoc._nodes_to_items

    @staticmethod
    def connect_structureexecdoc(tr_sed, title_sed):
        """
        Подключить tr_sed к контроллеру.
        """
        log.Log.get_logger().debug("IN connect_structureexecdoc(tr_sed, title_sed)")
        StructureExecDoc.set_tr_sed(tr_sed)
        StructureExecDoc.set_title_sed(title_sed)
        # Очистить при запуске
        StructureExecDoc.clear_sed()

        # Подключение сигнала on_item_changed()
        StructureExecDoc.get_tr_sed().currentItemChanged.connect(
            StructureExecDoc.on_item_changed
        )

    @staticmethod
    def clear_sed():
        """
        Очистить дерево
        """
        log.Log.get_logger().debug("IN clear_tr_sed()")
        StructureExecDoc.get_tr_sed().clear()
        StructureExecDoc.get_tr_sed().setHeaderLabels([""])
        StructureExecDoc.get_title_sed().setText("Проект не выбран")

    @staticmethod
    def create_structure_exec_doc():
        """
        Создает структуру дерева ИД
        """
        log.Log.get_logger().debug("IN create_structure_exec_doc()")
        # Задать название столбца
        title = f"{project.Project.get_current_name()}"
        StructureExecDoc.get_tr_sed().setHeaderLabels(["Проект"])
        StructureExecDoc.get_title_sed().setText(title)
        # проход по вершинам
        StructureExecDoc.update_structure_exec_doc()
    

    @staticmethod
    def update_structure_exec_doc():
        StructureExecDoc.dfs(projectdatabase.Database.get_project_node())

    @staticmethod
    def dfs(parent_node):
        """
        Проход по всем вершинам.
        """
        log.Log.get_logger().debug(f"IN dfs(parent_node): parent_node = {parent_node}")
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
        log.Log.get_logger().debug(f"IN set_item_in_nodes_to_items(node): node = {node}")
        item = None
        if node.get("id_parent") == 0:
            item = MyTreeWidgetItem(StructureExecDoc.get_tr_sed(), node)
        else:
            item = MyTreeWidgetItem(
                StructureExecDoc.get_nodes_to_items()[node.get("id_parent")], node
            )
        item.setText(0, node.get("name_node"))
        # С галочкой по умолчанию
        item.setCheckState(0, Qt.Checked)
        StructureExecDoc.get_nodes_to_items()[node.get("id_node")] = item

    # TODO Функционал добавить
    @staticmethod
    @Slot()
    def on_item_changed(current):
        log.Log.get_logger().debug(f"IN on_item_changed(current): current = {current}")
        pagestemplate.PagesTemplate.update_pages_template(current)
        #print(current.get_node())
        
