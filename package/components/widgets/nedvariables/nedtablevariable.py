import json
import copy
import uuid

from functools import partial

from PySide6.QtWidgets import QWidget, QListWidgetItem, QListWidget, QDialog
from PySide6.QtCore import QTimer, QSize

import package.ui.nedtablevariable_ui as nedtablevariable_ui

import package.components.dialogwindow.neddw.nedrowcoldialogwindow as nedrowcoldialogwindow

import package.components.widgets.customitemqlistwidget as customitemqlistwidget


# TODO !!! РАБОТА С ТАБЛИЦАМИ
class NedTableVariable(QWidget):
    def __init__(self, osbm, type_window, variable=None):
        self.__osbm = osbm
        self.__type_window = type_window
        self.__variable = variable
        self.__osbm.obj_logg.debug_logger("NedTableVariable __init__(osbm, type_window)")
        super(NedTableVariable, self).__init__()
        self.ui = nedtablevariable_ui.Ui_NedTableVariable()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__data = {
            "TYPETABLE": None,
            "ROWCOL": [{"ID": None, "ATTR": None, "TITLE": None, "ORDER": None}],
        }
        self.__config_dict = dict()
        self.__rowcols_items = []
        #
        if self.__variable and self.__variable.get("type_variable") == "TABLE":
            self.__config_variable = self.__variable.get("config_variable")
            if self.__config_variable:
                self.__config_dict = json.loads(self.__config_variable)
        #
        self.config_combox_typetable()
        self.config_lw_attrs()
        self.config_by_type_window()
        #
        self.connecting_actions()

    def get_save_data(self):
        self.save_data()
        self.__osbm.obj_logg.debug_logger(
            f"NedTableVariable get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("NedTableVariable connecting_actions()")
        self.ui.combox_typetable.currentIndexChanged.connect(self.typetable_changed)
        self.ui.btn_addrowcol.clicked.connect(self.add_item)

    def config_combox_typetable(self):
        self.__osbm.obj_logg.debug_logger("NedTableVariable config_combox_typetable()")
        combobox = self.ui.combox_typetable
        combobox.blockSignals(True)
        combobox.clear()
        self.__table_types = self.__osbm.obj_comwith.table_types.get_table_types()
        for table_type in self.__table_types:
            combobox.addItem(table_type.name, table_type.data)
        combobox.blockSignals(False)

    def config_lw_attrs(self, open_rowcol = None):
        self.__osbm.obj_logg.debug_logger("NedTableVariable config_lw_attrs()")
        list_widget = self.ui.lw_attrs
        list_widget.blockSignals(True)
        list_widget.clear()
        self.__rowcols_items = []
        rowcols = self.get_sorted_rowcols()
        for rowcol in rowcols:
            custom_widget = customitemqlistwidget.CustomItemQListWidget(
                self.__osbm, "ROWCOL", rowcol
            )
            item = QListWidgetItem()
            item.setData(0, rowcol)
            # Указываем размер элемента
            item.setSizeHint(custom_widget.sizeHint())
            item.setSizeHint(item.sizeHint().boundedTo(list_widget.sizeHint()))
            list_widget.addItem(item)
            # Устанавливаем виджет для элемента
            list_widget.setItemWidget(item, custom_widget)
            # кнопки
            self.config_buttons_for_item(custom_widget)
            #
            self.__rowcols_items.append(item)
        #
        if self.__rowcols_items:
            if open_rowcol:
                index_template = next(
                    (
                        i
                        for i, rowcol in enumerate(rowcols)
                        if open_rowcol.get("ID") == rowcol.get("ID")
                    ),
                    0,
                )
                list_widget.setCurrentRow(index_template)
            else:
                list_widget.setCurrentRow(0)

        list_widget.blockSignals(False)

    def config_buttons_for_item(self, item_widget):
        self.__osbm.obj_logg.debug_logger(
            f"NedTableVariable config_buttons_for_item(item_widget)\nitem_widget = {item_widget}"
        )
        edit_button = item_widget.get_btn_edit()
        delete_button = item_widget.get_btn_delete()
        edit_button.clicked.connect(
            partial(self.edit_item, data=item_widget.get_data())
        )
        delete_button.clicked.connect(
            partial(self.delete_item, data=item_widget.get_data())
        )

    def delete_item(self, data):
        self.__osbm.obj_logg.debug_logger(
            f"NedTableVariable delete_item(data):\ndata = {data}"
        )
        title_rowcol = data.get("TITLE")
        name_rowcol = data.get("ATTR")
        result = self.__osbm.obj_dw.question_message(
            f'Вы действительно удалить этот атрибут:\n"{title_rowcol}" ({name_rowcol})?'
        )
        if result:
            # удаление
            rowcols = self.get_sorted_rowcols()
            index = next((i for i, rowcol in enumerate(rowcols) if rowcol.get("ID") == data.get("ID")), None)
            if index is not None:
                rowcols.pop(index)
                for index, rowcol in enumerate(rowcols):
                    rowcol["ORDER"] = index
                self.__config_dict["ROWCOLS"] = rowcols
            self.config_lw_attrs()

    def edit_item(self, data):
        self.__osbm.obj_logg.debug_logger(
            f"NedTableVariable edit_item(data):\ndata = {data}"
        )
        self.__osbm.obj_logg.debug_logger("NedTableVariable add_item()")
        type_rowcol = self.ui.combox_typetable.currentData()
        rowcols = self.get_sorted_rowcols()
        result = self.nedrowcoldw("edit", type_rowcol, rowcols, data)
        if result:
            current_rowcol = self.__osbm.obj_nedrowcoldw.get_data()
            attr_current_rowcol = current_rowcol.get("ATTR")
            title_current_rowcol = current_rowcol.get("TITLE")
            order_current_rowcol = current_rowcol.get("ORDER")
            rowcol = {
                "ID": data.get("ID"),
                "ATTR": attr_current_rowcol,
                "TITLE": title_current_rowcol,
                "ORDER": order_current_rowcol
            }
            # удалить из списка
            order_old_rowcol = data.get("ORDER")
            del rowcols[order_old_rowcol]
            # добавить в список
            rowcols.insert(order_current_rowcol, rowcol)
            for index, rowcol in enumerate(rowcols):
                rowcol["ORDER"] = index
            self.__config_dict["ROWCOLS"] = rowcols
            self.config_lw_attrs(data)

    def add_item(self):
        self.__osbm.obj_logg.debug_logger("NedTableVariable add_item()")
        type_rowcol = self.ui.combox_typetable.currentData()
        rowcols = self.get_sorted_rowcols()
        result = self.nedrowcoldw("create", type_rowcol, rowcols, None)
        if result:
            current_rowcol = self.__osbm.obj_nedrowcoldw.get_data()
            attr_current_rowcol = current_rowcol.get("ATTR")
            title_current_rowcol = current_rowcol.get("TITLE")
            order_current_rowcol = current_rowcol.get("ORDER")
            rowcol = {
                "ID": uuid.uuid1().hex,
                "ATTR": attr_current_rowcol,
                "TITLE": title_current_rowcol,
                "ORDER": order_current_rowcol
            }
            rowcols.insert(order_current_rowcol, rowcol)
            for index, rowcol in enumerate(rowcols):
                rowcol["ORDER"] = index
            self.__config_dict["ROWCOLS"] = rowcols
            self.config_lw_attrs(rowcol)
            



    def nedrowcoldw(self, type_ned, type_rowcol, rowcols, rowcol = None):
        self.__osbm.obj_logg.debug_logger("NedTableVariable nedrowcoldw()")
        self.__osbm.obj_nedrowcoldw = nedrowcoldialogwindow.NedRowcolDialogWindow(
            self.__osbm, type_ned, type_rowcol, rowcols, rowcol
        )
        result = self.__osbm.obj_nedrowcoldw.exec()
        return result == QDialog.Accepted

    def config_by_type_window(self):
        self.__osbm.obj_logg.debug_logger("NedTableVariable config_by_type_window()")
        index = 0
        if self.__type_window == "edit":
            typetable = self.__config_dict.get("TYPETABLE")
            index = self.__osbm.obj_comwith.table_types.get_index_by_data(typetable)
        self.typetable_changed(index)

    def typetable_changed(self, index):
        self.__osbm.obj_logg.debug_logger(
            f"NedTableVariable typetable_changed(index):\nindex = {index}"
        )
        #
        is_view_rowcols = self.__osbm.obj_comwith.table_types.get_is_edit_rowcols_by_index(
            index
        )
        self.ui.label_rowcol.setEnabled(is_view_rowcols)
        self.ui.lw_attrs.setEnabled(is_view_rowcols)
        self.ui.btn_addrowcol.setEnabled(is_view_rowcols)
        #
        if is_view_rowcols:
            text_btns = self.__osbm.obj_comwith.table_types.get_text_btns_by_index(index)
            if text_btns:
                self.ui.label_rowcol.setText(text_btns[0])
                self.ui.btn_addrowcol.setText(text_btns[1])
            self.ui.combox_typetable.setCurrentIndex(index)

    def save_data(self):
        # TODO save_data
        self.__osbm.obj_logg.debug_logger("NedTableVariable save_data()")
        typetable = self.ui.combox_typetable.currentData()
        rowcols = self.get_sorted_rowcols()
        self.__data = {
            "TYPETABLE": typetable,
            "ROWCOL": rowcols,
        }

    def get_sorted_rowcols(self):
        rowcols = self.__config_dict.get("ROWCOLS", [])
        return sorted(rowcols, key=lambda x: x.get("ORDER"))
