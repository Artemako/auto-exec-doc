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
        temp_folder_dirpath = os.path.join(
            dirpathsmanager.DirPathManager.get_project_dirpath(), "temp"
        )

        if not os.path.exists(temp_folder_dirpath):
            os.mkdir(temp_folder_dirpath)

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

        # # все формы и json_content из templates_dirpath
        # for f in os.listdir(templates_dirpath):
        #     if f.endswith(".json"):
        #         json_content.append(f)
        #     else:
        #         forms.append(f)


        # # копирование форм в папку проекта forms
        # for form in forms:
        #     shutil.copytree(
        #         os.path.join(templates_dirpath, form, "main"),
        #         os.path.join(forms_folder_dirpath, form),
        #     )


    @staticmethod
    def move_image_to_temp(image_dirpath, file_name_with_extension):
        """
        Перемещение изображения в папку temp.
        """
        log.Log.debug_logger(
            f"IN move_image_to_temp(image_dirpath, file_name_with_extension): image_dirpath = {image_dirpath}, file_name_with_extension = {file_name_with_extension}"
        )
        
        shutil.copy2(
            image_dirpath,
            os.path.join(
                dirpathsmanager.DirPathManager.get_project_dirpath(), "temp", file_name_with_extension
            ),
        )

    @staticmethod
    def clear_temp_folder():
        """
        Очистка папки temp.
        """
        log.Log.debug_logger("IN clear_temp_folder()")
        temp_folder_dirpath = os.path.join(
            dirpathsmanager.DirPathManager.get_project_dirpath(), "temp"
        )
        if os.path.exists(temp_folder_dirpath):
            shutil.rmtree(temp_folder_dirpath)
        os.makedirs(temp_folder_dirpath)

