import os

from PySide6.QtWidgets import QMessageBox, QFileDialog
from PySide6.QtCore import Qt


class DialogWindows:
    def __init__(self):
        self.__dw = None
        pass

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm

    def get_new_prepare_dw(self) -> object:
        self.__osbm.obj_logg.debug_logger(
            "DialogWindows get_new_prepare_dw() -> object"
        )
        dw = QMessageBox()
        self.__osbm.obj_style.set_style_for(dw)
        return dw

    def save_active_project(self) -> str:
        """Диалоговое окно 'Вы не сохранили текущий проект. Сохранить?'."""

        self.__osbm.obj_logg.debug_logger(
            "DialogWindows save_active_project() -> str"
        )
        self.__dw = self.get_new_prepare_dw()
        self.__dw.setWindowTitle("Сохранение текущего проекта")
        self.__dw.setText("Вы не сохранили текущий проект. Сохранить?")
        self.__dw.setIcon(QMessageBox.Warning)

        self.__dw.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        self.__dw.setButtonText(QMessageBox.Yes, "Да")
        self.__dw.setButtonText(QMessageBox.No, "Нет")

        return_value = self.__dw.exec()

        self.__osbm.obj_logg.debug_logger(
            f"DialogWindows save_active_project() -> return_value = {return_value}"
        )

        if return_value == QMessageBox.Yes:
            return "Yes"
        elif return_value == QMessageBox.No:
            return "No"
        elif return_value == QMessageBox.Cancel:
            return "Cancel"

    def select_empty_folder(self):
        """Диалоговое окно 'Пожалуйста, выберите пустую папку'."""

        self.__osbm.obj_logg.debug_logger("DialogWindows select_empty_folder()")

        self.__dw = self.get_new_prepare_dw()
        self.__dw.setWindowTitle("Ошибка")
        self.__dw.setText("Пожалуйста, выберите пустую папку.")
        self.__dw.setIcon(QMessageBox.Critical)

        self.__dw.exec()

    def select_folder_for_new_project(self) -> str:
        """Диалоговое окно выбора папки для нового проекта."""

        self.__osbm.obj_logg.debug_logger(
            "DialogWindows select_folder_for_new_project() -> str"
        )

        while True:
            folder_path = QFileDialog.getExistingDirectory(
                None,
                "Выбор папки для нового проекта",
                self.__osbm.obj_dirm.get_default_folder_projects_dirpath(),
            )
            if folder_path:
                if not os.listdir(folder_path):
                    self.__osbm.obj_logg.debug_logger(
                        f"DialogWindows select_folder_for_new_project() -> {folder_path}"
                    )
                    return folder_path
                else:
                    self.select_empty_folder()
            else:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_folder_for_new_project() -> {None}"
                )
                return None

    def select_folder_for_saveas_project(self) -> str:
        """Диалоговое окно выбора папки для нового проекта."""

        self.__osbm.obj_logg.debug_logger(
            "DialogWindows select_folder_for_new_project() -> str"
        )

        while True:
            folder_path = QFileDialog.getExistingDirectory(
                None,
                "Выбор папки для сохранения проекта",
                self.__osbm.obj_dirm.get_default_folder_projects_dirpath(),
            )
            if folder_path:
                if not os.listdir(folder_path):
                    self.__osbm.obj_logg.debug_logger(
                        f"select_folder_for_new_project() -> {folder_path}"
                    )
                    return folder_path
                else:
                    self.select_empty_folder()
            else:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_folder_for_new_project() -> {None}"
                )
                return None

    def select_folder_for_open_project(self) -> str:
        """Диалоговое окно выбора папки для открытия проекта."""
        while True:
            folder_path = QFileDialog.getOpenFileName(
                None,
                "Выбор aed файла проекта для его открытия",
                self.__osbm.obj_dirm.get_default_folder_projects_dirpath(),
                "Project files (*.aed)",
            )
            if folder_path[0]:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_folder_for_open_project() -> {folder_path[0]}"
                )
                return os.path.dirname(folder_path[0])
            else:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_folder_for_open_project() -> {None}"
                )
                return None

    def select_image_for_formimage_in_project(self) -> str:
        """Диалоговое окно выбора изображения для формы."""

        self.__osbm.obj_logg.debug_logger(
            "DialogWindows select_image_for_formimage_in_project() -> str"
        )
        while True:
            image_path = QFileDialog.getOpenFileName(
                None,
                "Выбор изображения",
                self.__osbm.obj_dirm.get_pictures_dirpath(),
                "Изображения (*.png *.jpg *.jpeg, *.bmp, *.tiff)",
            )
            if image_path[0]:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_image_for_formimage_in_project() -> {image_path[0]}"
                )
                return image_path[0]
            else:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_image_for_formimage_in_project() -> {None}"
                )
                return None

    def select_docx_file(self) -> str:
        """Диалоговое окно выбора документа."""

        self.__osbm.obj_logg.debug_logger("DialogWindows select_docx_file() -> str")

        while True:
            docx_path = QFileDialog.getOpenFileName(
                None,
                "Выбор документа",
                self.__osbm.obj_dirm.get_documents_dirpath(),
                "Документы (*.docx)",
            )
            if docx_path[0]:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_docx_file() -> {docx_path[0]}"
                )
                return docx_path[0]
            else:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_docx_file() -> {None}"
                )
                return None

    def warning_message(self, message: str):
        """Диалоговое окно 'Предупреждение'."""

        self.__osbm.obj_logg.debug_logger(
            f"DialogWindows warning_message(message: str):\nmessage = {message}"
        )
        self.__dw = self.get_new_prepare_dw()
        self.__dw.setWindowTitle("Предупреждение")
        self.__dw.setText(message)
        self.__dw.setIcon(QMessageBox.Warning)
        response = self.__dw.exec()
        return response

    def error_message(self, message: str):
        """Диалоговое окно 'Ошибка'."""

        self.__osbm.obj_logg.debug_logger(
            f"DialogWindows error_message(message: str):\nmessage = {message}"
        )
        self.__dw = self.get_new_prepare_dw()
        self.__dw.setWindowTitle("Ошибка")
        self.__dw.setText(message)
        self.__dw.setIcon(QMessageBox.Critical)
        response = self.__dw.exec()
        return response

    def question_message(self, message: str):
        """Диалоговое окно 'Вопрос'."""

        self.__osbm.obj_logg.debug_logger(
            f"DialogWindows question_message(message: str):\nmessage = {message}"
        )
        self.__dw = self.get_new_prepare_dw()
        self.__dw.setWindowTitle("Вопрос")
        self.__dw.setText(message)
        self.__dw.setIcon(QMessageBox.Question)
        self.__dw.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.__dw.setButtonText(QMessageBox.Yes, "Да")
        self.__dw.setButtonText(QMessageBox.No, "Нет")
        response = self.__dw.exec()
        if response == QMessageBox.Yes:
            return True
        elif response == QMessageBox.No:
            return False
        else:
            return None

    def select_name_and_dirpath_export_pdf(self) -> str:
        """Диалоговое окно 'Выберите имя и путь для экспорта в PDF'."""

        self.__osbm.obj_logg.debug_logger(
            "DialogWindows select_name_and_dirpath_export_pdf() -> str"
        )

        while True:
            multipage_pdf_path = QFileDialog.getSaveFileName(
                None,
                "Выберите имя и путь для экспорта в PDF",
                self.__osbm.obj_dirm.get_documents_dirpath(),
                "PDF (*.pdf)",
            )
            if multipage_pdf_path[0]:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_name_and_dirpath_export_pdf() -> {multipage_pdf_path[0]}"
                )
                return multipage_pdf_path[0]
            else:
                self.__osbm.obj_logg.debug_logger(
                    f"DialogWindows select_name_and_dirpath_export_pdf() -> {None}"
                )
                return None


# obj_dw = DialogWindows()
