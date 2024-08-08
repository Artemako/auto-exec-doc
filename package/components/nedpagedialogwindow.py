from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QTimer, QSize
from PySide6.QtGui import QIcon

import package.ui.nedpagedialogwindow_ui as nedpagedialogwindow_ui

import os
import datetime
import subprocess

class NedPageDialogWindow(QDialog):
    def __init__(self, obs_manager, type_ned, page=None):
        self.__obs_manager = obs_manager
        self.__type_ned = type_ned
        self.__page = page
        self.__obs_manager.obj_l.debug_logger(
            f"NedPageDialogWindow __init__(obs_manager, type_ned, page):\ntype_ned = {self.__type_ned}\npage = {self.__page}"
        )
        super(NedPageDialogWindow, self).__init__()
        self.ui = nedpagedialogwindow_ui.Ui_NedPageDialogWindow()
        self.ui.setupUi(self)
        #
        self.__page_filename = None
        self.__data = {
            "id_parent_template": None,
            "name_page": None,
            "filename_page": None,
            "order_page": None,
            "included": 1,
        }
        self.__icons = self.__obs_manager.obj_gf.get_icons()
        # одноразовые действия
        self.config_by_type_window()
        self.connecting_actions()

    def config_by_type_window(self):
        self.__obs_manager.obj_l.debug_logger("NedPageDialogWindow config_by_type_window()")
        if self.__type_ned == "create":
            self.ui.btn_select.setText("Выбрать документ")
            self.ui.btn_open_in_folder.setEnabled(False)
            self.ui.label_file.setText("Файл не выбран")
            self.ui.btn_nestag.setText("Добавить страницу")
            self.ui.btn_nestag.setIcon(self.__icons.get("qicon_add"))
        elif self.__type_ned == "edit":
            self.ui.btn_select.setText("Выбрать новый документ")
            self.ui.btn_open_in_folder.setEnabled(True)
            self.ui.label_file.setText(self.__page.get("filename_page"))
            self.ui.btn_nestag.setText("Сохранить страницу")
            self.ui.btn_nestag.setIcon(self.__icons.get("qicon_save"))
        # TODO ORDER
        # TODO TAGS

    def connecting_actions(self):
        self.__obs_manager.obj_l.debug_logger("NedPageDialogWindow connecting_actions()")
        self.ui.btn_select.clicked.connect(self.select_file)
        self.ui.btn_open_in_folder.clicked.connect(self.open_in_folder)
        self.ui.btn_nestag.clicked.connect(self.btn_nestag_clicked)
        self.ui.btn_close.clicked.connect(self.close)

    def select_file(self):
        docx_path = self.__obs_manager.obj_dw.select_docx_file()
        if docx_path:
            # текст
            self.ui.label_file.setText(os.path.basename(docx_path))
            #
            file_name = f"docx_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            self.__page_filename = file_name
            file_name_with_docx = f"{file_name}.docx"
            # путь к временной папке
            temp_dir = self.__obs_manager.obj_dpm.get_temp_dirpath()
            # путь к временному файлу
            temp_file_path = os.path.join(temp_dir, file_name_with_docx)
            # копирование
            self.__obs_manager.obj_dpm.copy_file(docx_path, temp_file_path)

    def open_in_folder(self):
        self.__obs_manager.obj_l.debug_logger("NedPageDialogWindow open_in_folder()")
        # docx_path = self.__page.get("filename_page")
        # # TODO УЗНАТЬ ПУТЬ К ДОКУМЕНТУ ЧЕРЕЗ ШАБЛОН 
        # subprocess.Popen(f"explorer /select, {docx_path}")

    def btn_nestag_clicked(self):
        self.__obs_manager.obj_l.debug_logger("NedPageDialogWindow btn_nestag_clicked()")
        if self.__type_ned == "create":
            filenamepage = self.__page_filename 
            namepage = self.ui.lineedit_namepage.text()
            if len(namepage) > 0 and len(filenamepage) > 0:
                self.__data["name_page"] = namepage
                self.__data["filename_page"] = filenamepage
                self.accept()
            elif namepage == "":
                self.__obs_manager.obj_dw.warning_message("Заполните поле названия")
            elif len(filenamepage) == 0:
                self.__obs_manager.obj_dw.warning_message("Выберите документ")
            else:
                self.__obs_manager.obj_dw.warning_message("Заполните поле названия и выберите документ")
        elif self.__type_ned == "edit":
            self.__data = self.__page
            # TODO edit
