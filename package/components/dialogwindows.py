import os

from PySide6.QtWidgets import QMessageBox, QFileDialog
from PySide6.QtCore import Qt

import package.app as app
import package.modules.dirpathsmanager as dirpathsmanager
import package.modules.log as log


class DialogWindows:

    def save_active_project(self) -> str:
        """Диалоговое окно 'Вы не сохранили текущий проект. Сохранить?'."""

        log.obj_l.debug_logger("IN save_active_project() -> str")

        dialogwindow = QMessageBox()
        dialogwindow.setWindowTitle("Сохранение текущего проекта")
        dialogwindow.setText("Вы не сохранили текущий проект. Сохранить?")
        dialogwindow.setIcon(QMessageBox.Warning)

        dialogwindow.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )

        return_value = dialogwindow.exec()

        log.obj_l.debug_logger(f"save_active_project(): return_value = {return_value}")

        if return_value == QMessageBox.Yes:
            return "Yes"
        elif return_value == QMessageBox.No:
            return "No"
        elif return_value == QMessageBox.Cancel:
            return "Cancel"

    def select_empty_folder(self):
        """Диалоговое окно 'Пожалуйста, выберите пустую папку'."""

        log.obj_l.debug_logger("IN select_empty_folder()")

        dialogwindow = QMessageBox()
        dialogwindow.setWindowTitle("Ошибка")
        dialogwindow.setText("Пожалуйста, выберите пустую папку.")
        dialogwindow.setIcon(QMessageBox.Critical)

        dialogwindow.exec()


    def select_folder_for_new_project(self) -> str:
        """Диалоговое окно выбора папки для нового проекта."""

        log.obj_l.debug_logger("IN select_folder_for_new_project() -> str")

        while True:
            folder_path = QFileDialog.getExistingDirectory(
                None,
                "Выбор папки для нового проекта",
                dirpathsmanager.obj_dpm.get_default_folder_projects_dirpath(),
            )
            if folder_path:
                if not os.listdir(folder_path):
                    log.obj_l.debug_logger(
                        f"select_folder_for_new_project() -> {folder_path}"
                    )
                    return folder_path
                else:
                    self.select_empty_folder()
            else:
                log.obj_l.debug_logger(f"select_folder_for_new_project() -> {None}")
                return None


    def select_folder_for_open_project(self) -> str:
        """Диалоговое окно выбора папки для открытия проекта."""
        while True:
            folder_path = QFileDialog.getOpenFileName(
                None,
                "Выбор aed файла проекта для его открытия",
                dirpathsmanager.obj_dpm.get_default_folder_projects_dirpath(),
                "Project files (*.aed)"
            )
            if folder_path[0]:
                log.obj_l.debug_logger(
                    f"select_folder_for_open_project() -> {folder_path[0]}"
                )
                return os.path.dirname(folder_path[0])
            else:
                log.obj_l.debug_logger(f"select_folder_for_open_project() -> {None}")
                return None



    def select_image_for_formimage_in_project(self) -> str:
        """Диалоговое окно выбора изображения для формы."""

        log.obj_l.debug_logger("IN select_image_for_formimage_in_project() -> str")
        while True:
            image_path = QFileDialog.getOpenFileName(
                None,
                "Выбор изображения",
                dirpathsmanager.obj_dpm.get_default_folder_projects_dirpath(),
                "Изображения (*.png *.jpg *.jpeg, *.bmp, *.tiff)",
            )
            if image_path[0]:
                log.obj_l.debug_logger(
                    f"select_image_for_formimage_in_project() -> {image_path[0]}"
                )
                return image_path[0]
            else:
                log.obj_l.debug_logger(
                    f"select_image_for_formimage_in_project() -> {None}"
                )
                return None
            
    

    def warning_message(self, message: str):
        """Диалоговое окно 'Предупреждение'."""

        log.obj_l.debug_logger("IN warning_message(message: str)")
        dialogwindow = QMessageBox()
        dialogwindow.setWindowTitle("Предупреждение")
        dialogwindow.setText(message)
        dialogwindow.setIcon(QMessageBox.Warning)

        dialogwindow.exec()


    def select_name_and_dirpath_export_pdf(self) -> str:
        """Диалоговое окно 'Выберите имя и путь для экспорта в PDF'."""

        log.obj_l.debug_logger("IN select_name_and_dirpath_export_pdf() -> str")

        while True:
            multipage_pdf_path = QFileDialog.getSaveFileName(
                None,
                "Выберите имя и путь для экспорта в PDF",
                dirpathsmanager.obj_dpm.get_default_folder_projects_dirpath(),
                "PDF (*.pdf)",
            )
            if multipage_pdf_path[0]:
                log.obj_l.debug_logger(
                    f"select_name_and_dirpath_export_pdf() -> {multipage_pdf_path[0]}"
                )
                return multipage_pdf_path[0]
            else:
                log.obj_l.debug_logger(
                    f"select_name_and_dirpath_export_pdf() -> {None}"
                )
                return None
            

obj_dw = DialogWindows()