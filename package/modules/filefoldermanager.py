import os
import package.modules.dirpathsmanager as dirpathsmanager


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
