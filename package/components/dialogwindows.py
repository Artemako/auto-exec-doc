import os

from PySide6.QtWidgets import QMessageBox, QFileDialog

import package.app as app
import package.modules.dirpathsmanager as dirpathsmanager
import package.modules.log as log


class DialogWindows:
    @staticmethod
    def save_active_project() -> str:
        """Диалоговое окно 'Вы не сохранили текущий проект. Сохранить?'."""

        log.Log.debug_logger("IN save_active_project() -> str")

        dialogwindow = QMessageBox()
        dialogwindow.setWindowTitle("Сохранение текущего проекта")
        dialogwindow.setText("Вы не сохранили текущий проект. Сохранить?")
        dialogwindow.setIcon(QMessageBox.Warning)

        dialogwindow.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )

        return_value = dialogwindow.exec()

        log.Log.debug_logger(f"save_active_project(): return_value = {return_value}")

        if return_value == QMessageBox.Yes:
            return "Yes"
        elif return_value == QMessageBox.No:
            return "No"
        elif return_value == QMessageBox.Cancel:
            return "Cancel"

    def select_empty_folder():
        """Диалоговое окно 'Пожалуйста, выберите пустую папку'."""

        log.Log.debug_logger("IN select_empty_folder()")

        dialogwindow = QMessageBox()
        dialogwindow.setWindowTitle("Ошибка")
        dialogwindow.setText("Пожалуйста, выберите пустую папку.")
        dialogwindow.setIcon(QMessageBox.Critical)

        dialogwindow.exec()

    @staticmethod
    def select_folder_for_new_project() -> str:
        """Диалоговое окно выбора папки для нового проекта."""

        log.Log.debug_logger("IN select_folder_for_new_project() -> str")

        while True:
            folder_path = QFileDialog.getExistingDirectory(
                None,
                "Выбор папки",
                dirpathsmanager.DirPathManager.get_default_folder_projects_dirpath(),
            )
            if folder_path:
                if not os.listdir(folder_path):
                    log.Log.debug_logger(
                        f"select_folder_for_new_project() -> {folder_path}"
                    )
                    return folder_path
                else:
                    DialogWindows.select_empty_folder()
            else:
                log.Log.debug_logger(f"select_folder_for_new_project() -> {None}")
                return None

    @staticmethod
    def select_folder_for_open_project() -> str:
        """Диалоговое окно выбора папки для открытия проекта."""
        while True:
            folder_path = QFileDialog.getExistingDirectory(
                None,
                "Выбор папки",
                dirpathsmanager.DirPathManager.get_default_folder_projects_dirpath(),
            )
            if folder_path:
                log.Log.debug_logger(
                    f"select_folder_for_open_project() -> {folder_path}"
                )
                return folder_path
            else:
                log.Log.debug_logger(f"select_folder_for_open_project() -> {None}")
                return None


    @staticmethod
    def select_image_for_formimage_in_project() -> str:
        """Диалоговое окно выбора изображения для формы."""

        log.Log.debug_logger("IN select_image_for_formimage_in_project() -> str")
        while True:
            image_path = QFileDialog.getOpenFileName(
                None,
                "Выбор изображения",
                dirpathsmanager.DirPathManager.get_default_folder_projects_dirpath(),
                "Изображения (*.png *.jpg *.jpeg, *.bmp, *.tiff)",
            )
            if image_path[0]:
                log.Log.debug_logger(
                    f"select_image_for_formimage_in_project() -> {image_path[0]}"
                )
                return image_path[0]
            else:
                log.Log.debug_logger(
                    f"select_image_for_formimage_in_project() -> {None}"
                )
                return None