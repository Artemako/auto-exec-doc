import sys
import os

from PySide6.QtCore import QStandardPaths


class DirPathManager:
    # путь к main.py
    _main_dirpath = os.path.dirname(sys.modules["__main__"].__file__)

    # путь к Документы
    _documents_dirpath = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.DocumentsLocation
    )

    # путь к папке к базе данных
    _db_settings_dirpath = os.path.join(_main_dirpath, "db", "settings.db")

    # путь к папке с проектами по умолчанию
    _default_folder_projects_dirpath = os.path.join(_documents_dirpath, "AutoExecDoc")

    # путь к папке с логами
    _logs_dirpath = os.path.join(_main_dirpath, "logs")

    def __init__(self):
        pass

    # region методы get
    @staticmethod
    def get_main_dirpath() -> str:
        return DirPathManager._main_dirpath

    @staticmethod
    def get_documents_dirpath() -> str:
        return DirPathManager._documents_dirpath

    @staticmethod
    def get_folder_in_documents_dirpath() -> str:
        return DirPathManager._folder_in_documents_dirpath

    @staticmethod
    def get_db_settings_dirpath() -> str:
        return DirPathManager._db_settings_dirpath

    @staticmethod
    def get_default_folder_projects_dirpath() -> str:
        return DirPathManager._default_folder_projects_dirpath

    @staticmethod
    def get_logs_dirpath() -> str:
        return DirPathManager._logs_dirpath

    # endregion
