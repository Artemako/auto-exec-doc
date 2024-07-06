from PySide6.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QPushButton, QCheckBox, QHBoxLayout, QWidget


import package.ui.tagslistdialogwindow_ui as tagslistdialogwindow_ui

class TagsListDialogWindow(QDialog):
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        super(TagsListDialogWindow, self).__init__()
        self.ui = tagslistdialogwindow_ui.Ui_TagsListDialog()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        # Подключаем действия
        self.connecting_actions()
        # отобразить первый таб
        self.initalizate_tab_all_tags()

    def connecting_actions(self):
        # TODO 
        pass

    def initalizate_tab_all_tags(self):
        self.__obs_manager.obj_l.debug_logger("IN initalizate_tab_all_tags()")
        self.ui.tabwidget.setCurrentIndex(0)
        # заполнение таблицы
        table_widget = self.ui.table_all_tags
        table_widget.clear()
        # заголовки/столбцы
        table_widget.setColumnCount(4)
        table_widget.setHorizontalHeaderLabels(
            ["Тег", "Описание", "Тип", "Действия"]
        )
        # данные
        data = self.__obs_manager.obj_pd.get_project_tag_config_list()
        table_widget.setRowCount(len(data))
        for row, item in enumerate(data):
            name_item = QTableWidgetItem(item["name_tag"])
            title_item = QTableWidgetItem(item["title_tag"])
            type_item = QTableWidgetItem(item["type_tag"])
            # Добавляем виджеты в ячейки таблицы
            table_widget.setItem(row, 0, name_item)
            table_widget.setItem(row, 1, title_item)
            table_widget.setItem(row, 2, type_item)
            # кнопки       
            edit_button = QPushButton("Редактировать")
            delete_button = QPushButton("Удалить")   
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
            # edit_button.clicked.connect(self.edit_tag)
            # delete_button.clicked.connect(self.delete_tag)


    def initalizate_tab_project(self):
        self.__obs_manager.obj_l.debug_logger("IN initalizate_tab_project()")
        self.ui.tabwidget.setCurrentIndex(1)

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
