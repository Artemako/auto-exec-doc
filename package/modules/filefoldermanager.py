import os
import shutil

import package.modules.dirpathsmanager as dirpathsmanager
import package.modules.projectdatabase as projectdatabase
import package.modules.log as log


class FileFolderManager:
    def __init__(self):
        pass

    @staticmethod
    def create_and_config_files_and_folders():
        """
        Создание и конфигурация папок и файлов.
        """
        log.Log.debug_logger("IN create_and_config_files_and_folders()")
        if not os.path.exists(
            dirpathsmanager.DirPathManager.get_default_folder_projects_dirpath()
        ):
            os.mkdir(
                dirpathsmanager.DirPathManager.get_default_folder_projects_dirpath()
            )

    @staticmethod
    def add_forms_folders_to_new_project():
        """
        Добавление в проект папок форм.
        """
        log.Log.debug_logger("IN add_forms_folders_to_new_project()")
        # папка forms
        forms_folder_dirpath = os.path.join(
            dirpathsmanager.DirPathManager.get_project_dirpath(), "forms"
        )

        if not os.path.exists(forms_folder_dirpath):
            os.mkdir(forms_folder_dirpath)

        # Папка temp
        if not os.path.exists(dirpathsmanager.DirPathManager.get_temp_dirpath()):
            os.mkdir(dirpathsmanager.DirPathManager.get_temp_dirpath())

        # путь к папке с шаблонами
        templates_main_dirpath = os.path.join(
            dirpathsmanager.DirPathManager.get_templates_dirpath(), "main"
        )

        # копирование шаблонов в папку проекта forms
        for f in os.listdir(templates_main_dirpath):
            shutil.copy(
                os.path.join(templates_main_dirpath, f),
                os.path.join(forms_folder_dirpath, f),
            )

    @staticmethod
    def clear_temp_folder(is_del_folder=False):
        """
        Очистка папки temp.
        """
        log.Log.debug_logger(
            f"IN clear_temp_folder(is_del_folder): is_del_folder = {is_del_folder}, temp_dirpath = {dirpathsmanager.DirPathManager.get_temp_dirpath()}"
        )
        temp_dirpath = dirpathsmanager.DirPathManager.get_temp_dirpath()
        try:
            shutil.rmtree(temp_dirpath)
            if not is_del_folder:
                os.mkdir(temp_dirpath)
        except Exception as e:
            log.Log.error_logger(e)
            dirpathsmanager.DirPathManager.set_new_temp_dirpath()
