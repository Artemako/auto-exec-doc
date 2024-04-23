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
    def create_folders_for_new_project():
        """
        Добавление в проект папок форм.
        """
        log.Log.debug_logger("IN add_forms_folders_to_new_project()")
        
        # папка forms в проекте
        forms_folder_dirpath = dirpathsmanager.DirPathManager.get_forms_folder_dirpath()

        if not os.path.exists(forms_folder_dirpath):
            os.makedirs(forms_folder_dirpath)

        # папка images в проекте
        image_folder_dirpath = dirpathsmanager.DirPathManager.get_images_folder_dirpath()

        if not os.path.exists(image_folder_dirpath):
            os.makedirs(image_folder_dirpath)        

        # папка с pdfs
        pdfs_folder_dirpath = dirpathsmanager.DirPathManager.get_pdfs_folder_dirpath()

        if not os.path.exists(pdfs_folder_dirpath):
            os.makedirs(pdfs_folder_dirpath)    


        # Папка TEMP/AUTOEXECDOC
        if not os.path.exists(dirpathsmanager.DirPathManager.get_temp_dirpath()):
            os.makedirs(dirpathsmanager.DirPathManager.get_temp_dirpath())

        templates_main_dirpath = dirpathsmanager.DirPathManager.get_templates_main_dirpath()




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

    @staticmethod
    def move_image_from_temp_to_project(name_image):
        log.Log.debug_logger("IN move_image_from_temp_to_project()")
        # путь к папке с шаблонами
        temp_dirpath = dirpathsmanager.DirPathManager.get_temp_dirpath()
        image_folder_dirpath = os.path.join(dirpathsmanager.DirPathManager.get_project_dirpath(), "images")
        try:
            shutil.move(os.path.join(temp_dirpath, name_image), os.path.join(image_folder_dirpath, name_image))
        except Exception as e:
            log.Log.error_logger(e)

    @staticmethod
    def delete_image_from_project(image_dirpath):
        log.Log.debug_logger("IN delete_image_from_project()")
        # путь к папке с шаблонами
        image_folder_dirpath = os.path.join(dirpathsmanager.DirPathManager.get_project_dirpath(), "images")
        try:
            os.remove(os.path.join(image_folder_dirpath, image_dirpath))
        except Exception as e:
            log.Log.error_logger(e)