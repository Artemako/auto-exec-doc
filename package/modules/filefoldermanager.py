import os
import shutil

import package.modules.dirpathsmanager as dirpathsmanager
import package.modules.projectdatabase as projectdatabase


class FileFolderManager:
    def __init__(self):
        pass

    @staticmethod
    def create_and_config_files_and_folders():
        """
        Создание и конфигурация папок и файлов.
        """
        FileFolderManager.create_folder_in_documents_dirpath()

    @staticmethod
    def create_folder_in_documents_dirpath():
        """
        Создание папки хранения проектов в документах.
        """
        if not os.path.exists(
            dirpathsmanager.DirPathManager.get_default_folder_projects_dirpath()
        ):
            os.mkdir(
                dirpathsmanager.DirPathManager.get_default_folder_projects_dirpath()
            )

    @staticmethod
    def add_files_and_folders_to_new_project():
        """
        Добавление в проект папок и файлов.
        """
        # TODO Файлы и папки
        projectdatabase.Database.create_and_config_db()
        FileFolderManager.add_forms_folders_to_new_project()

    @staticmethod
    def add_forms_folders_to_new_project():
        """
        Добавление в проект папок форм.
        """
        forms_folder_dirpath = os.path.join(
            dirpathsmanager.DirPathManager.get_project_dirpath(), "forms"
        )
        templates_dirpath = dirpathsmanager.DirPathManager.get_templates_dirpath()

        # все формы из templates_dirpath
        forms = os.listdir(templates_dirpath)

        # копирование форм в папку проекта forms
        for folder in forms:
            shutil.copytree(
                os.path.join(templates_dirpath, folder, "main"),
                os.path.join(forms_folder_dirpath, folder),
            )
