from PySide6.QtWidgets import (
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QCheckBox,
    QHBoxLayout,
    QWidget,
)

from functools import partial

import package.ui.tagslistdialogwindow_ui as tagslistdialogwindow_ui

def find_in_list_of_dicts(list_of_dicts, key, value): 
    for data in list_of_dicts:
        if data.get(key) == value:
            return data
    return None

class Obj:
    pass

class TagsListDialogWindow(QDialog):
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        self.initalizate_tabs_objects()
        super(TagsListDialogWindow, self).__init__()
        self.ui = tagslistdialogwindow_ui.Ui_TagsListDialog()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)       
        # Подключаем действия
        self.connecting_actions()
        # отобразить первый таб
        self.initalizate_tab_all_tags()

    def initalizate_tabs_objects(self):
        self.obj_all = Obj()
        self.obj_project = Obj()
        self.obj_group = Obj()
        self.obj_form_template_page = Obj()
        setattr(self.obj_project, "project_node", self.__obs_manager.obj_pd.get_project_node())
        setattr(self.obj_group, "list_of_group_node", self.__obs_manager.obj_pd.get_group_nodes())
        # setattr(self.obj_template, "list_of_templates")
        # TODO Другая логика

    def connecting_actions(self):
        self.ui.combox_groups.currentIndexChanged.connect(self.combox_groups_index_changed)
        self.ui.tabwidget.currentChanged.connect(self.on_tab_changed)        
        # TODO Сохранить и закрыть


    def combox_groups_index_changed(self, index):
        # TODO
        pass


    def on_tab_changed(self, index):
        # self.__obs_manager.obj_l.debug_logger(
        #     f"IN on_tab_changed(self, index): index = {index}"
        # )
        if index == 0:
            self.initalizate_tab_all_tags()
        elif index == 1:
            self.initalizate_tab_project()
        elif index == 2:
            self.initalizate_tab_group()
        elif index == 3:
            self.initalizate_tab_form_template_page()

    def get_table_by_parameter(self, type_table):
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

    def get_data_by_parameter(self, type_table, combox_first_id_node = None, combox_second = None):
        # получение данных
        data = []
        if type_table == "all_tags":
            data = self.__obs_manager.obj_pd.get_project_tag_config()
        elif type_table == "project_tags":
            node_data = self.__obs_manager.obj_pd.get_node_data(
                self.obj_project.project_node
            )
            for pair in node_data:
                data += self.__obs_manager.obj_pd.get_tag_config_by_id(pair.get("id_tag"))

        elif type_table == "group_tags":
            group_node = self.get_group_node(combox_first_id_node)
            node_data = self.__obs_manager.obj_pd.get_node_data(
                group_node
            )
            for pair in node_data:
                data += self.__obs_manager.obj_pd.get_tag_config_by_id(pair.get("id_tag"))
            
        # elif parameter == "form_template_page_tags":
        #     data = self.__obs_manager.obj_pd.
        return data

    def get_group_node(self, combox_first_id_node):
        group_node = None
        if combox_first_id_node:
            group_node = find_in_list_of_dicts(self.obj_group.list_of_group_node, "id_node", combox_first_id_node)
        else:
            group_node = self.obj_group.list_of_group_node[0]
        return group_node

    
    def clear_and_fill_combobox_group(self):
        combobox = self.ui.combox_groups
        combobox.clear()
        for group_node in self.obj_group.list_of_group_node:
            print(f"group_node = {group_node}")
            combobox.addItem(group_node.get("name_node"))
        combobox.show()

    # def clear_and_fill_combobox_form_template_page(self):
    #     # TODO
    #     combobox = self.ui.combox_
    #     combobox.clear()
    #     for form_template_page_node in self.obj_
    #         print(f"group_node = {group_node}")
    #         combobox.addItem(group_node.get("name_node"))
    #     combobox.show()

    #     combobox = self.ui.combox_pages
    #     combobox.clear()


    def clear_and_fill_table(self, type_table, par1 = None, par2 = None):
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
            delete_button = QPushButton("Удалить")
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
            # Обработчики событий
            # TODO Обработчики кнопок
            edit_button.clicked.connect(partial(self.print_custom_data, btn=edit_button))
            delete_button.clicked.connect(partial(self.print_custom_data, btn=delete_button))

   
    def print_custom_data(self, btn):
        print(btn.custom_data)


    def initalizate_tab_all_tags(self):
        self.__obs_manager.obj_l.debug_logger("IN initalizate_tab_all_tags()")
        self.ui.tabwidget.setCurrentIndex(0)
        self.clear_and_fill_table("all_tags")

    def initalizate_tab_project(self):
        self.__obs_manager.obj_l.debug_logger("IN initalizate_tab_project()")
        self.ui.tabwidget.setCurrentIndex(1)
        self.clear_and_fill_table("project_tags")

    def initalizate_tab_group(self):
        self.__obs_manager.obj_l.debug_logger("IN initalizate_tab_group()")
        self.ui.tabwidget.setCurrentIndex(2)
                    # TODO combobox
        self.clear_and_fill_combobox_group()
        self.clear_and_fill_table("group_tags")
        pass

    def initalizate_tab_form_template_page(self):
        self.__obs_manager.obj_l.debug_logger("IN initalizate_tab_form_template_page()")
        self.ui.tabwidget.setCurrentIndex(3)
                    # TODO combobox
        self.clear_and_fill_combobox_form_template_page()
        self.clear_and_fill_table("template_tags")
        pass
