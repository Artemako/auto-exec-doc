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
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

from functools import partial

import package.components.nedtagdialogwindow as nedtagdialogwindow

import package.ui.tagslistdialogwindow_ui as tagslistdialogwindow_ui

import resources_rc

class Obj:
    pass


class TagsListDialogWindow(QDialog):
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger("IN TagsListDialogWindow(obs_manager)")
        self.initalizate_tabs_objects()
        super(TagsListDialogWindow, self).__init__()
        self.ui = tagslistdialogwindow_ui.Ui_TagsListDialog()
        self.ui.setupUi(self)
        # config
        self.config()
        # Подключаем действия
        self.connecting_actions()
        # отобразить первый таб
        self.show_tab_project()

    def initalizate_tabs_objects(self):
        self.__obs_manager.obj_l.debug_logger("IN initalizate_tabs_objects()")
        self.obj_project = Obj()
        self.obj_group = Obj()
        self.obj_form_template_page = Obj()
        # Списки с данными
        setattr(
            self.obj_project,
            "project_node",
            self.__obs_manager.obj_pd.get_project_node(),
        )
        setattr(
            self.obj_group,
            "list_of_group_node",
            self.__obs_manager.obj_pd.get_group_nodes(),
        )
        setattr(
            self.obj_form_template_page,
            "list_of_form_node",
            self.__obs_manager.obj_pd.get_form_nodes(),
        )
        # TODO

    def config(self):
        self.__obs_manager.obj_l.debug_logger("IN config()")
        self.ui.splitter_ftp.setSizes([500, 300])
        self.ui.splitter_group.setSizes([500, 300])
        self.ui.splitter_project.setSizes([500, 300])

    def connecting_actions(self):
        self.__obs_manager.obj_l.debug_logger("IN connecting_actions()")
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
        # TODO КНОПКИ
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_save.clicked.connect(self.save_changes)
        

    def get_typetable(self):
        self.__obs_manager.obj_l.debug_logger("IN get_typetable()")
        index = self.ui.tabwidget.currentIndex()
        if index == 0:
            return "project_tags"
        elif index == 1:
            return "group_tags"
        elif index == 2:
            return "form_template_page_tags"

    def combox_groups_index_changed(self, index):
        self.__obs_manager.obj_l.debug_logger(
            f"IN combox_groups_index_changed(index):\nindex = {index}"
        )
        # данные таблицы
        typetable = self.get_typetable()
        self.clear_and_fill_two_tables(typetable)


    def combox_forms_index_changed(self, index):
        self.__obs_manager.obj_l.debug_logger(
            f"IN combox_forms_index_changed(index):\nindex = {index}"
        )
        self.clear_and_fill_combobox_template()
        self.clear_and_fill_combobox_page()
        # данные таблицы
        typetable = self.get_typetable()
        self.clear_and_fill_two_tables(typetable)

    def combox_templates_index_changed(self, index):
        self.__obs_manager.obj_l.debug_logger(
            f"IN combox_templates_index_changed(index):\nindex = {index}"
        )
        self.clear_and_fill_combobox_page()
        # данные таблицы
        typetable = self.get_typetable()
        self.clear_and_fill_two_tables(typetable)

    def combox_pages_index_changed(self, index):
        self.__obs_manager.obj_l.debug_logger(
            f"IN combox_pages_index_changed(index):\nindex = {index}"
        )
        # данные таблицы
        typetable = self.get_typetable()
        self.clear_and_fill_two_tables(typetable)

    def show_tab_project(self):
        self.__obs_manager.obj_l.debug_logger("IN show_tab_project()")
        self.ui.tabwidget.setCurrentIndex(0)
        self.clear_and_fill_two_tables("project_tags")

    def show_tab_group(self):
        self.__obs_manager.obj_l.debug_logger("IN show_tab_group()")
        self.ui.tabwidget.setCurrentIndex(1)
        self.clear_and_fill_combobox_group()
        self.clear_and_fill_two_tables("group_tags")
        pass

    def show_tab_form_template_page(self):
        self.__obs_manager.obj_l.debug_logger("IN show_tab_form_template_page()")
        self.ui.tabwidget.setCurrentIndex(2)
        self.clear_and_fill_combobox_form_template_page()
        self.clear_and_fill_two_tables("form_template_page_tags")
        pass

    def on_tab_changed(self, index):
        self.__obs_manager.obj_l.debug_logger(
            f"IN on_tab_changed(self, index):\nindex = {index}"
        )
        if index == 0:
            self.show_tab_project()
        elif index == 1:
            self.show_tab_group()
        elif index == 2:
            self.show_tab_form_template_page()

    def get_table_by_parameters(self, type_table, editor):
        self.__obs_manager.obj_l.debug_logger(
            f"IN get_table_by_parameters(self, type_table, editor):\ntype_table = {type_table}\neditor = {editor}"
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
        self.__obs_manager.obj_l.debug_logger(
            f"IN get_data_by_parameters(self, type_table, editor):\ntype_table = {type_table}\neditor = {editor}"
        )
        # получение данных
        data = []
        if type_table == "project_tags":
            node_data = self.__obs_manager.obj_pd.get_node_data(
                self.obj_project.project_node
            )
            for pair in node_data:
                data += self.__obs_manager.obj_pd.get_tag_config_by_id(
                    pair.get("id_tag")
                )

        elif type_table == "group_tags":
            # TODO ???
            group_node = self.ui.combox_groups.currentData()
            node_data = self.__obs_manager.obj_pd.get_node_data(group_node)
            for pair in node_data:
                data += self.__obs_manager.obj_pd.get_tag_config_by_id(
                    pair.get("id_tag")
                )
        elif type_table == "form_template_page_tags":
            page = self.ui.combox_pages.currentData()
            print(f"page = {page}")
            if page == "all_pages":
                template = self.ui.combox_templates.currentData()
                template_data = self.__obs_manager.obj_pd.get_template_data(template)
                for pair in template_data:
                    data += self.__obs_manager.obj_pd.get_tag_config_by_id(
                        pair.get("id_tag")
                    )
            else:
                page_data = self.__obs_manager.obj_pd.get_page_data(page)
                for pair in page_data:
                    data += self.__obs_manager.obj_pd.get_tag_config_by_id(
                        pair.get("id_tag")
                    )
        if editor:
            editor_data = []
            cashe = dict()
            for pair in data:
                cashe[pair.get("id_tag")] = pair
            all_data = self.__obs_manager.obj_pd.get_project_tag_config_list()
            for pair in all_data:
                if cashe.get(pair.get("id_tag")):
                    pair["_checked"] = True
                else:
                    pair["_checked"] = False
                editor_data.append(pair)
            return editor_data
        return data

    def clear_and_fill_combobox_group(self):
        self.__obs_manager.obj_l.debug_logger("IN clear_and_fill_combobox_group()")
        self.ui.combox_groups.blockSignals(True)
        self.ui.combox_groups.clear()
        for group_node in self.obj_group.list_of_group_node:
            self.ui.combox_groups.addItem(group_node.get("name_node"), group_node)
        self.ui.combox_groups.blockSignals(False)
        self.ui.combox_groups.show()

    def clear_and_fill_combobox_form_template_page(self):
        self.__obs_manager.obj_l.debug_logger(
            "IN clear_and_fill_combobox_form_template_page()"
        )
        self.clear_and_fill_combobox_form()
        self.clear_and_fill_combobox_template()
        self.clear_and_fill_combobox_page()

    def clear_and_fill_combobox_form(self):
        self.__obs_manager.obj_l.debug_logger("IN clear_and_fill_combobox_form()")
        self.ui.combox_forms.blockSignals(True)
        self.ui.combox_forms.clear()
        for form_node in self.obj_form_template_page.list_of_form_node:
            self.ui.combox_forms.addItem(form_node.get("name_node"), form_node)
        self.ui.combox_forms.blockSignals(False)
        self.ui.combox_forms.show()

    def clear_and_fill_combobox_template(self):
        self.__obs_manager.obj_l.debug_logger("IN clear_and_fill_combobox_template()")
        # TODO Для определенного шаблона
        form = self.ui.combox_forms.currentData()
        print(f"form = {form}")
        templates = self.__obs_manager.obj_pd.get_templates_by_form(form)
        print(f"templates = {templates}")
        #
        self.ui.combox_templates.blockSignals(True)
        self.ui.combox_templates.clear()
        for template in templates:
            self.ui.combox_templates.addItem(template.get("name_template"), template)
        self.ui.combox_templates.blockSignals(False)
        self.ui.combox_templates.show()

    def clear_and_fill_combobox_page(self):
        self.__obs_manager.obj_l.debug_logger("IN clear_and_fill_combobox_page()")
        print(f"index = {self.ui.combox_templates.currentIndex()}")
        template = self.ui.combox_templates.currentData()
        print(f"template = {template}")
        pages = self.__obs_manager.obj_pd.get_pages_by_template(template)
        print(f"pages = {pages}")
        #
        self.ui.combox_pages.blockSignals(True)
        self.ui.combox_pages.clear()
        # пункт - Для всех страниц
        self.ui.combox_pages.addItem("- Для всех страниц -", "all_pages")
        for page in pages:
            self.ui.combox_pages.addItem(page.get("page_name"), page)
        self.ui.combox_pages.blockSignals(False)
        self.ui.combox_pages.show()


    def clear_and_fill_two_tables(self, type_table):
        self.__obs_manager.obj_l.debug_logger(
            f"IN clear_and_fill_two_tables(self, type_table):\ntype_table = {type_table}"
        )
        self.clear_and_fill_table(type_table, editor=False)
        self.clear_and_fill_table(type_table, editor=True)


    def clear_and_fill_table(self, type_table, editor=False):
        self.__obs_manager.obj_l.debug_logger(
            f"IN clear_and_fill_table(self, type_table, editor):\ntype_table = {type_table}\neditor = {editor}"
        )
        # заполнение таблицы
        table_widget = self.get_table_by_parameters(type_table, editor)
        table_widget.clear()
        # заголовки/столбцы
        if editor:
            table_widget.setColumnCount(5)
            table_widget.setHorizontalHeaderLabels(["Тег", "Описание", "Тип", "Вкл", "Действия"])
        else:
            table_widget.setColumnCount(3)
            table_widget.setHorizontalHeaderLabels(["Тег", "Описание", "Тип"])
        # данные
        data = self.get_data_by_parameters(type_table, editor)
        header = table_widget.horizontalHeaderItem(0)
        header.setData(1000, data)
        table_widget.setRowCount(len(data))
        for row, item in enumerate(data):
            name_tag = item["name_tag"]
            title_tag = item["title_tag"]
            type_tag = item["type_tag"]
            # setData для строки
            qtwt_name_tag = QTableWidgetItem(name_tag)
            qtwt_name_tag.setData(1001, item)
            # Добавляем виджеты в ячейки таблицы
            table_widget.setItem(row, 0, qtwt_name_tag)
            table_widget.setItem(row, 1, QTableWidgetItem(title_tag))
            table_widget.setItem(row, 2, QTableWidgetItem(type_tag))
            # Настраиваем режимы изменения размера для заголовков
            header = table_widget.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            if editor:
                # checkbox
                checkbtn = QCheckBox(text="вкл.")
                is_checked = item.get("_checked")
                if is_checked is None:
                    is_checked = False
                checkbtn.setChecked(is_checked)
                # Добавляем значение для сортировки
                sort_value = "ДА" if is_checked else "НЕТ"
                table_widget.setItem(row, 3, QTableWidgetItem(sort_value))
                # кнопки
                edit_button = QPushButton()
                qicon_edit_button = QIcon(":/icons/resources/icons/pen.svg")
                qicon_edit_button = qicon_edit_button.pixmap(QSize(16, 16))
                edit_button.setIcon(qicon_edit_button)
                # 
                delete_button = QPushButton()
                qicon_delete_button = QIcon(":/icons/resources/icons/trash.svg")
                qicon_delete_button = qicon_delete_button.pixmap(QSize(16, 16))
                delete_button.setIcon(qicon_delete_button)   
                #             
                edit_button.custom_data = item
                delete_button.custom_data = item
                # добавление кнопок в layout
                layout = QHBoxLayout()
                layout.addWidget(checkbtn)
                layout.addWidget(edit_button)
                layout.addWidget(delete_button)
                layout.setContentsMargins(0, 0, 0, 0)
                widget = QWidget()
                widget.setLayout(layout)
                table_widget.setCellWidget(row, 4, widget)
                # обработчики
                edit_button.clicked.connect(
                    partial(self.edit_tag, btn=edit_button)
                )
                # TODO delete_button
                delete_button.clicked.connect(
                    partial(self.delete_tag, btn=delete_button, type_table=type_table)
                )           
        # Включение сортировки
        table_widget.setSortingEnabled(True)
        # Изменение размеров столбцов
        table_widget.resizeColumnsToContents()
        # Запрет на редактирование
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        # Отключаем возможность выделения
        table_widget.setSelectionMode(QAbstractItemView.NoSelection)


    def create_tag(self):
        self.__obs_manager.obj_l.debug_logger("IN create_tag()")
        self.__obs_manager.obj_nedtdw = nedtagdialogwindow.NedTagDialogWindow(self.__obs_manager, "create")
        self.__obs_manager.obj_nedtdw.exec()

    def edit_tag(self, btn):
        self.__obs_manager.obj_l.debug_logger(f"IN edit_tag(btn):\nbtn = {btn}")
        self.__obs_manager.obj_nedtdw = nedtagdialogwindow.NedTagDialogWindow(self.__obs_manager, "edit", btn.custom_data, )
        self.__obs_manager.obj_nedtdw.exec()

    def delete_tag(self, btn, type_table):
        self.__obs_manager.obj_l.debug_logger(f"IN delete_tag(btn, type_table):\nbtn = {btn}\ntype_table = {type_table}")
        # TODO удаление
        print(f"btn.custom_data = {btn.custom_data}")
        # if type_table == "all_tags":
        #     self.__obs_manager.obj_pd.delete_tag(...)
        #     self.clear_and_fill_two_tables(type_table)
        # else:
        #     self.__obs_manager.obj_pd.delete_tag_from_group(...)
        #     self.clear_and_fill_two_tables(type_table)
       
    def save_changes(self):
        self.__obs_manager.obj_l.debug_logger("IN save_changes()")
        new_data = []
        type_table = self.get_typetable()
        table_widget_editor = self.get_table_by_parameters(type_table, True)
        row_count = table_widget_editor.rowCount()
        for row in range(row_count):
            item = table_widget_editor.item(row, 0).data(1001)
            checked = table_widget_editor.cellWidget(row, 4).findChild(QCheckBox).isChecked()
            if checked:
                item.pop("_checked")
                new_data.append(item)
        # TODO определить куда, удалить и вставить заново
        print(f"new_data = {new_data}")        
        # получить старые данные
        table_widget = self.get_table_by_parameters(type_table, False)
        header = table_widget.horizontalHeaderItem(0)
        old_data = header.data(1000)
        print(f"old_data = {old_data}")
        # if type_table == "project_tags":
            # TODO
            # self.__obs_manager.obj_pd.delete_node_data(self.obj_project.project_node)

        # elif type_table == "group_tags":
        #     # TODO ???
        #     group_node = self.ui.combox_groups.currentData()
        #     node_data = self.__obs_manager.obj_pd.get_node_data(group_node)
        #     for pair in node_data:
        #         data += self.__obs_manager.obj_pd.get_tag_config_by_id(
        #             pair.get("id_tag")
        #         )
        # elif type_table == "form_template_page_tags":
        #     page = self.ui.combox_pages.currentData()
        #     print(f"page = {page}")
        #     if page == "all_pages":
        #         template = self.ui.combox_templates.currentData()
        #         template_data = self.__obs_manager.obj_pd.get_template_data(template)
        #         for pair in template_data:
        #             data += self.__obs_manager.obj_pd.get_tag_config_by_id(
        #                 pair.get("id_tag")
        #             )
        #     else:
        #         page_data = self.__obs_manager.obj_pd.get_page_data(page)
        #         for pair in page_data:
        #             data += self.__obs_manager.obj_pd.get_tag_config_by_id(
        #                 pair.get("id_tag")
        #             )