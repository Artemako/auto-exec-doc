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

        #Папка temp
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

    # @staticmethod
    # def move_image_to_temp(image_dirpath) -> str:
    #     """
    #     Перемещение изображения в папку temp.
    #     """
    #     log.Log.debug_logger(
    #         f"IN move_image_to_temp(image_dirpath): image_dirpath = {image_dirpath}"
    #     )  
    #     new_dirpath = shutil.copy(image_dirpath, dirpathsmanager.DirPathManager.get_temp_dirpath())
    #     return new_dirpath


    @staticmethod
    def clear_temp_folder():
        """
        Очистка папки temp.
        """
        log.Log.debug_logger("IN clear_temp_folder()")

        temp_dirpath = dirpathsmanager.DirPathManager.get_temp_dirpath()
        files = os.listdir(temp_dirpath)
        # Удалить каждый файл и папку в папке
        for file in files:
            file_path = os.path.join(temp_dirpath, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)


