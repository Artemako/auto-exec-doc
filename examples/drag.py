from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

class DraggableTableWidget(QTableWidget):
    def __init__(self, parent = None):
        self.__parent = parent
        super().__init__()
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def dropEvent(self, event):
        if event.source() == self:
            drop_row = self.rowAt(event.position().y())
            if drop_row == -1:
                drop_row = self.rowCount() - 1

            drag_row = self.currentRow()

            if drag_row != drop_row and drag_row != -1:
                row_data = []
                for column in range(self.columnCount()):
                    item = self.item(drag_row, column)
                    row_data.append(item.text() if item else "")

                self.insertRow(drop_row)

                for column in range(self.columnCount()):
                    self.setItem(drop_row, column, QTableWidgetItem(row_data[column]))
                    
                self.removeRow(drag_row if drag_row < drop_row else drag_row + 1)
        event.accept()
        # TODO self.__parent сделать перестановку компонентов
        # self.__parent.drop_changed(item)

    def dragMoveEvent(self, event):
        if event.source() == self:
            event.accept()


    from PySide6.QtWidgets import QTreeWidget, QAbstractItemView
from PySide6.QtCore import Qt


class DraggableTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        self.__parent = parent
        super().__init__()
        self.setDragDropMode(QTreeWidget.InternalMove)

    def set_parent(self, parent):
        self.__parent = parent

    def dragMoveEvent(self, event):
        if self.canDrop(event):
            super().dragMoveEvent(event)
        else:
            event.ignore()

    def dropEvent(self, event):
        if self.canDrop(event):
            item = self.itemAt(event.pos())
            item_from = self.currentItem()
            item_to = item
            super().dropEvent(event)
            self.__parent.drop_changed(item)
        else:
            event.ignore()

    def canDrop(self, event):
        target = self.itemAt(event.pos())
        if target is not None:
            index = self.indexFromItem(target)
            indicator = self.dragIndicator(
                event.pos(), self.visualItemRect(target), index
            )
            return (
                indicator == QAbstractItemView.AboveItem
                or indicator == QAbstractItemView.BelowItem
            )
        return False

    def dragIndicator(self, pos, rect, index):
        indicator = QAbstractItemView.OnViewport
        if not self.dragDropOverwriteMode():
            margin = int(max(2, min(rect.height() / 5.5, 12)))
            if pos.y() - rect.top() < margin:
                indicator = QAbstractItemView.AboveItem
            elif rect.bottom() - pos.y() < margin:
                indicator = QAbstractItemView.BelowItem
            elif rect.contains(pos, True):
                indicator = QAbstractItemView.OnItem
        else:
            touching = rect.adjust(-1, -1, 1, 1)
            if touching.contains(pos, False):
                indicator = QAbstractItemView.OnItem
        if (
            indicator == QAbstractItemView.OnItem
            and not self.model().flags(index) & Qt.ItemIsDropEnabled
        ):
            if pos.y() < rect.center().y():
                indicator = QAbstractItemView.AboveItem
            else:
                indicator = QAbstractItemView.BelowItem
        return indicator




    def drop_changed(self, item):
        self.__osbm.obj_logg.debug_logger(
            f"NodesEditorDialogWindow drop_changed(item):\nitem = {item}"
        )
        # узнать вершину
        current_node = item.data(0, Qt.UserRole)
        print(f"current_node = {current_node}")
        old_id_parent = current_node.get("id_parent")
        # родитель
        parent_item = item.parent()
        if parent_item is None:
            parent_node = self.__osbm.obj_prodb.get_project_node()
        else:
            parent_node = parent_item.data(0, Qt.UserRole)
        id_parent_node = parent_node.get("id_node")
        if old_id_parent == id_parent_node:
            # только в одной группе
            self.update_order_for_parent_item_childs(parent_item, parent_node)
        else:
            # в разных группах (сначала в новой, потом в старой)
            self.update_order_for_parent_item_childs(parent_item)
            self.update_order_for_old_parent_node_childs(old_id_parent)
    

    def update_order_for_parent_item_childs(self, parent_item, parent_node):
        self.__osbm.obj_logg.debug_logger(
            f"NodesEditorDialogWindow update_order_for_parent_item_childs(parent_item, parent_node):\nparent_item = {parent_item}\nparent_node = {parent_node}"
        )
        # получить дочерние элементы
        if parent_item is None:
            children_items = [child_item for child_item in self.ui.tw_nodes.invisibleRootItem().takeChildren()]
        else:
            children_items = parent_item.takeChildren()
        # обновить порядок
        for index, child_item in enumerate(children_items):
            child_node = child_item.data(0, Qt.UserRole)
            # поставить родителя и порядок
            self.__osbm.obj_prodb.set_new_parent_for_child_node(parent_node, child_node)
            self.__osbm.obj_prodb.set_order_for_node(child_node, index)

    def update_order_for_old_parent_node_childs(self, old_id_parent):
        self.__osbm.obj_logg.debug_logger(
            f"NodesEditorDialogWindow update_order_for_old_parent_node_childs(old_id_parent):\nold_id_parent = {old_id_parent}"
        )
        parent_node = {
            "id_node": old_id_parent,
        }
        childs_nodes = self.__osbm.obj_prodb.get_childs(parent_node)
        for index, child_node in enumerate(childs_nodes):
            # поставить порядок
            self.__osbm.obj_prodb.set_order_for_node(child_node, index)