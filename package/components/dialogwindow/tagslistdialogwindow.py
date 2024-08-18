from PySide6.QtWidgets import (
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QPushButton,
    QCheckBox,
    QHBoxLayout,
    QWidget,
    QHeaderView
)
from PySide6.QtCore import Qt

from functools import partial

import package.components.dialogwindow.neddw.nedtagdialogwindow as nedtagdialogwindow

import package.ui.tagslistdialogwindow_ui as tagslistdialogwindow_ui


class Obj:
    pass


class NumericItem(QTableWidgetItem):
    def __lt__(self, other):
        return self.data(Qt.UserRole) < other.data(Qt.UserRole)

# TODO Сделать open_...
class TagsListDialogWindow(QDialog):
    def __init__(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger(
            "TagsListDialogWindow __init__(osbm)"
        )
        self.initalizate_tabs_objects()
        super(TagsListDialogWindow, self).__init__()
        self.ui = tagslistdialogwindow_ui.Ui_TagsListDialog()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__icons = self.__osbm.obj_icons.get_icons()
        # config
        self.config()
        self.config_tws()
        # Подключаем действия
        self.connecting_actions()
        # отобразить первый таб (в нём caf - reconfig)
        self.show_tab_project()

    def initalizate_tabs_objects(self):
        self.__osbm.obj_logg.debug_logger(
            "TagsListDialogWindow initalizate_tabs_objects()"
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
        self.__osbm.obj_logg.debug_logger("TagsListDialogWindow config()")
        self.ui.splitter_ftp.setSizes([500, 300])
        self.ui.splitter_group.setSizes([500, 300])
        self.ui.splitter_project.setSizes([500, 300])
        # свернуть/развернуть окно
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger(
            "TagsListDialogWindow connecting_actions()"
        )
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
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")
        self.ui.btn_save.clicked.connect(self.save_changes)
        self.ui.btn_save.setShortcut("Ctrl+S")

    def get_typetable(self):
        type_table = None
        index = self.ui.tabwidget.currentIndex()
        if index == 0:
            type_table = "project_tags"
        elif index == 1:
            type_table = "group_tags"
        elif index == 2:
            type_table = "form_template_page_tags"
        self.__osbm.obj_logg.debug_logger(
            f"TagsListDialogWindow get_typetable():\ntype_table = {type_table}"
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
            f"TagsListDialogWindow combox_forms_index_changed(index):\nindex = {index}"
        )
        self.caf_combobox_template()
        self.caf_combobox_page()
        # данные таблицы
        typetable = self.get_typetable()
        self.caf_two_tables(typetable)

    def combox_templates_index_changed(self, index):
        self.__osbm.obj_logg.debug_logger(
            f"TagsListDialogWindow combox_templates_index_changed(index):\nindex = {index}"
        )
        self.caf_combobox_page()
        # данные таблицы
        typetable = self.get_typetable()
        self.caf_two_tables(typetable)

    def combox_pages_index_changed(self, index):
        self.__osbm.obj_logg.debug_logger(
            f"TagsListDialogWindow combox_pages_index_changed(index):\nindex = {index}"
        )
        # данные таблицы
        typetable = self.get_typetable()
        self.caf_two_tables(typetable)

    def show_tab_project(self):
        self.__osbm.obj_logg.debug_logger("TagsListDialogWindow show_tab_project()")
        self.ui.tabwidget.setCurrentIndex(0)
        self.caf_two_tables("project_tags")

    def show_tab_group(self):
        self.__osbm.obj_logg.debug_logger("TagsListDialogWindow show_tab_group()")
        self.ui.tabwidget.setCurrentIndex(1)
        self.caf_combobox_group()
        self.caf_two_tables("group_tags")
        pass

    def show_tab_form_template_page(self):
        self.__osbm.obj_logg.debug_logger(
            "TagsListDialogWindow show_tab_form_template_page()"
        )
        self.ui.tabwidget.setCurrentIndex(2)
        self.caf_combobox_form_template_page()
        self.caf_two_tables("form_template_page_tags")
        pass

    def on_tab_changed(self, index):
        self.__osbm.obj_logg.debug_logger(
            f"TagsListDialogWindow on_tab_changed(self, index):\nindex = {index}"
        )
        if index == 0:
            self.show_tab_project()
        elif index == 1:
            self.show_tab_group()
        elif index == 2:
            self.show_tab_form_template_page()

    def get_table_by_parameters(self, type_table, editor):
        self.__osbm.obj_logg.debug_logger(
            f"TagsListDialogWindow get_table_by_parameters(self, type_table, editor):\ntype_table = {type_table}\neditor = {editor}"
        )
        # получение таблицы
        table_widget = None
        if type_table == "project_tags":
            if editor:
                table_widget = self.ui.table_editor_project_tags
            else:
                table_widget = self.ui.table_project_tags
        elif type_table == "group_tags":
            if editor:
                table_widget = self.ui.table_editor_group_tags
            else:
                table_widget = self.ui.table_group_tags
        elif type_table == "form_template_page_tags":
            if editor:
                table_widget = self.ui.table_editor_ftp_tags
            else:
                table_widget = self.ui.table_ftp_tags
        return table_widget

    def get_data_by_parameters(self, type_table, editor):
        # получение данных
        data = []
        if type_table == "project_tags":
            node_data = self.__osbm.obj_prodb.get_node_data(
                self.obj_projroject.project_node
            )
            print(f"node_data = {node_data}")
            for pair in node_data:
                data.append(self.__osbm.obj_prodb.get_tag_by_id(pair.get("id_tag")))
            print(f"data = {data}")
        elif type_table == "group_tags":
            group_node = self.ui.combox_groups.currentData()
            # проверка на наличия групп
            if group_node:
                node_data = self.__osbm.obj_prodb.get_node_data(group_node)
                for pair in node_data:
                    data.append(self.__osbm.obj_prodb.get_tag_by_id(pair.get("id_tag")))
        elif type_table == "form_template_page_tags":
            page = self.ui.combox_pages.currentData()
            if page is None:
                pass
            elif page == "all_pages":
                template = self.ui.combox_templates.currentData()
                if template:
                    template_data = self.__osbm.obj_prodb.get_template_data(
                        template
                    )
                    for pair in template_data:
                        data.append(
                            self.__osbm.obj_prodb.get_tag_by_id(pair.get("id_tag"))
                        )
            else:
                page_data = self.__osbm.obj_prodb.get_page_data(page)
                for pair in page_data:
                    data.append(
                        self.__osbm.obj_prodb.get_tag_by_id(pair.get("id_tag"))
                    )
        if editor:
            editor_data = []
            cashe = dict()
            for pair in data:
                cashe[pair.get("id_tag")] = pair
            all_data = self.__osbm.obj_prodb.get_project_tags()
            for pair in all_data:
                if cashe.get(pair.get("id_tag")):
                    pair["_checked"] = True
                else:
                    pair["_checked"] = False
                editor_data.append(pair)
            self.__osbm.obj_logg.debug_logger(
                f"TagsListDialogWindow get_data_by_parameters(self, type_table, editor):\ntype_table = {type_table}\neditor = {editor}\neditor_data = {editor_data}"
            )
            return editor_data

        self.__osbm.obj_logg.debug_logger(
            f"TagsListDialogWindow get_data_by_parameters(self, type_table, editor):\ntype_table = {type_table}\neditor = {editor}\ndata = {data}"
        )
        return data

    
    def caf_combobox_form_template_page(self):
        self.__osbm.obj_logg.debug_logger(
            "TagsListDialogWindow caf_combobox_form_template_page()"
        )
        self.caf_combobox_form()
        self.caf_combobox_template()
        self.caf_combobox_page()


    def caf_combobox_group(self):
        self.__osbm.obj_logg.debug_logger(
            "TagsListDialogWindow caf_combobox_group()"
        )
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


    def caf_combobox_form(self):
        self.__osbm.obj_logg.debug_logger(
            "TagsListDialogWindow caf_combobox_form()"
        )
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

    def caf_combobox_template(self):
        self.__osbm.obj_logg.debug_logger(
            "TagsListDialogWindow caf_combobox_template()"
        )
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

    def caf_combobox_page(self):
        self.__osbm.obj_logg.debug_logger(
            "TagsListDialogWindow caf_combobox_page()"
        )
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

    def caf_two_tables(self, type_table):
        """
        Логика такая же, что и в reconfig в других QDialogs.
        """
        self.__osbm.obj_logg.debug_logger(
            f"TagsListDialogWindow caf_two_tables(self, type_table):\ntype_table = {type_table}"
        )
        self.caf_table(type_table, editor=False)
        self.caf_table(type_table, editor=True)

    def config_tws(self):
        self.__osbm.obj_logg.debug_logger(
            "TagsListDialogWindow config_tws()"
        )
        tws_no_editor = [self.ui.table_project_tags, self.ui.table_group_tags, self.ui.table_ftp_tags]
        tws_editor = [self.ui.table_editor_project_tags, self.ui.table_editor_group_tags, self.ui.table_editor_ftp_tags]
        for tw in tws_no_editor:
            self.config_tw(tw, editor=False)
        for tw in tws_editor:
            self.config_tw(tw, editor=True)

    def config_tw(self, table_widget, editor):
        self.__osbm.obj_logg.debug_logger(
            f"TagsListDialogWindow config_tw(self, tw):\ntable_widget = {table_widget}"
        )
        # заголовки/столбцы
        table_widget.verticalHeader().hide()
        if editor:
            headers = ["№", "Тег", "Описание", "Тип", "Вкл", "Действия"]
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
        else:
            headers = ["№", "Тег", "Описание", "Тип"]
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
        table_widget.setSelectionMode(QAbstractItemView.NoSelection)
        # table_widget.sortByColumn(0, Qt.AscendingOrder)
        


    def caf_table(self, type_table, editor=False):
        self.__osbm.obj_logg.debug_logger(
            f"TagsListDialogWindow caf_table(self, type_table, editor):\ntype_table = {type_table}\neditor = {editor}"
        )
        # заполнение таблицы
        table_widget = self.get_table_by_parameters(type_table, editor)
        table_widget.clearContents()
        table_widget.setRowCount(0)
        table_widget.setSortingEnabled(False)
        # данные
        data = self.get_data_by_parameters(type_table, editor)
        header = table_widget.horizontalHeaderItem(0)
        header.setData(1000, data)
        table_widget.setRowCount(len(data))
        for row, item in enumerate(data):
            # получение данных
            if not editor:
                print(f"NOT editor item = {item}")
            order_tag = item.get("order_tag") + 1
            name_tag = item.get("name_tag")
            title_tag = item.get("title_tag")
            type_tag = item.get("type_tag")
            # setData для строки
            qtwt_order_tag = NumericItem(str(order_tag))
            qtwt_order_tag.setData(Qt.UserRole, order_tag)
            qtwt_name_tag = QTableWidgetItem(name_tag)
            qtwt_name_tag.setData(1001, item)
            qtwt_title_tag = QTableWidgetItem(title_tag)
            qtwt_type_tag = QTableWidgetItem(type_tag)
            # Иконка и текст в зависимости от типа тега
            key_icon = self.__osbm.obj_icons.get_key_icon_by_type_tag(type_tag)
            qicon_type_tag = self.__icons.get(key_icon)
            qtwt_type_tag.setIcon(qicon_type_tag)
            qtwt_type_tag.setText(type_tag)
            # Добавляем виджеты в ячейки таблицы
            table_widget.setItem(row, 0, qtwt_order_tag)
            table_widget.setItem(row, 1, qtwt_name_tag)
            table_widget.setItem(row, 2, qtwt_title_tag)
            table_widget.setItem(row, 3, qtwt_type_tag)
            if editor:
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
                edit_button.clicked.connect(partial(self.edit_tag, btn=edit_button))
                delete_button.clicked.connect(
                    partial(self.delete_tag, btn=delete_button, type_table=type_table)
                )
        # включить сортировку после заполнения данных
        table_widget.setSortingEnabled(True)
        table_widget.sortByColumn(0, Qt.AscendingOrder)
        # Изменение размеров столбцов
        table_widget.resizeColumnsToContents()

    def create_tag(self):
        self.__osbm.obj_logg.debug_logger("TagsListDialogWindow create_tag()")
        result = self.ned_tag_dw("create")
        # TODO create_tag - обработать и сохранить изменения в БД
        if result:
            ...
            # получить data
            # обработать и сохранить изменения в БД
            # обновить таблицу

    def edit_tag(self, btn):
        self.__osbm.obj_logg.debug_logger(
            f"TagsListDialogWindow edit_tag(btn):\nbtn = {btn}"
        )
        result = self.ned_tag_dw("edit", btn.custom_data)
        # TODO edit_tag - обработать и сохранить изменения в БД
        if result:
            ...
            # получить data
            # обработать и сохранить изменения в БД
            # обновить таблицу

    def ned_tag_dw(self, type_window, tag=None):
        self.__osbm.obj_nedtdw = nedtagdialogwindow.NedTagDialogWindow(
            self.__osbm, type_window, tag
        )
        result = self.__osbm.obj_nedtdw.exec()
        return result == QDialog.Accepted

    def delete_tag(self, btn, type_table):
        self.__osbm.obj_logg.debug_logger(
            f"TagsListDialogWindow delete_tag(btn, type_table):\nbtn = {btn}\ntype_table = {type_table}"
        )
        name_tag = btn.custom_data.get("name_tag")
        question = self.__osbm.obj_dw.question_message(
            f"Вы действительно хотите удалить этот тег ({name_tag})?"
        )
        if question:
            self.__osbm.obj_prodb.delete_tag(btn.custom_data)
            self.caf_two_tables(type_table)

    def get_current_data_table(self, type_table, editor=False):
        table_widget = self.get_table_by_parameters(type_table, False)
        header = table_widget.horizontalHeaderItem(0)
        data = header.data(1000)
        self.__osbm.obj_logg.debug_logger(
            f"TagsListDialogWindow get_current_data_table(type_table, editor) -> list:\ntype_table = {type_table}\neditor = {editor}\ndata = {data}"
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
            f"TagsListDialogWindow get_new_data_editor_table(type_table) -> list:\ntype_table = {type_table}\nnew_data = {new_data}"
        )
        return new_data

    def save_changes(self):
        self.__osbm.obj_logg.debug_logger("TagsListDialogWindow save_changes()")
        type_table = self.get_typetable()
        # получить данные
        new_data = self.get_new_data_editor_table(type_table)
        old_data = self.get_current_data_table(type_table, editor=False)
        # данные для удаления
        ids_new_data = {item.get("id_tag") for item in new_data}
        data_for_delete = [
            item for item in old_data if item.get("id_tag") not in ids_new_data
        ]
        # данные для добавления
        ids_old_data = {item.get("id_tag") for item in old_data}
        data_for_insert = [
            item for item in new_data if item.get("id_tag") not in ids_old_data
        ]
        # удаление и добавление
        if type_table == "project_tags":
            project_node = self.obj_projroject.project_node
            self.__osbm.obj_prodb.insert_node_datas(project_node, data_for_insert)
            self.__osbm.obj_prodb.delete_node_datas(project_node, data_for_delete)
        elif type_table == "group_tags":
            group_node = self.ui.combox_groups.currentData()
            if group_node:
                self.__osbm.obj_prodb.insert_node_datas(group_node, data_for_insert)
                self.__osbm.obj_prodb.delete_node_datas(group_node, data_for_delete)
        elif type_table == "form_template_page_tags":
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
