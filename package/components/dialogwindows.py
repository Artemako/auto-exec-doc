import os

from PySide6.QtWidgets import QMessageBox, QFileDialog

import package.app as app
import package.modules.dirpathsmanager as dirpathsmanager


class DialogWindows:
    @staticmethod
    def save_active_project() -> str:
        """Диалоговое окно 'Вы не сохранили текущий проект. Сохранить?'."""
        dialogwindow = QMessageBox()
        dialogwindow.setWindowTitle("Сохранение текущего проекта")
        dialogwindow.setText("Вы не сохранили текущий проект. Сохранить?")
        dialogwindow.setIcon(QMessageBox.Warning)

        dialogwindow.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )

        return_value = dialogwindow.exec()

        if return_value == QMessageBox.Yes:
            return "Yes"
        elif return_value == QMessageBox.No:
            return "No"
        elif return_value == QMessageBox.Cancel:
            return "Cancel"

    def select_empty_folder():
        """Диалоговое окно 'Пожалуйста, выберите пустую папку'."""
        dialogwindow = QMessageBox()
        dialogwindow.setWindowTitle("Ошибка")
        dialogwindow.setText("Пожалуйста, выберите пустую папку.")
        dialogwindow.setIcon(QMessageBox.Critical)

        dialogwindow.exec()

    @staticmethod
    def select_folder_for_new_project() -> str:
        """Диалоговое окно выбора папки для нового проекта."""
        while True:
            folder_path = QFileDialog.getExistingDirectory(
                None,
                "Выбор папки",
                dirpathsmanager.DirPathManager.get_default_folder_projects_dirpath(),
            )
            if folder_path:
                if not os.listdir(folder_path):
                    print(f"Selected Folder: {folder_path}")
                    return folder_path
                else:
                    DialogWindows.select_empty_folder()
            else:
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
                print(f"Selected Folder: {folder_path}")
                return folder_path
            else:
                return None
