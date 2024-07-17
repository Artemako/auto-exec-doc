from PySide6.QtWidgets import (
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QPushButton,
    QCheckBox,
    QHBoxLayout,
    QWidget,
)

from functools import partial

import package.components.nedtagdialogwindow as nedtagdialogwindow

import package.ui.tagslistdialogwindow_ui as tagslistdialogwindow_ui

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
        # Подключаем действия
        self.connecting_actions()
        # отобразить первый таб
        self.show_tab_all_tags()

    def initalizate_tabs_objects(self):
        self.__obs_manager.obj_l.debug_logger("IN initalizate_tabs_objects()")
        self.obj_all = Obj()
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
        self.ui.btn_add_tag_to_group
        self.ui.btn_add_tag_to_project
        self.ui.btn_add_tag_to_template_or_page
        self.ui.btn_close
        # создать новый тег
        self.ui.btn_create_tag.clicked.connect(
            self.create_tag
        )
        self.ui.btn_save
        

    def get_typetable(self):
        self.__obs_manager.obj_l.debug_logger("IN get_typetable()")
        index = self.ui.tabwidget.currentIndex()
        if index == 0:
            return "all_tags"
        elif index == 1:
            return "project_tags"
        elif index == 2:
            return "group_tags"
        elif index == 3:
            return "form_template_page_tags"

    def combox_groups_index_changed(self, index):
        self.__obs_manager.obj_l.debug_logger(
            f"IN combox_groups_index_changed(index):\nindex = {index}"
        )
        # данные таблицы
        typetable = self.get_typetable()
        self.clear_and_fill_table(typetable)


    def combox_forms_index_changed(self, index):
        self.__obs_manager.obj_l.debug_logger(
            f"IN combox_forms_index_changed(index):\nindex = {index}"
        )
        self.clear_and_fill_combobox_template()
        self.clear_and_fill_combobox_page()
        # данные таблицы
        typetable = self.get_typetable()
        self.clear_and_fill_table(typetable)

    def combox_templates_index_changed(self, index):
        self.__obs_manager.obj_l.debug_logger(
            f"IN combox_templates_index_changed(index):\nindex = {index}"
        )
        self.clear_and_fill_combobox_page()
        # данные таблицы
        typetable = self.get_typetable()
        self.clear_and_fill_table(typetable)

    def combox_pages_index_changed(self, index):
        self.__obs_manager.obj_l.debug_logger(
            f"IN combox_pages_index_changed(index):\nindex = {index}"
        )
        # данные таблицы
        typetable = self.get_typetable()
        self.clear_and_fill_table(typetable)

    def show_tab_all_tags(self):
        self.__obs_manager.obj_l.debug_logger("IN show_tab_all_tags()")
        self.ui.tabwidget.setCurrentIndex(0)
        self.clear_and_fill_table("all_tags")

    def show_tab_project(self):
        self.__obs_manager.obj_l.debug_logger("IN show_tab_project()")
        self.ui.tabwidget.setCurrentIndex(1)
        self.clear_and_fill_table("project_tags")

    def show_tab_group(self):
        self.__obs_manager.obj_l.debug_logger("IN show_tab_group()")
        self.ui.tabwidget.setCurrentIndex(2)
        self.clear_and_fill_combobox_group()
        self.clear_and_fill_table("group_tags")
        pass

    def show_tab_form_template_page(self):
        self.__obs_manager.obj_l.debug_logger("IN show_tab_form_template_page()")
        self.ui.tabwidget.setCurrentIndex(3)
        self.clear_and_fill_combobox_form_template_page()
        self.clear_and_fill_table("form_template_page_tags")
        pass

    def on_tab_changed(self, index):
        self.__obs_manager.obj_l.debug_logger(
            f"IN on_tab_changed(self, index):\nindex = {index}"
        )
        if index == 0:
            self.show_tab_all_tags()
        elif index == 1:
            self.show_tab_project()
        elif index == 2:
            self.show_tab_group()
        elif index == 3:
            self.show_tab_form_template_page()

    def get_table_by_parameter(self, type_table):
        self.__obs_manager.obj_l.debug_logger(
            f"IN get_table_by_parameter(self, type_table):\ntype_table = {type_table}"
        )
        # получение таблицы
        table_widget = None
        if type_table == "all_tags":
            table_widget = self.ui.table_all_tags
        elif type_table == "project_tags":
            table_widget = self.ui.table_project_tags
        elif type_table == "group_tags":
            table_widget = self.ui.table_group_tags
        elif type_table == "form_template_page_tags":
            table_widget = self.ui.table_form_template_page_tags
        return table_widget

    def get_data_by_parameter(self, type_table):
        self.__obs_manager.obj_l.debug_logger(
            f"IN get_data_by_parameter(self, type_table):\ntype_table = {type_table}"
        )
        # получение данных
        data = []
        if type_table == "all_tags":
            data = self.__obs_manager.obj_pd.get_project_tag_config()
        elif type_table == "project_tags":
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

    def clear_and_fill_table(self, type_table):
        self.__obs_manager.obj_l.debug_logger(
            f"IN clear_and_fill_table(self, type_table):\ntype_table = {type_table}"
        )
        # заполнение таблицы
        table_widget = self.get_table_by_parameter(type_table)
        table_widget.clear()
        # заголовки/столбцы
        table_widget.setColumnCount(4)
        table_widget.setHorizontalHeaderLabels(["Тег", "Описание", "Тип", "Действия"])
        # данные
        data = self.get_data_by_parameter(type_table)
        print(f"data = {data}")
        table_widget.setRowCount(len(data))
        for row, item in enumerate(data):
            name_tag = item["name_tag"]
            title_tag = item["title_tag"]
            type_tag = item["type_tag"]
            # Добавляем виджеты в ячейки таблицы
            table_widget.setItem(row, 0, QTableWidgetItem(name_tag))
            table_widget.setItem(row, 1, QTableWidgetItem(title_tag))
            table_widget.setItem(row, 2, QTableWidgetItem(type_tag))
            # кнопки
            edit_button = QPushButton("Редактировать")
            delete_button = QPushButton()
            if type_table == "all_tags":
                delete_button.setText("Удалить")
            else:
                delete_button.setText("Убрать")
            edit_button.custom_data = item
            delete_button.custom_data = item
            # добавление кнопок в layout
            layout = QHBoxLayout()
            layout.addWidget(edit_button)
            layout.addWidget(delete_button)
            layout.setContentsMargins(0, 0, 0, 0)
            widget = QWidget()
            widget.setLayout(layout)
            table_widget.setCellWidget(row, 3, widget)
            # Включение сортировки
            table_widget.setSortingEnabled(True)
            # Изменение размеров столбцов
            table_widget.resizeColumnsToContents()
            # Запрет на редактирование
            table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
            # Отключаем возможность выделения
            table_widget.setSelectionMode(QAbstractItemView.NoSelection)
            # table_widget событий
            # TODO Обработчики кнопок
            edit_button.clicked.connect(
                partial(self.edit_tag, btn=edit_button)
            )
            delete_button.clicked.connect(
                partial(self.delete_tag, btn=delete_button, type_table=type_table)
            )

    def create_tag(self):
        self.__obs_manager.obj_l.debug_logger("IN create_tag()")
        self.__obs_manager.obj_nedtdw = nedtagdialogwindow.NedTagDialogWindow(self.__obs_manager, "create")
        self.__obs_manager.obj_nedtdw.exec()

    def add_tag(self):
        # TODO ОКНО добавления
        ...

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
        #     self.clear_and_fill_table(type_table)
        # else:
        #     self.__obs_manager.obj_pd.delete_tag_from_group(...)
        #     self.clear_and_fill_table(type_table)
       
