import os
import tempfile

from PySide6.QtCore import QStandardPaths


class ObjectsManagerDirPathManager:
    def __init__(self, osbm):
        self.obj_logg = osbm.obj_logg

class DirPathManager:
    def __init__(self):
        self.__main_dirpath = ""
        self.__documents_dirpath = ""
        self.__pictures_dirpath = ""
        self.__temp_dirpath = ""
        self.__default_folder_projects_dirpath = ""
        self.__db_settings_dirpath = ""
        self.__db_original_project_dirpath = ""
        self.__project_dirpath = ""
        self.__db_project_dirpath = ""
        self.__logs_dirpath = ""
        self.__forms_folder_dirpath = ""
        self.__images_folder_dirpath = ""
        self.__global_documents_dirpath = ""
        self.__global_images_dirpath = ""


    def setting_osbm(self, osbm):
        self.__osbm = ObjectsManagerDirPathManager(osbm)
        self.__osbm.obj_logg.debug_logger(f"DirPathManager setting_osbm():\nself.__osbm = {self.__osbm}")


    def setting_paths(self, main_dirpath):
        self.__osbm.obj_logg.debug_logger("DirPathManager setting_paths()")
        # путь к main.py
        self.__main_dirpath = main_dirpath

        # путь к Документы
        self.__documents_dirpath = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DocumentsLocation
        )
        # путь к Изображения
        self.__pictures_dirpath = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.PicturesLocation
        )

        # путь к папке с Temp
        self.__temp_dirpath = tempfile.mkdtemp()

        # путь к папке с проектами по умолчанию
        self.__default_folder_projects_dirpath = os.path.join(
            self.__documents_dirpath, "AutoExecDoc Projects"
        )

        # путь к папке к базе данных
        self.__db_settings_dirpath = os.path.join(
            self.__main_dirpath, "db", "settings.db"
        )
        self.__db_original_project_dirpath = os.path.join(
            self.__main_dirpath, "db", "project.db"
        )

        # путь к директории проекта
        self.__project_dirpath = None
        # путь к project.db проекта
        self.__db_project_dirpath = None

        # путь к папке с логами
        self.__logs_dirpath = os.path.join(
            self.__main_dirpath, "logs"
        )

        # путь к папке с формами (по умолчанию проект не загружен поэтому и пусто)
        self.__forms_folder_dirpath = None
        self.__images_folder_dirpath = None
        self.__pdfs_filder_dirpath = None


    def set_new_dirpaths_for_project(self):
        self.__osbm.obj_logg.debug_logger("DirPathManager set_new_dirpaths_for_project()")
        # папка forms в проекте
        self.__forms_folder_dirpath = os.path.join(
            self.get_project_dirpath(), "forms"
        )

        # папка images в проекте
        self.__images_folder_dirpath = os.path.join(
            self.get_project_dirpath(), "images"
        )

        # папка pdfs в проекте
        self.__pdfs_filder_dirpath = os.path.join(
            self.get_project_dirpath(), "pdfs"
        )

    def get_forms_folder_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_forms_folder_dirpath() -> str: {self.__forms_folder_dirpath}"
        )
        return self.__forms_folder_dirpath

    def get_images_folder_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_image_folder_dirpath() -> str: {self.__images_folder_dirpath}"
        )
        return self.__images_folder_dirpath

    def get_pdfs_folder_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"get_pdfs_folder_dirpath() -> str: {self.__pdfs_filder_dirpath}"
        )
        return self.__pdfs_filder_dirpath

    def set_project_dirpath(self, dirpath: str):
        self.__project_dirpath = dirpath
        self.__osbm.obj_logg.debug_logger(f"DirPathManager set_project_dirpath(dirpath: str):\ndirpath = {dirpath}")

    def set_db_project_dirpath(self, dirpath: str):
        self.__db_project_dirpath = dirpath
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager set_db_project_dirpath(dirpath: str):\ndirpath = {dirpath}"
        )

    def get_main_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_main_dirpath() -> str: {self.__main_dirpath}"
        )
        return self.__main_dirpath

    def get_documents_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_documents_dirpath() -> str: {self.__documents_dirpath}"
        )
        return self.__documents_dirpath

    def get_pictures_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_pictures_dirpath() -> str: {self.__pictures_dirpath}"
        )
        return self.__pictures_dirpath

    def get_folder_in_documents_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_folder_in_documents_dirpath() -> str: {self._folder_in_documents_dirpath}"
        )
        return self._folder_in_documents_dirpath

    def get_db_settings_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_db_settings_dirpath() -> str: {self.__db_settings_dirpath}"
        )
        return self.__db_settings_dirpath

    def get_default_folder_projects_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_default_folder_projects_dirpath() -> str: {self.__default_folder_projects_dirpath}"
        )
        return self.__default_folder_projects_dirpath

    def get_logs_dirpath(self) -> str:
        # ТУТ НЕ НУЖЕН self.__osbm.obj_logg.debug_logger()
        return self.__logs_dirpath

    def get_project_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_project_dirpath() -> str: {self.__project_dirpath}"
        )
        return self.__project_dirpath

    def get_db_project_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_db_project_dirpath() -> str: {self.__db_project_dirpath}"
        )
        return self.__db_project_dirpath

    def get_db_original_project_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager get_db_original_project_dirpath() -> str: {self.__db_original_project_dirpath}"
        )
        return self.__db_original_project_dirpath

    def get_temp_dirpath(self) -> str:
        self.__osbm.obj_logg.debug_logger("DirPathManager get_temp_dirpath() -> str:")
        return self.__temp_dirpath

    def set_new_temp_dirpath(self):
        self.__temp_dirpath = tempfile.mkdtemp()
        self.__osbm.obj_logg.debug_logger(
            f"DirPathManager set_temp_dirpath(dirpath: str):\n__temp_dirpath = {self.__temp_dirpath}"
        )


# obj_dirm = DirPathManager()