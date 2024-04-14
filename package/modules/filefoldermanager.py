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

        # все формы и json_content из templates_dirpath
        forms = []
        json_content = []
        for f in os.listdir(templates_dirpath):
            if f.endswith(".json"):
                json_content.append(f)
            else:
                forms.append(f)

        print(f"forms, {forms}")
        print(f"json_content, {json_content}")

        # копирование форм в папку проекта forms
        for form in forms:
            shutil.copytree(
                os.path.join(templates_dirpath, form, "main"),
                os.path.join(forms_folder_dirpath, form),
            )

        # копирование json_content в папку проекта forms
        for json_file in json_content:
            shutil.copy(
                os.path.join(templates_dirpath, json_file),
                os.path.join(forms_folder_dirpath, json_file),
            )
