import json

from PySide6.QtWidgets import (
    QDialog,
    QTableWidget,
    QHeaderView,
    QMenu,
    QApplication,
    QTableWidgetItem,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

import package.ui.formtabledialogwindow_ui as formtabledialogwindow_ui


class FormTableDialogWindow(QDialog):
    def __init__(self, osbm, current_variable, config_dict, value_pair):
        self.__osbm = osbm
        self.__current_variable = current_variable
        self.__config_dict = config_dict
        self.__value_pair = value_pair
        self.__osbm.obj_logg.debug_logger(
            f"FormTableDialogWindow __init__(osbm, current_variable, config_dict, value_pair): \n current_variable = {current_variable}, \n config_dict = {config_dict}, \n value_pair = {value_pair}"
        )
        super(FormTableDialogWindow, self).__init__()
        self.ui = formtabledialogwindow_ui.Ui_FormTableDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__typetable = None
        self.__rowcols = []
        #
        self.__data = []
        #
        self.config()
        self.config_tw()
        self.config_context_menu()
        #
        self.connecting_actions()

    def get_data(self):
        self.__osbm.obj_logg.debug_logger(
            f"FormTableDialogWindow get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def config(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow config()")
        #
        self.ui.label_nametable.setText(
            self.__current_variable.get("name_variable", "Таблица")
        )
        #
        self.ui.table.clear()
        #
        self.__typetable = self.__config_dict.get("TYPETABLE")
        self.__rowcols = self.__config_dict.get("ROWCOLS")
        #
        if self.__typetable == "COL":
            self.ui.add_button.setText("Добавить строку")
            self.ui.delete_button.setText("Удалить строку")
        elif self.__typetable == "ROW":
            self.ui.add_button.setText("Добавить столбец")
            self.ui.delete_button.setText("Удалить столбец")
        # свернуть/развернуть окно
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    def config_tw(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow config_tw()")
        #
        self.ui.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )
        # self.ui.table.horizontalHeader().setSectionResizeMode(
        #     QHeaderView.ResizeMode.ResizeToContents
        # )
        #
        headers = []
        ids_rowcols = []
        self.__rowcols = sorted(self.__rowcols, key=lambda x: x.get("ORDER"))
        for rowcol in self.__rowcols:
            headers.append(f'{rowcol.get("TITLE")} ({rowcol.get("ATTR")})')
            ids_rowcols.append(rowcol.get("ID"))
        #
        table_data, len_data = self.get_table_data_from_value_pair(ids_rowcols)
        self.fill_tw_table(table_data, headers, len_data)
        self.resize_headers_tw_table(headers)


    def config_context_menu(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow config_context_menu()")
        # контекстное меню
        self.context_menu = QMenu(self)
        self.context_menu.addSeparator()
        # Вырезать - cut_values_to_clipboard
        self.cut_action = QAction("Вырезать", self)
        self.cut_action.triggered.connect(lambda: self.cut_values_to_clipboard())
        self.context_menu.addAction(self.cut_action)
        # Копировать - copy_values_to_clipboard
        self.copy_action = QAction("Копировать", self)
        self.copy_action.triggered.connect(lambda: self.copy_values_to_clipboard())
        self.context_menu.addAction(self.copy_action)        
        #
        self.context_menu.addSeparator()
        #
        self.paste_action = QAction("Вставить ", self)
        self.paste_action.triggered.connect(lambda: self.paste_values_from_clipboard())
        self.context_menu.addAction(self.paste_action)
        #
        self.context_menu.addSeparator()
        # Очистиь значения выделенного
        self.clear_action = QAction("Очистить выделенное", self)
        self.clear_action.triggered.connect(lambda: self.clear_selected_values())
        self.context_menu.addAction(self.clear_action)
        # контекстное меню по правой кнопкой мыши по таблице.
        self.ui.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.table.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        # Show the context menu at the mouse position
        self.__osbm.obj_logg.debug_logger(
            f"FormTableDialogWindow show_context_menu(position):\nposition = {position}"
        )
        self.context_menu.exec_(self.ui.table.mapToGlobal(position))

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow connecting_actions()")
        # действия в завимости от типа таблицы
        if self.__typetable == "COL":
            self.ui.add_button.clicked.connect(self.add_row)
            self.ui.delete_button.clicked.connect(self.delete_row)
        elif self.__typetable == "ROW":
            self.ui.add_button.clicked.connect(self.add_column)
            self.ui.delete_button.clicked.connect(self.delete_column)
        #
        self.ui.btn_save.clicked.connect(self.save)
        self.ui.btn_save.setShortcut("Ctrl+S")
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")

    def add_row(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow add_row()")
        selected_row = self.ui.table.currentRow()
        if selected_row == -1:
            row_count = self.ui.table.rowCount()
        else:
            row_count = selected_row + 1
        self.ui.table.insertRow(row_count)
        for column in range(self.ui.table.columnCount()):
            item = QTableWidgetItem()
            self.ui.table.setItem(row_count, column, item)

    def add_column(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow add_column()")
        # column_count = self.ui.table.columnCount()
        # self.ui.table.insertColumn(column_count)
        # for row in range(self.ui.table.rowCount()):
        #     item = QTableWidgetItem()
        #     self.ui.table.setItem(row, column_count, item)

    def delete_row(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow delete_row()")
        current_row = self.ui.table.currentRow()
        if current_row >= 0:
            self.ui.table.removeRow(current_row)

    def delete_column(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow delete_column()")
        # current_column = self.ui.table.currentColumn()
        # if current_column >= 0:
        #     self.ui.table.removeColumn(current_column)

    # def update_cell(self, row, column):
    #     item = self.ui.table.item(row, column)
    #     if item:
    #         print(f"Cell ({row}, {column}) changed to {item.text()}")

    def clear_selected_values(self):
        self.__osbm.obj_logg.debug_logger(
            "FormTableDialogWindow clear_selected_values()"
        )
        selected_items = self.ui.table.selectedItems()
        for item in selected_items:
            item.setText("")


    def cut_values_to_clipboard(self):
        self.__osbm.obj_logg.debug_logger(
            "FormTableDialogWindow cut_values_to_clipboard()"
        )
        self.copy_values_to_clipboard()
        self.clear_selected_values()


    def copy_values_to_clipboard(self):
        """
        Копирование значения в буфер обмена
        """
        self.__osbm.obj_logg.debug_logger(
            "FormTableDialogWindow copy_values_to_clipboard()"
        )
        selected_items = self.ui.table.selectedItems()
        if not selected_items:
            return
        clipboard = QApplication.clipboard()
        clipboard.clear()
        # Сортируем элементы по строкам и колонкам
        selected_items.sort(key=lambda item: (item.row(), item.column()))
        # Формируем текст для вставки в буфер обмена
        rows = []
        current_row = -1
        current_row_values = []
        for item in selected_items:
            if item.row() != current_row:
                if current_row != -1:
                    rows.append("\t".join(current_row_values))
                current_row_values = []
                current_row = item.row()
            current_row_values.append(item.text())
        if current_row_values:
            rows.append("\t".join(current_row_values))
        clipboard.setText("\n".join(rows))

    # def copy_qtable_values_to_clipboard(self):
    #     """
    #     Копирование значения в буфер обмена
    #     """
    #     self.__osbm.obj_logg.debug_logger(
    #         "FormTableDialogWindow copy_qtable_values_to_clipboard()"
    #     )
    #     selected_items = self.ui.table.selectedItems()
    #     values_array = {}

    #     # Формируем словарь значений для хранения строк и их значений
    #     for item in selected_items:
    #         row = item.row()
    #         col = item.column()
    #         if row not in values_array:
    #             values_array[row] = {}
    #         values_array[row][col] = item.text()

    #     # Преобразуем словарь в JSON
    #     text = json.dumps(values_array)

    #     self.__clipboard = QApplication.clipboard()
    #     self.__clipboard.clear()
    #     self.__clipboard.setText(text)
    #     print(f"text = {text}")

    def paste_values_from_clipboard(self):
        """
        Вставка значения из буфера обмена
        """
        self.__osbm.obj_logg.debug_logger(
            "FormTableDialogWindow paste_from_clipboard()"
        )
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        row_start = self.ui.table.currentRow()
        column_start = self.ui.table.currentColumn()
        for row, line in enumerate(text.split("\n")):
            for column, item in enumerate(line.split("\t")):
                if (
                    item
                    and (row + row_start < self.ui.table.rowCount())
                    and (column + column_start < self.ui.table.columnCount())
                ):
                    self.ui.table.setItem(
                        row + row_start, column + column_start, QTableWidgetItem(item)
                    )

    # def paste_qtable_values_from_clipboard(self):
    #     """
    #     Вставка выделенного из буфера обмена
    #     """
    #     self.__osbm.obj_logg.debug_logger(
    #         "FormTableDialogWindow paste_qtable_values_from_clipboard()"
    #     )
    #     if self.__clipboard:
    #         text = self.__clipboard.text()
    #     else:
    #         return

    #     # Декодируем JSON
    #     values_dict = json.loads(text) if text else {}
    #     selected_items = self.ui.table.selectedItems()
    #     start_row = selected_items[0].row() if selected_items else 0
    #     start_col = selected_items[0].column() if selected_items else 0

    #     for row, columns in values_dict.items():
    #         row_index = int(row)  # Преобразуем строку в целое число
    #         if start_row + row_index < self.ui.table.rowCount():
    #             for col, value in columns.items():
    #                 col_index = int(col)  # Преобразуем строку в целое число
    #                 if start_col + col_index < self.ui.table.columnCount():
    #                     item = self.ui.table.item(
    #                         start_row + row_index, start_col + col_index
    #                     )
    #                     if item:
    #                         item.setText(value)

    def get_table_data_from_value_pair(self, ids_rowcols):
        self.__osbm.obj_logg.debug_logger(
            f"FormTableDialogWindow get_table_data_from_value_pair(ids_rowcols):\nids_rowcols = {ids_rowcols}"
        )
        json_data = self.__value_pair
        if json_data:
            data = json.loads(json_data)
            # заполнить информацией исходя из ID
            table_data = []
            # словарь ключ-значение
            data_rowcol_by_id_rowcol = dict()
            for elem_data in data:
                data_rowcol_by_id_rowcol[elem_data.get("id_rowcol")] = elem_data.get(
                    "data_rowcol"
                )
            #
            len_data = 0
            for ids_rowcol in ids_rowcols:
                data_rowcol = data_rowcol_by_id_rowcol.get(ids_rowcol, [])
                len_data = max(len_data, len(data_rowcol))
                table_data.append(data_rowcol)
            return (table_data, len_data)
        return ([[]], 0)

    def fill_tw_table(self, table_data, headers, len_data):
        self.__osbm.obj_logg.debug_logger(
            f"FormTableDialogWindow fill_tw_table(table_data, headers, len_data):\n table_data = {table_data}\n headers = {headers}\n len_data = {len_data}"
        )
        if self.__typetable == "COL":
            # заголовки
            self.ui.table.setRowCount(len_data)
            self.ui.table.setColumnCount(len(headers))
            self.ui.table.setHorizontalHeaderLabels(headers)
            self.ui.table.verticalHeader().setVisible(False)
            #
            for col, col_data in enumerate(table_data):
                for row, value in enumerate(col_data):
                    item = QTableWidgetItem(value)
                    self.ui.table.setItem(row, col, item)

        elif self.__typetable == "ROW":
            # заголовки
            self.ui.table.setRowCount(len(headers))
            self.ui.table.setColumnCount(len_data)
            self.ui.table.setVerticalHeaderLabels(headers)
            self.ui.table.horizontalHeader().setVisible(False)
            #
            for row, row_data in enumerate(table_data):
                for col, value in enumerate(row_data):
                    item = QTableWidgetItem(value)
                    self.ui.table.setItem(row, col, item)

    def resize_headers_tw_table(self, headers):
        self.__osbm.obj_logg.debug_logger(f"FormTableDialogWindow resize_cols_tw_table(headers): \n headers = {headers}")
        table_widget = self.ui.table
        for index in range(len(headers)):
            header_width = table_widget.horizontalHeader().fontMetrics().horizontalAdvance(headers[index])
            table_widget.setColumnWidth(index, header_width + 20)

    def get_data_from_table(self) -> list:
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow to_json() -> list:")
        data = [
            {"id_rowcol": rowcol.get("ID"), "data_rowcol": []}
            for rowcol in self.__rowcols
        ]
        for row in range(self.ui.table.rowCount()):
            for column in range(self.ui.table.columnCount()):
                item = self.ui.table.item(row, column)
                text = item.text() if item else ""
                #
                if self.__typetable == "COL":
                    data[column]["data_rowcol"].append(text)
                elif self.__typetable == "ROW":
                    data[row]["data_rowcol"].append(text)
        print(f"table_data = {data}")
        return json.dumps(data)

    def save(self):
        self.__osbm.obj_logg.debug_logger("FormTableDialogWindow save()")
        self.__data = self.get_data_from_table()
        self.accept()
