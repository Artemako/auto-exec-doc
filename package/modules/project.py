import os
import datetime

import package.components.dialogwindows as dialogwindows
import package.modules.database as database


class Project:
    # по умолчанию None
    _current_directory = None
    _current_name = None

    # по умолчанию False
    _status_active = False
    _status_save = False

    def __init__(self):
        pass

    # region методы set
    @staticmethod
    def set_current_directory(directory):
        Project._current_directory = directory

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
    def get_current_directory() -> str:
        return Project._current_directory

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
    def new_project():
        """
        Действие создание проекта.
        """
        # продолжить, если проверка успешна и не отменена
        if Project.check_project_before_new_or_open():
            # выбор директории будущего проекта
            folder_path = Project.check_folder_path_for_new_project()
            if folder_path:
                # добавление в БД
                database.Database.add_new_project_to_db(
                    os.path.basename(folder_path), folder_path
                )
                # TODO Добавить в директорию файлы для проекта
                Project.set_true_actives_project(folder_path)

    @staticmethod
    def save_project():
        """
        Сохранение проекта.
        """
        Project.set_status_save(True)

    @staticmethod
    def check_folder_path_for_new_project() -> str:
        """
        Выбор папки для нового проекта.
        """
        while True:
            folder_path = dialogwindows.DialogWindows.select_folder_for_new_project()
            if folder_path:
                if not os.listdir(folder_path):
                    return folder_path
                else:
                    dialogwindows.DialogWindows.select_empty_folder()
            else:
                return None

    @staticmethod
    def open_project():
        """Открытие проекта."""
        # продолжить, если проверка успешна и не отменена
        if Project.check_project_before_new_or_open():
            # выбор директории будущего проекта
            folder_path = Project.check_folder_path_for_new_project()
            if folder_path:
                database.Database.add_or_update_open_project_to_db(
                    os.path.basename(folder_path), folder_path
                )
                Project.set_true_actives_project(folder_path)

    @staticmethod
    def open_recent_project():
        """Открытие недавнего проекта."""
        # TODO Проверить папку на проектность
        pass

    @staticmethod
    def set_true_actives_project(folder_path):
        """
        Задает активность проекта.
        """
        Project.set_current_directory(folder_path)
        Project.set_current_name(os.path.basename(folder_path))
        Project.set_status_active(True)
        Project.set_status_save(True)

    @staticmethod
    def save_project():
        # TODO Сделать сохранение проекта
        Project.set_status_save(True)
        return
