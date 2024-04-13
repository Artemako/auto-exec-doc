import os

import package.components.dialogwindows as dialogwindows
import package.modules.settingsdatabase as settingsdatabase
import package.modules.projectdatabase as projectdatabase

import package.modules.filefoldermanager as filefoldermanager
import package.modules.dirpathsmanager as dirpathsmanager


class Project:
    # по умолчанию None
    _current_name = None

    # по умолчанию False
    _status_active = False
    _status_save = False

    def __init__(self):
        pass

    # region методы set

    @staticmethod
    def set_current_name(name):
        Project._current_name = name

    @staticmethod
    def set_status_active(status: bool):
        Project._status_active = status

    @staticmethod
    def set_status_save(status: bool):
        Project._status_save = status

    # endregion
    # region методы get

    @staticmethod
    def get_current_name() -> str:
        return Project._current_name

    # endregion
    # region методы is, check
    @staticmethod
    def is_active_status() -> bool:
        return Project._status_active

    @staticmethod
    def is_status_save() -> bool:
        return Project._status_save

    @staticmethod
    def check_project_before_new_or_open() -> bool:
        """
        Проверка текущего проекта до создания или открытия нового.
        """
        # появление диалогового окна, когда проект активен, но не сохранен
        if Project.is_active_status() and not Project.is_status_save():
            answer = dialogwindows.DialogWindows.save_active_project()
            if answer == "Yes":
                Project.save_project()
                return True
            elif answer == "Cancel":
                # отменяет создание проекта
                return False
        return True

    # endregion

    @staticmethod
    def set_project_dirpaths(folder_path: str):
        """
        Установка путей к папке проекта.
        Установка пути к project.db проекта.
        """
        # Установка пути к папке проекта
        dirpathsmanager.DirPathManager.set_project_dirpath(folder_path)
        # Установка пути к project.db проекта
        dirpathsmanager.DirPathManager.set_db_project_dirpath(
            os.path.join(
                dirpathsmanager.DirPathManager.get_project_dirpath(), "project.db"
            )
        )

    @staticmethod
    def new_project():
        """
        Действие создание проекта.
        """
        # продолжить, если проверка успешна и не отменена
        if Project.check_project_before_new_or_open():
            # выбор директории будущего проекта
            folder_path = dialogwindows.DialogWindows.select_folder_for_new_project()
            if folder_path:
                Project.set_project_dirpaths(folder_path)
                Project.config_new_project()

    @staticmethod
    def config_new_project():
        """
        Конфигурация нового проекта.
        """
        Project.set_current_name(
            os.path.basename(dirpathsmanager.DirPathManager.get_project_dirpath())
        )
        settingsdatabase.Database.add_new_project_to_db()

        filefoldermanager.FileFolderManager.add_files_and_folders_to_new_project()

        Project.set_true_actives_project()

    @staticmethod
    def save_project():
        """
        Сохранение проекта.
        """
        Project.set_status_save(True)

    @staticmethod
    def open_project():
        """Открытие проекта."""
        # продолжить, если проверка успешна и не отменена
        if Project.check_project_before_new_or_open():
            # выбор директории будущего проекта
            folder_path = dialogwindows.DialogWindows.select_folder_for_open_project()
            if folder_path:
                Project.set_project_dirpaths(folder_path)
                Project.config_open_project()

    @staticmethod
    def config_open_project():
        """
        Конфигурация открытого проекта.
        """
        settingsdatabase.Database.add_or_update_open_project_to_db()

        Project.set_true_actives_project()

    @staticmethod
    def open_recent_project():
        """Открытие недавнего проекта."""
        # TODO Проверить папку на проектность
        pass

    @staticmethod
    def set_true_actives_project():
        """
        Задает активность проекта.
        """
        Project.set_status_active(True)
        Project.set_status_save(True)

    @staticmethod
    def save_project():
        # TODO Сделать сохранение проекта
        Project.set_status_save(True)
        return
