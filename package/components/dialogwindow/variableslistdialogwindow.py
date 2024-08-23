import json

from PySide6.QtWidgets import (
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QPushButton,
    QCheckBox,
    QHBoxLayout,
    QWidget,
    QHeaderView,
)
from PySide6.QtCore import Qt, QTimer

from functools import partial

import package.components.dialogwindow.neddw.nedvariabledialogwindow as nedvariabledialogwindow

import package.ui.variableslistdialogwindow_ui as variableslistdialogwindow_ui


class Obj:
    pass


class NumericItem(QTableWidgetItem):
    def __lt__(self, other):
        return self.data(Qt.UserRole) < other.data(Qt.UserRole)


class VariablesListDialogWindow(QDialog):
    def __init__(self, osbm, open_node, open_template, open_page):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger(f"VariablesListDialogWindow __init__(osbm, open_node, open_template, open_page): \nopen_node = {open_node}\nopen_template = {open_template}\nopen_page = {open_page}")
        self.initalizate_tabs_objects()
        super(VariablesListDialogWindow, self).__init__()
        self.ui = variableslistdialogwindow_ui.Ui_VariablesListDialog()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__icons = self.__osbm.obj_icons.get_icons()
        self.__all_variables = None
        self.__vertical_scroll_position_by_parameters = {}
        # config
        self.config()
        self.config_tws()
        # Подключаем действия
        self.connecting_actions()
        # отобразить (в нём caf - reconfig)
        self.show_config(open_node, open_template, open_page)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Игнорируем нажатие Enter
            event.ignore()
        else:
            super().keyPressEvent(event)

    def initalizate_tabs_objects(self):
        self.__osbm.obj_logg.debug_logger(
            "VariablesListDialogWindow initalizate_tabs_objects()"
        )
        self.obj_projroject = Obj()
        self.obj_group = Obj()
        self.obj_form_template_page = Obj()
        # Списки с данными
        setattr(
            self.obj_projroject,
            "project_node",
            self.__osbm.obj_prodb.get_project_node(),
        )
        setattr(
            self.obj_group,
            "list_of_group_node",
            self.__osbm.obj_prodb.get_group_nodes(),
        )
        setattr(
            self.obj_form_template_page,
            "list_of_form_node",
            self.__osbm.obj_prodb.get_form_nodes(),
        )

    def config(self):
        self.__osbm.obj_logg.debug_logger("VariablesListDialogWindow config()")
        self.ui.splitter_ftp.setSizes([500, 300])
        self.ui.splitter_group.setSizes([500, 300])
        self.ui.splitter_project.setSizes([500, 300])
        # свернуть/развернуть окно
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("VariablesListDialogWindow connecting_actions()")
        # смена tab
        self.ui.tabwidget.currentChanged.connect(self.on_tab_changed)
        # КОМБОБОКСЫ
        # combox_groups
        self.ui.combox_groups.currentIndexChanged.connect(
            self.combox_groups_index_changed
        )
        # combox_forms
        self.ui.combox_forms.currentIndexChanged.connect(
            self.combox_forms_index_changed
        )
        # combox_templates
        self.ui.combox_templates.currentIndexChanged.connect(
            self.combox_templates_index_changed
        )
        # combox_pages
        self.ui.combox_pages.currentIndexChanged.connect(
            self.combox_pages_index_changed
        )
        self.ui.btn_create_variable.clicked.connect(self.create_variable)
        self.ui.btn_create_variable.setShortcut("Ctrl+N")
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")
        self.ui.btn_save.clicked.connect(self.save_changes)
        self.ui.btn_save.setShortcut("Ctrl+S")

    def get_typetable(self):
        type_table = None
        index = self.ui.tabwidget.currentIndex()
        if index == 0:
            type_table = "project_variables"
        elif index == 1:
            type_table = "group_variables"
        elif index == 2:
            type_table = "form_template_page_variables"
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow get_typetable():\ntype_table = {type_table}"
        )
        return type_table

    def combox_groups_index_changed(self, index):
        self.__osbm.obj_logg.debug_logger(
            f"combox_groups_index_changed(index):\nindex = {index}"
        )
        # данные таблицы
        typetable = self.get_typetable()
        self.caf_two_tables(typetable)

    def combox_forms_index_changed(self, index):
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow combox_forms_index_changed(index):\nindex = {index}"
        )
        self.caf_combobox_template()
        self.caf_combobox_page()
        # данные таблицы
        typetable = self.get_typetable()
        self.caf_two_tables(typetable)

    def combox_templates_index_changed(self, index):
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow combox_templates_index_changed(index):\nindex = {index}"
        )
        self.caf_combobox_page()
        # данные таблицы
        typetable = self.get_typetable()
        self.caf_two_tables(typetable)

    def combox_pages_index_changed(self, index):
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow combox_pages_index_changed(index):\nindex = {index}"
        )
        # данные таблицы
        typetable = self.get_typetable()
        self.caf_two_tables(typetable)


    def show_config(self, open_node, open_template, open_page):
        self.__osbm.obj_logg.debug_logger(
            "VariablesListDialogWindow show_config()"
        )
        if open_node:
            type_node = open_node.get("type_node")
            if type_node == "GROUP":
                self.show_tab_group(open_node)
            elif type_node == "FORM":
                if open_template:
                    if open_page:
                        self.show_tab_form_template_page(open_node, open_template, open_page)
                    else:
                        self.show_tab_form_template_page(open_node, open_template)
                else:
                    self.show_tab_form_template_page(open_node)

        else:
            self.show_tab_project()
            



    def show_tab_project(self):
        self.__osbm.obj_logg.debug_logger("VariablesListDialogWindow show_tab_project()")
        self.ui.tabwidget.setCurrentIndex(0)
        self.caf_two_tables("project_variables")

    def show_tab_group(self, open_node = None):
        self.__osbm.obj_logg.debug_logger("VariablesListDialogWindow show_tab_group()")
        self.ui.tabwidget.setCurrentIndex(1)
        self.caf_combobox_group(open_node)
        self.caf_two_tables("group_variables")
        pass

    def show_tab_form_template_page(self, open_node = None, open_template = None, open_page = None):
        self.__osbm.obj_logg.debug_logger(
            "VariablesListDialogWindow show_tab_form_template_page()"
        )
        self.ui.tabwidget.setCurrentIndex(2)
        self.caf_combobox_form(open_node)
        self.caf_combobox_template(open_template)
        self.caf_combobox_page(open_page)
        self.caf_two_tables("form_template_page_variables")
        pass

    def on_tab_changed(self, index):
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow on_tab_changed(self, index):\nindex = {index}"
        )
        if index == 0:
            self.show_tab_project()
        elif index == 1:
            self.show_tab_group()
        elif index == 2:
            self.show_tab_form_template_page()

    def get_table_by_parameters(self, type_table, editor):
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow get_table_by_parameters(self, type_table, editor):\ntype_table = {type_table}\neditor = {editor}"
        )
        # получение таблицы
        table_widget = None
        if type_table == "project_variables":
            if editor:
                table_widget = self.ui.table_editor_project_variables
            else:
                table_widget = self.ui.table_project_variables
        elif type_table == "group_variables":
            if editor:
                table_widget = self.ui.table_editor_group_variables
            else:
                table_widget = self.ui.table_group_variables
        elif type_table == "form_template_page_variables":
            if editor:
                table_widget = self.ui.table_editor_ftp_variables
            else:
                table_widget = self.ui.table_ftp_variables
        return table_widget

    def get_data_by_parameters(self, type_table, editor):
        # получение данных
        data = []
        if type_table == "project_variables":
            node_data = self.__osbm.obj_prodb.get_node_data(
                self.obj_projroject.project_node
            )
            print(f"node_data = {node_data}")
            for pair in node_data:
                data.append(self.__osbm.obj_prodb.get_variable_by_id(pair.get("id_variable")))
            print(f"data = {data}")
        elif type_table == "group_variables":
            group_node = self.ui.combox_groups.currentData()
            # проверка на наличия групп
            if group_node:
                node_data = self.__osbm.obj_prodb.get_node_data(group_node)
                for pair in node_data:
                    data.append(self.__osbm.obj_prodb.get_variable_by_id(pair.get("id_variable")))
        elif type_table == "form_template_page_variables":
            page = self.ui.combox_pages.currentData()
            if page is None:
                pass
            elif page == "all_pages":
                template = self.ui.combox_templates.currentData()
                if template:
                    template_data = self.__osbm.obj_prodb.get_template_data(template)
                    for pair in template_data:
                        data.append(
                            self.__osbm.obj_prodb.get_variable_by_id(pair.get("id_variable"))
                        )
            else:
                page_data = self.__osbm.obj_prodb.get_page_data(page)
                for pair in page_data:
                    data.append(self.__osbm.obj_prodb.get_variable_by_id(pair.get("id_variable")))
        if editor:
            editor_data = []
            cashe = dict()
            for pair in data:
                cashe[pair.get("id_variable")] = pair
            # self.__all_variables отсортирован по order_variable
            self.__all_variables = self.__osbm.obj_prodb.get_variables()
            for pair in self.__all_variables:
                if cashe.get(pair.get("id_variable")):
                    pair["_checked"] = True
                else:
                    pair["_checked"] = False
                editor_data.append(pair)
            #
            self.__osbm.obj_logg.debug_logger(
                f"VariablesListDialogWindow get_data_by_parameters(self, type_table, editor):\ntype_table = {type_table}\neditor = {editor}\neditor_data = {editor_data}"
            )
            return editor_data
        #
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow get_data_by_parameters(self, type_table, editor):\ntype_table = {type_table}\neditor = {editor}\ndata = {data}"
        )
        return data


    def caf_combobox_group(self, open_node = None):
        self.__osbm.obj_logg.debug_logger("VariablesListDialogWindow caf_combobox_group()")
        if open_node:
            current_text = open_node.get("name_node")
        else:
            current_text = self.ui.combox_groups.currentText()
        #
        self.ui.combox_groups.blockSignals(True)
        self.ui.combox_groups.clear()
        for group_node in self.obj_group.list_of_group_node:
            self.ui.combox_groups.addItem(group_node.get("name_node"), group_node)
        #
        index = self.ui.combox_groups.findText(current_text)
        if index != -1:
            self.ui.combox_groups.setCurrentIndex(index)
        #
        self.ui.combox_groups.blockSignals(False)
        self.ui.combox_groups.show()

    def caf_combobox_form(self, open_node):
        self.__osbm.obj_logg.debug_logger("VariablesListDialogWindow caf_combobox_form()")
        if open_node:
            current_text = open_node.get("name_node")
        else:
            current_text = self.ui.combox_forms.currentText()
        #
        self.ui.combox_forms.blockSignals(True)
        self.ui.combox_forms.clear()
        for form_node in self.obj_form_template_page.list_of_form_node:
            self.ui.combox_forms.addItem(form_node.get("name_node"), form_node)
        #
        index = self.ui.combox_forms.findText(current_text)
        if index != -1:
            self.ui.combox_forms.setCurrentIndex(index)
        #
        self.ui.combox_forms.blockSignals(False)
        self.ui.combox_forms.show()

    def caf_combobox_template(self, open_template = None):
        self.__osbm.obj_logg.debug_logger(
            "VariablesListDialogWindow caf_combobox_template()"
        )
        if open_template:
            current_text = open_template.get("name_template")
        else:
            current_text = self.ui.combox_templates.currentText()
        #
        form = self.ui.combox_forms.currentData()
        templates = []
        if form:
            templates = self.__osbm.obj_prodb.get_templates_by_form(form)
        #
        self.ui.combox_templates.blockSignals(True)
        self.ui.combox_templates.clear()
        for template in templates:
            self.ui.combox_templates.addItem(template.get("name_template"), template)
        #
        index = self.ui.combox_templates.findText(current_text)
        if index != -1:
            self.ui.combox_templates.setCurrentIndex(index)
        #
        self.ui.combox_templates.blockSignals(False)
        self.ui.combox_templates.show()

    def caf_combobox_page(self, open_page = None):
        self.__osbm.obj_logg.debug_logger("VariablesListDialogWindow caf_combobox_page()")
        if open_page:
            current_text = open_page.get("name_page")
        else:
            current_text = self.ui.combox_pages.currentText()
        #
        template = self.ui.combox_templates.currentData()
        pages = []
        if template:
            pages = self.__osbm.obj_prodb.get_pages_by_template(template)
        # очистка
        self.ui.combox_pages.blockSignals(True)
        self.ui.combox_pages.clear()
        # пункт - Для всех страниц
        self.ui.combox_pages.addItem("- Для всех страниц -", "all_pages")
        for page in pages:
            self.ui.combox_pages.addItem(page.get("name_page"), page)
        #
        index = self.ui.combox_pages.findText(current_text)
        if index != -1:
            self.ui.combox_pages.setCurrentIndex(index)
        #
        self.ui.combox_pages.blockSignals(False)
        self.ui.combox_pages.show()

    def caf_two_tables(self, type_table, open_variable=None):
        """
        Логика такая же, что и в reconfig в других QDialogs.
        """
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow caf_two_tables(self, type_table):\ntype_table = {type_table}"
        )
        self.caf_table(type_table, False, open_variable)
        self.caf_table(type_table, True, open_variable)

    def config_tws(self):
        self.__osbm.obj_logg.debug_logger("VariablesListDialogWindow config_tws()")
        tws_no_editor = [
            self.ui.table_project_variables,
            self.ui.table_group_variables,
            self.ui.table_ftp_variables,
        ]
        tws_editor = [
            self.ui.table_editor_project_variables,
            self.ui.table_editor_group_variables,
            self.ui.table_editor_ftp_variables,
        ]
        for tw in tws_no_editor:
            self.config_tw(tw, editor=False)
        for tw in tws_editor:
            self.config_tw(tw, editor=True)

    def config_tw(self, table_widget, editor):
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow config_tw(self, tw):\ntable_widget = {table_widget}"
        )
        # заголовки/столбцы
        table_widget.verticalHeader().hide()
        if editor:
            headers = ["№", "Переменная", "Описание", "Тип", "Вкл", "Действия"]
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
        else:
            headers = ["№", "Переменная", "Описание", "Тип"]
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
        #
        table_widget.setRowCount(0)
        # Настраиваем режимы изменения размера для заголовков
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        if editor:
            header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        # Включение сортировки
        table_widget.setSortingEnabled(True)
        # Запрет на редактирование
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        # Отключаем возможность выделения
        # table_widget.setSelectionMode(QAbstractItemView.NoSelection)
        # table_widget.sortByColumn(0, Qt.AscendingOrder)

    def caf_table(self, type_table, editor, open_variable=None):
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow caf_table(self, type_table, editor):\ntype_table = {type_table}\neditor = {editor}"
        )
        table_widget = self.get_table_by_parameters(type_table, editor)
        # вертикальный ползунок
        vertical_scroll_position = table_widget.verticalScrollBar().value()
        self.__vertical_scroll_position_by_parameters[type_table, editor] = (
            vertical_scroll_position
        )
        # очистка таблицы
        table_widget.clearContents()
        table_widget.setRowCount(0)
        table_widget.setSortingEnabled(False)
        # данные
        data = self.get_data_by_parameters(type_table, editor)
        header = table_widget.horizontalHeaderItem(0)
        header.setData(1000, data)
        table_widget.setRowCount(len(data))
        # TODO используется ли переменная?
        for row, item in enumerate(data):
            # получение данных
            order_variable = item.get("order_variable") + 1
            name_variable = item.get("name_variable")
            title_variable = item.get("title_variable")
            type_variable = item.get("type_variable")
            # setData для строки
            qtwt_order_variable = NumericItem(str(order_variable))
            qtwt_order_variable.setData(Qt.UserRole, order_variable)
            qtwt_name_variable = QTableWidgetItem(name_variable)
            qtwt_name_variable.setData(1001, item)
            qtwt_title_variable = QTableWidgetItem(title_variable)
            qtwt_type_variable = QTableWidgetItem(type_variable)
            # Иконка и текст в зависимости от типа переменной
            key_icon = self.__osbm.obj_icons.get_key_icon_by_type_variable(type_variable)
            qicon_type_variable = self.__icons.get(key_icon)
            qtwt_type_variable.setIcon(qicon_type_variable)
            qtwt_type_variable.setText(type_variable)
            # Добавляем виджеты в ячейки таблицы
            table_widget.setItem(row, 0, qtwt_order_variable)
            table_widget.setItem(row, 1, qtwt_name_variable)
            table_widget.setItem(row, 2, qtwt_title_variable)
            table_widget.setItem(row, 3, qtwt_type_variable)
            # если editor
            if editor:
                self.item_tw_editor(table_widget, item, row, type_table)
            # если open_variable
            if open_variable and open_variable.get("id_variable") == item.get("id_variable"):
                table_widget.selectRow(row)
                QTimer.singleShot(3000, lambda: table_widget.clearSelection())

        # включить сортировку после заполнения данных
        table_widget.setSortingEnabled(True)
        table_widget.sortByColumn(0, Qt.AscendingOrder)
        # Изменение размеров столбцов
        table_widget.resizeColumnsToContents()
        # Вертикальный ползунок
        vertical_scroll_position = self.__vertical_scroll_position_by_parameters.get(
            (type_table, editor), 0
        )
        table_widget.verticalScrollBar().setValue(vertical_scroll_position)

    def item_tw_editor(self, table_widget, item, row, type_table):
        # checkbox
        checkbtn = QCheckBox(text="вкл.")
        is_checked = item.get("_checked")
        if is_checked is None:
            is_checked = False
        checkbtn.setChecked(is_checked)
        # Добавляем значение для сортировки
        sort_value = "ДА" if is_checked else "НЕТ"
        table_widget.setItem(row, 4, QTableWidgetItem(sort_value))
        # кнопки
        edit_button = QPushButton()
        qicon_edit_button = self.__icons.get("pen")
        edit_button.setIcon(qicon_edit_button)
        #
        delete_button = QPushButton()
        qicon_delete_button = self.__icons.get("trash")
        delete_button.setIcon(qicon_delete_button)
        #
        edit_button.custom_data = item
        delete_button.custom_data = item
        # добавление кнопок в layout
        layout = QHBoxLayout()
        layout.addWidget(checkbtn)
        layout.addWidget(edit_button)
        layout.addWidget(delete_button)
        layout.setContentsMargins(4, 0, 4, 0)
        widget = QWidget()
        widget.setLayout(layout)
        table_widget.setCellWidget(row, 5, widget)
        # обработчики
        edit_button.clicked.connect(partial(self.edit_variable, btn=edit_button))
        delete_button.clicked.connect(
            partial(self.delete_variable, btn=delete_button, type_table=type_table)
        )

    def create_variable(self):
        """
        Похожий код у NedPageDialogWindow.
        """
        self.__osbm.obj_logg.debug_logger("VariablesListDialogWindow create_variable()")
        result = self.ned_variable_dw("create")
        if result:
            # получить data
            data = self.__osbm.obj_nedtdw.get_data()
            name_variable = data.get("NAME")
            type_variable = data.get("TYPE")
            title_variable = data.get("TITLE")
            order_variable = data.get("ORDER")
            config_variable = data.get("CONFIG")
            config_variable = json.dumps(config_variable) if config_variable else None
            description_variable = data.get("DESCRIPTION")
            create_variable = {
                "name_variable": name_variable,
                "type_variable": type_variable,
                "title_variable": title_variable,
                "order_variable": order_variable,
                "config_variable": config_variable,
                "description_variable": description_variable,
            }
            # вставка
            self.__all_variables.insert(order_variable, create_variable)
            self.__osbm.obj_prodb.insert_variable(create_variable)
            # Меняем порядок в БД - кому нужно
            for index, variable in enumerate(self.__all_variables):
                order = variable.get("order_variable")
                if order != index:
                    self.__osbm.obj_prodb.set_order_for_variable(variable, index)
            # обновление таблиц + self.__all_variables
            type_table = self.get_typetable()
            self.caf_two_tables(type_table, create_variable)

    def edit_variable(self, btn):
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow edit_variable(btn):\nbtn = {btn}"
        )
        item = btn.custom_data
        result = self.ned_variable_dw("edit", item)
        if result:
            # получить data
            data = self.__osbm.obj_nedtdw.get_data()
            name_variable = data.get("NAME")
            type_variable = data.get("TYPE")
            title_variable = data.get("TITLE")
            order_variable = data.get("ORDER")
            config_variable = data.get("CONFIG")
            config_variable = json.dumps(config_variable) if config_variable else None
            description_variable = data.get("DESCRIPTION")
            edit_variable = {
                "id_variable": item.get("id_variable"),
                "name_variable": name_variable,
                "type_variable": type_variable,
                "title_variable": title_variable,
                "order_variable": order_variable,
                "config_variable": config_variable,
                "description_variable": description_variable,
            }
            # сортировочный процесс
            self.__all_variables.remove(item)
            self.__all_variables.insert(order_variable, edit_variable)
            # замена информации
            self.__osbm.obj_prodb.update_variable(edit_variable)
            # Меняем порядок в БД - кому нужно
            for index, variable in enumerate(self.__all_variables):
                order = variable.get("order_variable")
                if order != index:
                    self.__osbm.obj_prodb.set_order_for_variable(variable, index)
            # обновление таблиц + self.__all_variables
            type_table = self.get_typetable()
            self.caf_two_tables(type_table, edit_variable)

    def ned_variable_dw(self, type_window, variable=None):
        self.__osbm.obj_nedtdw = nedvariabledialogwindow.NedVariableDialogWindow(
            self.__osbm, type_window, self.__all_variables, variable
        )
        result = self.__osbm.obj_nedtdw.exec()
        return result == QDialog.Accepted

    def delete_variable(self, btn, type_table):
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow delete_variable(btn, type_table):\nbtn = {btn}\ntype_table = {type_table}"
        )
        item = btn.custom_data
        title_variable = item.get("title_variable")
        name_variable = item.get("name_variable")
        question = self.__osbm.obj_dw.question_message(
            f'Вы действительно хотите удалить эту переменную:\n"{title_variable}" ({name_variable})?'
        )
        if question:
            # удалить из БД
            self.__all_variables.remove(item)
            self.__osbm.obj_prodb.delete_variable(item)
            # обновить порядок в БД - кому нужно
            for index, variable in enumerate(self.__all_variables):
                order = variable.get("order_variable")
                if order != index:
                    self.__osbm.obj_prodb.set_order_for_variable(variable, index)
            self.caf_two_tables(type_table)

    def get_current_data_table(self, type_table, editor=False):
        table_widget = self.get_table_by_parameters(type_table, editor)
        header = table_widget.horizontalHeaderItem(0)
        data = header.data(1000)
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow get_current_data_table(type_table, editor) -> list:\ntype_table = {type_table}\neditor = {editor}\ndata = {data}"
        )
        return data

    def get_new_data_editor_table(self, type_table):
        new_data = []
        table_widget_editor = self.get_table_by_parameters(type_table, True)
        row_count = table_widget_editor.rowCount()
        for row in range(row_count):
            item = table_widget_editor.item(row, 1).data(1001)
            checked = (
                table_widget_editor.cellWidget(row, 5).findChild(QCheckBox).isChecked()
            )
            if checked:
                item.pop("_checked")
                new_data.append(item)
        self.__osbm.obj_logg.debug_logger(
            f"VariablesListDialogWindow get_new_data_editor_table(type_table) -> list:\ntype_table = {type_table}\nnew_data = {new_data}"
        )
        return new_data

    def save_changes(self):
        self.__osbm.obj_logg.debug_logger("VariablesListDialogWindow save_changes()")
        type_table = self.get_typetable()
        # получить данные
        new_data = self.get_new_data_editor_table(type_table)
        old_data = self.get_current_data_table(type_table, editor=False)
        # данные для удаления
        ids_new_data = {item.get("id_variable") for item in new_data}
        data_for_delete = [
            item for item in old_data if item.get("id_variable") not in ids_new_data
        ]
        # данные для добавления
        ids_old_data = {item.get("id_variable") for item in old_data}
        data_for_insert = [
            item for item in new_data if item.get("id_variable") not in ids_old_data
        ]
        # удаление и добавление
        if type_table == "project_variables":
            project_node = self.obj_projroject.project_node
            self.__osbm.obj_prodb.insert_node_datas(project_node, data_for_insert)
            self.__osbm.obj_prodb.delete_node_datas(project_node, data_for_delete)
        elif type_table == "group_variables":
            group_node = self.ui.combox_groups.currentData()
            if group_node:
                self.__osbm.obj_prodb.insert_node_datas(group_node, data_for_insert)
                self.__osbm.obj_prodb.delete_node_datas(group_node, data_for_delete)
        elif type_table == "form_template_page_variables":
            page = self.ui.combox_pages.currentData()
            if page is None:
                pass
            elif page == "all_pages":
                template = self.ui.combox_templates.currentData()
                if template:
                    self.__osbm.obj_prodb.insert_template_datas(
                        template, data_for_insert
                    )
                    self.__osbm.obj_prodb.delete_template_datas(
                        template, data_for_delete
                    )
            else:
                self.__osbm.obj_prodb.insert_page_datas(page, data_for_insert)
                self.__osbm.obj_prodb.delete_page_datas(page, data_for_delete)

        # обновление таблиц
        self.caf_two_tables(type_table)
