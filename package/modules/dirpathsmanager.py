import sys
import os
import tempfile 

from PySide6.QtCore import QStandardPaths

import package.modules.log as log


class DirPathManager:

    def config_paths(main_dirpath):
    # путь к main.py
        DirPathManager.__main_dirpath = main_dirpath

        # путь к Документы
        DirPathManager.__documents_dirpath = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DocumentsLocation
        )

        # путь к папке с Temp
        DirPathManager.__temp_dirpath = tempfile.mkdtemp()

        # путь к папке с проектами по умолчанию
        DirPathManager.__default_folder_projects_dirpath = os.path.join(
            DirPathManager.__documents_dirpath, "AutoExecDoc Projects"
        )

        # путь к папке к базе данных
        DirPathManager.__db_settings_dirpath = os.path.join(DirPathManager.__main_dirpath, "db", "settings.db")
        DirPathManager.__db_original_project_dirpath = os.path.join(DirPathManager.__main_dirpath, "db", "project.db")

        # путь к директории проекта
        DirPathManager.__project_dirpath = None
        # путь к project.db проекта
        DirPathManager.__db_project_dirpath = None

        # путь к папке с логами
        DirPathManager.__logs_dirpath = os.path.join(DirPathManager.__main_dirpath, "logs")

        # путь к папке с формами
        DirPathManager.__templates_dirpath = os.path.join(DirPathManager.__main_dirpath, "templates")
        DirPathManager.__templates_main_dirpath = os.path.join(DirPathManager.__templates_dirpath, "main" )


        DirPathManager.__forms_folder_dirpath = None
        DirPathManager.__images_folder_dirpath = None
        # DirPathManager.__pdfs_filder_dirpath = None

    def __init__(self):
        pass
    
    
    @staticmethod
    def set_new_dirpaths_for_project():
        log.Log.debug_logger("set_new_dirpaths_for_project()")
        # папка forms в проекте
        DirPathManager.__forms_folder_dirpath = os.path.join(
            DirPathManager.get_project_dirpath(), "forms"
        )

        # папка images в проекте
        DirPathManager.__images_folder_dirpath = os.path.join(
            DirPathManager.get_project_dirpath(), "images"
        )

        # папка pdfs в проекте
        # DirPathManager.__pdfs_filder_dirpath = os.path.join(
        #     DirPathManager.get_project_dirpath(), "pdfs"
        # )

    @staticmethod
    def get_forms_folder_dirpath() -> str:
        log.Log.debug_logger(
            f"get_forms_folder_dirpath() -> str: {DirPathManager.__forms_folder_dirpath}"
        )
        return DirPathManager.__forms_folder_dirpath
    
    @staticmethod
    def get_images_folder_dirpath() -> str:
        log.Log.debug_logger(
            f"get_image_folder_dirpath() -> str: {DirPathManager.__images_folder_dirpath}"
        )
        return DirPathManager.__images_folder_dirpath
    
    # @staticmethod
    # def get_pdfs_folder_dirpath() -> str:
    #     log.Log.debug_logger(
    #         f"get_pdfs_folder_dirpath() -> str: {DirPathManager.__pdfs_filder_dirpath}"
    #     )
    #     return DirPathManager.__pdfs_filder_dirpath
    
    @staticmethod
    def get_templates_main_dirpath() -> str:
        log.Log.debug_logger(
            f"get_templates_main_dirpath() -> str: {DirPathManager.__templates_main_dirpath}"
        )
        return DirPathManager.__templates_main_dirpath


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
            f"get_default_folder_projects_dirpath() -> str: {DirPathManager.__default_folder_projects_dirpath}"
        )
        return DirPathManager.__default_folder_projects_dirpath

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

    @staticmethod
    def get_temp_dirpath() -> str:
        log.Log.debug_logger(
            "get_temp_dirpath() -> str:"
        )
        return DirPathManager.__temp_dirpath
    
    @staticmethod
    def set_new_temp_dirpath():
        DirPathManager.__temp_dirpath = tempfile.mkdtemp()
        log.Log.debug_logger(f"set_temp_dirpath(dirpath: str): __temp_dirpath = {DirPathManager.__temp_dirpath}")

