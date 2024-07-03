import os
import tempfile

from PySide6.QtCore import QStandardPaths



class DirPathManager:
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__main_dirpath = ""
        self.__documents_dirpath = ""
        self.__temp_dirpath = ""
        self.__default_folder_projects_dirpath = ""
        self.__db_settings_dirpath = ""
        self.__db_original_project_dirpath = ""
        self.__project_dirpath = ""
        self.__db_project_dirpath = ""
        self.__logs_dirpath = ""
        self.__templates_dirpath = ""
        self.__templates_main_dirpath = ""
        self.__forms_folder_dirpath = ""
        self.__images_folder_dirpath = ""


    def config_paths(self, main_dirpath):
        # путь к main.py
        self.__main_dirpath = main_dirpath

        # путь к Документы
        self.__documents_dirpath = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DocumentsLocation
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

        # путь к папке с формами
        self.__templates_dirpath = os.path.join(
            self.__main_dirpath, "templates"
        )
        self.__templates_main_dirpath = os.path.join(
            self.__templates_dirpath, "main"
        )

        self.__forms_folder_dirpath = None
        self.__images_folder_dirpath = None
        # self.__pdfs_filder_dirpath = None

    def set_new_dirpaths_for_project(self):
        self.__obs_manager.obj_l.debug_logger("set_new_dirpaths_for_project()")
        # папка forms в проекте
        self.__forms_folder_dirpath = os.path.join(
            self.get_project_dirpath(), "forms"
        )

        # папка images в проекте
        self.__images_folder_dirpath = os.path.join(
            self.get_project_dirpath(), "images"
        )

        # папка pdfs в проекте
        # self.__pdfs_filder_dirpath = os.path.join(
        #     self.get_project_dirpath(), "pdfs"
        # )

    def get_forms_folder_dirpath(self) -> str:
        self.__obs_manager.obj_l.debug_logger(
            f"get_forms_folder_dirpath() -> str: {self.__forms_folder_dirpath}"
        )
        return self.__forms_folder_dirpath

    def get_images_folder_dirpath(self) -> str:
        self.__obs_manager.obj_l.debug_logger(
            f"get_image_folder_dirpath() -> str: {self.__images_folder_dirpath}"
        )
        return self.__images_folder_dirpath

    #
    # def get_pdfs_folder_dirpath(self) -> str:
    #     self.__obs_manager.obj_l.debug_logger(
    #         f"get_pdfs_folder_dirpath() -> str: {self.__pdfs_filder_dirpath}"
    #     )
    #     return self.__pdfs_filder_dirpath

    def get_templates_main_dirpath(self) -> str:
        self.__obs_manager.obj_l.debug_logger(
            f"get_templates_main_dirpath() -> str: {self.__templates_main_dirpath}"
        )
        return self.__templates_main_dirpath

    def set_project_dirpath(self, dirpath: str):
        self.__project_dirpath = dirpath
        self.__obs_manager.obj_l.debug_logger(f"set_project_dirpath(dirpath: str): dirpath = {dirpath}")

    def set_db_project_dirpath(self, dirpath: str):
        self.__db_project_dirpath = dirpath
        self.__obs_manager.obj_l.debug_logger(
            f"set_db_project_dirpath(dirpath: str): dirpath = {dirpath}"
        )

    def get_main_dirpath(self) -> str:
        self.__obs_manager.obj_l.debug_logger(
            f"get_main_dirpath() -> str: {self.__main_dirpath}"
        )
        return self.__main_dirpath

    def get_documents_dirpath(self) -> str:
        self.__obs_manager.obj_l.debug_logger(
            f"get_documents_dirpath() -> str: {self.__documents_dirpath}"
        )
        return self.__documents_dirpath

    def get_folder_in_documents_dirpath(self) -> str:
        self.__obs_manager.obj_l.debug_logger(
            f"get_folder_in_documents_dirpath() -> str: {self._folder_in_documents_dirpath}"
        )
        return self._folder_in_documents_dirpath

    def get_db_settings_dirpath(self) -> str:
        self.__obs_manager.obj_l.debug_logger(
            f"get_db_settings_dirpath() -> str: {self.__db_settings_dirpath}"
        )
        return self.__db_settings_dirpath

    def get_default_folder_projects_dirpath(self) -> str:
        self.__obs_manager.obj_l.debug_logger(
            f"get_default_folder_projects_dirpath() -> str: {self.__default_folder_projects_dirpath}"
        )
        return self.__default_folder_projects_dirpath

    def get_logs_dirpath(self) -> str:
        # ТУТ НЕ НУЖЕН self.__obs_manager.obj_l.debug_logger()
        return self.__logs_dirpath

    def get_project_dirpath(self) -> str:
        self.__obs_manager.obj_l.debug_logger(
            f"get_project_dirpath() -> str: {self.__project_dirpath}"
        )
        return self.__project_dirpath

    def get_db_project_dirpath(self) -> str:
        self.__obs_manager.obj_l.debug_logger(
            f"get_db_project_dirpath() -> str: {self.__db_project_dirpath}"
        )
        return self.__db_project_dirpath

    def get_db_original_project_dirpath(self) -> str:
        self.__obs_manager.obj_l.debug_logger(
            f"get_db_original_project_dirpath() -> str: {self.__db_original_project_dirpath}"
        )
        return self.__db_original_project_dirpath

    def get_templates_dirpath(self) -> str:
        self.__obs_manager.obj_l.debug_logger(
            f"get_templates_dirpath() -> str: {self.__templates_dirpath}"
        )
        return self.__templates_dirpath

    def get_temp_dirpath(self) -> str:
        self.__obs_manager.obj_l.debug_logger("get_temp_dirpath() -> str:")
        return self.__temp_dirpath

    def set_new_temp_dirpath(self):
        self.__temp_dirpath = tempfile.mkdtemp()
        self.__obs_manager.obj_l.debug_logger(
            f"set_temp_dirpath(dirpath: str): __temp_dirpath = {self.__temp_dirpath}"
        )


# obj_dpm = DirPathManager()