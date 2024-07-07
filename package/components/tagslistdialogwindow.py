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


class TagsListDialogWindow(QDialog):
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        self.table_widget = None
        self.buttons = None
        super(TagsListDialogWindow, self).__init__()
        self.ui = tagslistdialogwindow_ui.Ui_TagsListDialog()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        # Подключаем действия
        self.connecting_actions()
        # отобразить первый таб
        self.initalizate_tab_all_tags()

    def connecting_actions(self):
        self.ui.tabwidget.currentChanged.connect(self.on_tab_changed)
        # TODO Сохранить и закрыть

    def on_tab_changed(self, index):
        self.__obs_manager.obj_l.debug_logger(
            f"IN on_tab_changed(self, index): index = {index}"
        )
        if index == 0:
            self.initalizate_tab_all_tags()
        if index == 1:
            self.initalizate_tab_project()
        if index == 2:
            self.initalizate_tab_group()
        if index == 3:
            self.initalizate_tab_template()

    def get_table_by_parameter(self, parameter):
        # получение таблицы
        table_widget = None
        if parameter == "all_tags":
            table_widget = self.ui.table_all_tags
        if parameter == "project_tags":
            table_widget = self.ui.table_project_tags
        if parameter == "group_tags":
            table_widget = self.ui.table_group_tags
        if parameter == "template_tags":
            table_widget = self.ui.table_template_tags
        return table_widget

    def get_data_by_parameter(self, parameter):
        # получение данных
        data = []
        if parameter == "all_tags":
            data = self.__obs_manager.obj_pd.get_project_tag_config()
        elif parameter == "project_tags":
            project_node = self.__obs_manager.obj_pd.get_project_node()
            node_data = self.__obs_manager.obj_pd.get_node_data(
                project_node
            )
            for pair in node_data:
                data += self.__obs_manager.obj_pd.get_tag_config_by_id(pair.get("id_tag"))

        # elif parameter == "group_tags":
        #     list_of_id_node_group = self.__obs_manager.obj_pd.
        # elif parameter == "template_tags":
        #     data = self.__obs_manager.obj_pd.
        return data

    def clear_and_fill_table(self, parameter):
        # заполнение таблицы
        self.table_widget = self.get_table_by_parameter(parameter)
        self.table_widget.clear()
        self.buttons = []
        # заголовки/столбцы
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Тег", "Описание", "Тип", "Действия"])
        # данные
        data = self.get_data_by_parameter(parameter)
        print(f"data = {data}")
        self.table_widget.setRowCount(len(data))
        for row, item in enumerate(data):
            name_tag = item["name_tag"]
            title_tag = item["title_tag"]
            type_tag = item["type_tag"]
            # Добавляем виджеты в ячейки таблицы
            self.table_widget.setItem(row, 0, QTableWidgetItem(name_tag))
            self.table_widget.setItem(row, 1, QTableWidgetItem(title_tag))
            self.table_widget.setItem(row, 2, QTableWidgetItem(type_tag))
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
            self.table_widget.setCellWidget(row, 3, widget)
            # Включение сортировки
            self.table_widget.setSortingEnabled(True)
            # Изменение размеров столбцов
            self.table_widget.resizeColumnsToContents()
            # Запрет на редактирование
            self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
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
        # TODO
        pass

    def initalizate_tab_template(self):
        self.__obs_manager.obj_l.debug_logger("IN initalizate_tab_template()")
        self.ui.tabwidget.setCurrentIndex(3)
        # TODO
        pass
