import sys
import os

from PySide6.QtCore import QStandardPaths

import package.modules.log as log


class DirPathManager:
    # путь к main.py
    __main_dirpath = os.path.dirname(sys.modules["__main__"].__file__)

    # путь к Документы
    __documents_dirpath = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.DocumentsLocation
    )

    # путь к папке с проектами по умолчанию
    _default_folder_projects_dirpath = os.path.join(
        __documents_dirpath, "AutoExecDoc Projects"
    )

    # путь к папке к базе данных
    __db_settings_dirpath = os.path.join(__main_dirpath, "db", "settings.db")
    __db_original_project_dirpath = os.path.join(__main_dirpath, "db", "project.db")

    # путь к директории проекта
    __project_dirpath = None
    # путь к project.db проекта
    __db_project_dirpath = None

    # путь к папке с логами
    __logs_dirpath = os.path.join(__main_dirpath, "logs")

    # путь к папке с формами
    __templates_dirpath = os.path.join(__main_dirpath, "templates")

    def __init__(self):
        pass

    # region Методы set
    @staticmethod
    def set_project_dirpath(dirpath: str):
        DirPathManager.__project_dirpath = dirpath
        log.Log.debug_logger(f"set_project_dirpath(dirpath: str): dirpath = {dirpath}")

    @staticmethod
    def set_db_project_dirpath(dirpath: str):
        DirPathManager.__db_project_dirpath = dirpath
        log.Log.debug_logger(
            f"set_db_project_dirpath(dirpath: str): dirpath = {dirpath}"
        )

    # endregion

    # region методы get
    @staticmethod
    def get_main_dirpath() -> str:
        log.Log.debug_logger(
            f"get_main_dirpath() -> str: {DirPathManager.__main_dirpath}"
        )
        return DirPathManager.__main_dirpath

    @staticmethod
    def get_documents_dirpath() -> str:
        log.Log.debug_logger(
            f"get_documents_dirpath() -> str: {DirPathManager.__documents_dirpath}"
        )
        return DirPathManager.__documents_dirpath

    @staticmethod
    def get_folder_in_documents_dirpath() -> str:
        log.Log.debug_logger(
            f"get_folder_in_documents_dirpath() -> str: {DirPathManager._folder_in_documents_dirpath}"
        )
        return DirPathManager._folder_in_documents_dirpath

    @staticmethod
    def get_db_settings_dirpath() -> str:
        log.Log.debug_logger(
            f"get_db_settings_dirpath() -> str: {DirPathManager.__db_settings_dirpath}"
        )
        return DirPathManager.__db_settings_dirpath

    @staticmethod
    def get_default_folder_projects_dirpath() -> str:
        log.Log.debug_logger(
            f"get_default_folder_projects_dirpath() -> str: {DirPathManager._default_folder_projects_dirpath}"
        )
        return DirPathManager._default_folder_projects_dirpath

    @staticmethod
    def get_logs_dirpath() -> str:
        # ТУТ НЕ НУЖЕН log.Log.debug_logger()
        return DirPathManager.__logs_dirpath

    @staticmethod
    def get_project_dirpath() -> str:
        log.Log.debug_logger(
            f"get_project_dirpath() -> str: {DirPathManager.__project_dirpath}"
        )
        return DirPathManager.__project_dirpath

    @staticmethod
    def get_db_project_dirpath() -> str:
        log.Log.debug_logger(
            f"get_db_project_dirpath() -> str: {DirPathManager.__db_project_dirpath}"
        )
        return DirPathManager.__db_project_dirpath

    @staticmethod
    def get_db_original_project_dirpath() -> str:
        log.Log.debug_logger(
            f"get_db_original_project_dirpath() -> str: {DirPathManager.__db_original_project_dirpath}"
        )
        return DirPathManager.__db_original_project_dirpath

    @staticmethod
    def get_templates_dirpath() -> str:
        log.Log.debug_logger(
            f"get_templates_dirpath() -> str: {DirPathManager.__templates_dirpath}"
        )
        return DirPathManager.__templates_dirpath

    # endregion
