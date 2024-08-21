from PySide6.QtWidgets import (
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QHeaderView,
)

import package.ui.nedpagedialogwindow_ui as nedpagedialogwindow_ui

import package.components.dialogwindow.neddw.nedvariabledialogwindow as nedvariabledialogwindow

import json
import os
import datetime
from docxtpl import DocxTemplate
from functools import partial


class NedPageDialogWindow(QDialog):
    def __init__(self, osbm, type_ned, pages, page=None):
        self.__osbm = osbm
        self.__type_ned = type_ned
        self.__pages = pages
        self.__page = page
        self.__osbm.obj_logg.debug_logger(
            f"NedPageDialogWindow __init__(osbm, type_ned, page):\ntype_ned = {self.__type_ned}\npages = {self.__pages}\npage = {self.__page}"
        )
        super(NedPageDialogWindow, self).__init__()
        self.ui = nedpagedialogwindow_ui.Ui_NedPageDialogWindow()
        self.ui.setupUi(self)
        # СТИЛЬ
        self.__osbm.obj_style.set_style_for(self)
        #
        self.__select_filename = str()
        self.__temp_copy_file_path = str()
        self.__data = {
            "TEMP_COPY_FILE_PATH": None,
            "id_parent_template": None,
            "name_page": None,
            "filename_page": None,
            "order_page": None,
            "included": 1,
        }
        self.__variables_for_add = []
        # одноразовые действия
        self.config_by_type_window()
        self.config_combox_neighboor()
        self.reconfig_tw_variables()
        self.connecting_actions()

    def get_data(self):
        self.__osbm.obj_logg.debug_logger(
            f"NedPageDialogWindow get_data():\nself.__data = {self.__data}"
        )
        return self.__data

    def connecting_actions(self):
        self.__osbm.obj_logg.debug_logger("NedPageDialogWindow connecting_actions()")
        self.ui.btn_select.clicked.connect(self.select_new_file)
        self.ui.btn_open_docx.setShortcut("Ctrl+O")
        self.ui.btn_open_docx.clicked.connect(self.open_edit_docx)
        self.ui.btn_open_docx.setShortcut("Ctrl+E")
        self.ui.btn_nedvariable.clicked.connect(self.btn_nedvariable_clicked)
        self.ui.btn_nedvariable.setShortcut("Ctrl+S")
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_close.setShortcut("Ctrl+Q")
        self.ui.btn_findvariables.clicked.connect(self.reconfig_tw_variables)
        self.ui.btn_findvariables.setShortcut("Ctrl+F")

    def config_by_type_window(self):
        self.__osbm.obj_logg.debug_logger("NedPageDialogWindow config_by_type_window()")
        if self.__type_ned == "create":
            self.ui.btn_select.setText("Выбрать документ")
            self.ui.label_file.setText("Файл не выбран")
            self.ui.btn_nedvariable.setText("Добавить страницу")
            self.ui.btn_open_docx.setEnabled(False)
        elif self.__type_ned == "edit":
            self.ui.btn_select.setText("Выбрать документ")
            self.ui.label_file.setText("Файл выбран")
            self.ui.btn_nedvariable.setText("Сохранить страницу")
            self.ui.lineedit_namepage.setText(self.__page.get("name_page"))
            # Создать копию для редактирования
            self.do_temp_copy_for_edit(self.__page.get("filename_page"))
            self.ui.btn_open_docx.setEnabled(True)

    def reconfig_tw_variables(self):
        self.__osbm.obj_logg.debug_logger("NedPageDialogWindow reconfig_tw_variables()")
        tablewidget = self.ui.tw_variables
        tablewidget.blockSignals(True)
        tablewidget.clearContents()
        tablewidget.setRowCount(0)
        # если выбран временный файл
        if self.__temp_copy_file_path:
            jinja_variables = self.extract_jinja_variables(self.__temp_copy_file_path)
            if jinja_variables:
                self.fill_tw_variables(jinja_variables)
        # если выбран основной файл
        # elif self.__select_filename:
        #     forms_folder_dirpath = self.__osbm.obj_dirm.get_forms_folder_dirpath()
        #     docx_path = os.path.join(
        #         forms_folder_dirpath, self.__select_filename + ".docx"
        #     )
        #     jinja_variables = self.extract_jinja_variables(docx_path)
        #     if jinja_variables:
        #         self.fill_tw_variables(jinja_variables)
        tablewidget.blockSignals(False)

    def fill_tw_variables(self, jinja_variables):
        # TODO ПЕРЕДЕЛАТЬ
        self.__osbm.obj_logg.debug_logger(
            f"NedPageDialogWindow fill_tw_variables(jinja_variables):\njinja_variables = {jinja_variables}"
        )
        tablewidget = self.ui.tw_variables
        tablewidget.setColumnCount(2)
        tablewidget.setHorizontalHeaderLabels(["Переменная", "Действия"])
        tablewidget.setRowCount(len(jinja_variables))
        for row, name_variable in enumerate(jinja_variables):
            qtwt_name_variable = QTableWidgetItem(name_variable)
            tablewidget.setItem(row, 0, qtwt_name_variable)
            # кнопка действия
            layout = QHBoxLayout()
            add_button = QPushButton("...")
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(add_button)
            widget = QWidget()
            widget.setLayout(layout)
            #
            result_bd = self.__osbm.obj_prodb.get_variable_by_name(name_variable)
            result_variables_for_add = self.get_variable_by_name(name_variable)
            if result_bd or result_variables_for_add:
                tablewidget.setItem(row, 1, QTableWidgetItem("Имеется"))
            else:
                add_button.setText("Добавить переменную")
                add_button.clicked.connect(
                    partial(self.add_variable, name_variable, False)
                )
                tablewidget.setCellWidget(row, 1, widget)
        # Настраиваем режимы изменения размера для заголовков
        header = tablewidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        #
        tablewidget.setSortingEnabled(True)
        tablewidget.resizeColumnsToContents()
        tablewidget.setEditTriggers(QTableWidget.NoEditTriggers)
        tablewidget.setSelectionMode(QAbstractItemView.NoSelection)

    def get_variable_by_name(self, name_variable) -> dict:
        self.__osbm.obj_logg.debug_logger(
            f"NedPageDialogWindow get_variable_by_name(name_variable) -> dict:\nname_variable = {name_variable}"
        )
        variables = self.__variables_for_add
        result = None
        for variable in variables:
            if variable.get("name_variable") == name_variable:
                result = variable
                break
        return result

    def add_variable(self, name_variable, is_block):
        # TODO Traceback (most recent call last):
#   File "d:\work\project\AutoExecDoc\package\components\dialogwindow\neddw\nedpagedialogwindow.py", line 173, in add_variable
# 2024-08-21 23:23:02,559 - DEBUG -  ProjectDatabase get_conn() -> object
#     self.__osbm.obj_nedtdw = nedvariabledialogwindow.NedVariableDialogWindow(
# TypeError: __init__() takes from 4 to 6 positional arguments but 7 were given
        """
        Похожий код у VariablesListDialogWindow.
        """
        self.__osbm.obj_logg.debug_logger(
            f"NedPageDialogWindow add_variable(variable, name_variable, is_block):\nname_variable = {name_variable}\n is_block = {is_block}"
        )
        #
        self.__all_variables = self.__osbm.obj_prodb.get_variables()
        # окно
        self.__osbm.obj_nedtdw = nedvariabledialogwindow.NedVariableDialogWindow(
            self.__osbm, "create", self.__all_variables, None, name_variable, is_block
        )
        result = self.__osbm.obj_nedtdw.exec()
        # результат
        if result == QDialog.Accepted:
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
            # обновляем таблицу
            self.reconfig_tw_variables()

    def extract_jinja_variables(self, docx_path) -> set:
        self.__osbm.obj_logg.debug_logger(
            f"NedPageDialogWindow extract_jinja_variables(docx_path) -> set:\ndocx_path = {docx_path}"
        )
        try:
            docx_template = DocxTemplate(docx_path)
            set_of_variables = docx_template.get_undeclared_template_variables()
            return set_of_variables
        except Exception as error:
            self.__osbm.obj_logg.error_logger(
                f"NedPageDialogWindow extract_jinja_variables(docx_path) -> set:\nerror = {error}"
            )
            self.__osbm.obj_dw.warning_message(
                f"Ошибка в поиске переменных в выбранном документе:\n{error}"
            )
            return set()

    def config_combox_neighboor(self):
        self.__osbm.obj_logg.debug_logger(
            "NedPageDialogWindow config_combox_neighboor()"
        )
        combobox = self.ui.combox_neighboor
        combobox.blockSignals(True)
        combobox.clear()
        current_index = 0
        # по умолчанию - в конец
        flag = True
        combobox.addItem("- В начало -", "START")
        for index, page in enumerate(self.__pages):
            if self.__page and self.__page.get("id_page") == page.get("id_page"):
                flag = False
            else:
                combobox.addItem(page.get("name_page"), page)
            if flag:
                current_index = index + 1
        combobox.setCurrentIndex(current_index)
        combobox.blockSignals(False)

    def do_temp_copy_for_edit(self, old_filename_page):
        self.__osbm.obj_logg.debug_logger("NedPageDialogWindow do_copy_for_edit()")
        # образуем новое название документа
        file_name = f"docx_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        self.__select_filename = file_name
        file_name_with_docx = f"{file_name}.docx"
        # edit документ - как бы старый
        forms_folder_dirpath = self.__osbm.obj_dirm.get_forms_folder_dirpath()
        old_docx_path = os.path.join(
            forms_folder_dirpath, old_filename_page + ".docx"
        )
        # временный - как бы новый
        temp_dir = self.__osbm.obj_dirm.get_temp_dirpath()
        self.__temp_copy_file_path = os.path.join(temp_dir, file_name_with_docx)
        # копирование
        self.__osbm.obj_film.copy_file(old_docx_path, self.__temp_copy_file_path)


    def select_new_file(self):
        self.__osbm.obj_logg.debug_logger("NedPageDialogWindow select_new_file()")
        docx_path = self.__osbm.obj_dw.select_docx_file()
        if docx_path:
            # текст
            self.ui.label_file.setText("Файл выбран")
            # образуем новое название документа
            file_name = f"docx_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
            self.__select_filename = file_name
            file_name_with_docx = f"{file_name}.docx"
            # пути + копирование
            temp_dir = self.__osbm.obj_dirm.get_temp_dirpath()
            self.__temp_copy_file_path = os.path.join(temp_dir, file_name_with_docx)
            self.__osbm.obj_film.copy_file(docx_path, self.__temp_copy_file_path)
            # файл выбран
            self.ui.btn_open_docx.setEnabled(True)
            self.reconfig_tw_variables()

    
    def open_edit_docx(self):
        self.__osbm.obj_logg.debug_logger("NedPageDialogWindow open_edit_docx()")
        try:
            # путь к документу
            docx_path = self.__temp_copy_file_path
            # открытие
            if os.path.exists(docx_path):
                try:
                    os.startfile(docx_path)
                except OSError:
                    raise Exception("Не удалось открыть.")
        except Exception as e:
            self.__osbm.obj_logg.error_logger(e)
            self.__osbm.obj_dw.warning_message("Не удалось открыть документ")

    def find_page_by_namepage_in_pages(self, namepage) -> object:
        self.__osbm.obj_logg.debug_logger(
            f"NedPageDialogWindow find_page_by_namepage_in_pages(namepage):\nnamepage = {namepage}"
        )
        for current_page in self.__pages:
            if current_page.get("name_page") == namepage:
                return current_page
        return None

    def btn_nedvariable_clicked(self):
        self.__osbm.obj_logg.debug_logger(
            "NedPageDialogWindow btn_nedvariable_clicked()"
        )

        select_filename_page = self.__select_filename
        namepage = self.ui.lineedit_namepage.text()
        if len(namepage) > 0 and len(select_filename_page) > 0:
            # поиск по имени
            find_page = self.find_page_by_namepage_in_pages(namepage)
            # выбранный сосед
            neighboor_page = self.ui.combox_neighboor.currentData()
            order_page = (
                0 if neighboor_page == "START" else neighboor_page.get("order_page") + 1
            )
            #
            if self.__type_ned == "create":
                if find_page is None:
                    self.__data["name_page"] = namepage
                    self.__data["filename_page"] = select_filename_page
                    self.__data["order_page"] = order_page
                    self.__data["TEMP_COPY_FILE_PATH"] = self.__temp_copy_file_path
                    self.accept()
                else:
                    msg = "Другая страница с таким именем уже существует!"
                    self.__osbm.obj_dw.warning_message(msg)

            elif self.__type_ned == "edit":
                if find_page is None:
                    self.__data = self.__page
                    self.__data["name_page"] = namepage
                    self.__data["filename_page"] = select_filename_page
                    self.__data["order_page"] = order_page
                    self.__data["TEMP_COPY_FILE_PATH"] = self.__temp_copy_file_path
                    self.accept()
                elif namepage == self.__page.get("name_page"):
                    self.__data = self.__page
                    self.__data["name_page"] = namepage
                    self.__data["filename_page"] = select_filename_page
                    self.__data["order_page"] = order_page
                    self.__data["TEMP_COPY_FILE_PATH"] = self.__temp_copy_file_path
                    self.accept()
                else:
                    msg = "Другая страница с таким именем уже существует!"
                    self.__osbm.obj_dw.warning_message(msg)
        elif namepage == "":
            self.__osbm.obj_dw.warning_message("Заполните поле названия")
        elif select_filename_page is None or len(select_filename_page) == 0:
            self.__osbm.obj_dw.warning_message("Выберите документ")
        else:
            self.__osbm.obj_dw.warning_message(
                "Заполните поле названия и выберите документ"
            )
