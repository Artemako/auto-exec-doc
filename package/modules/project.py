import os

import package.components.dialogwindows as dialogwindows


import package.modules.settingsdatabase as settingsdatabase
import package.modules.projectdatabase as projectdatabase
import package.modules.log as log
import package.modules.filefoldermanager as filefoldermanager
import package.modules.dirpathsmanager as dirpathsmanager

import package.controllers.scrollareainput as scrollareainput

import package.controllers.structureexecdoc as structureexecdoc
import package.controllers.pagestemplate as pagestemplate
import package.controllers.statusbar as statusbar


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
        """
        Установка имени проекта.
        """
        log.Log.debug_logger(f"set_current_name(name: str): name = {name}")
        Project._current_name = name

    @staticmethod
    def set_status_active(status: bool):
        """
        Установка статуса активности проекта.
        """
        log.Log.debug_logger(f"set_status_active(status: bool): status = {status}")
        Project._status_active = status

    @staticmethod
    def set_status_save(status: bool):
        """
        Установка статуса сохранения проекта.
        """
        log.Log.debug_logger(f"set_status_save(status: bool): status = {status}")
        Project._status_save = status

    # endregion
    # region методы get

    @staticmethod
    def get_current_name() -> str:
        log.Log.debug_logger(f"get_current_name() -> str: {Project._current_name}")
        return Project._current_name

    # endregion
    # region методы is, check
    @staticmethod
    def is_active_status() -> bool:
        log.Log.debug_logger(f"is_active_status() -> bool: {Project._status_active}")
        return Project._status_active

    @staticmethod
    def is_status_save() -> bool:
        log.Log.debug_logger(f"is_status_save() -> bool: {Project._status_save}")
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
        log.Log.debug_logger(
            f"IN set_project_dirpaths(folder_path: str): folder_path = {folder_path}"
        )
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
        log.Log.debug_logger("IN new_project()")
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
        log.Log.debug_logger("IN config_new_project()")

        Project.set_current_name(
            os.path.basename(dirpathsmanager.DirPathManager.get_project_dirpath())
        )
        settingsdatabase.Database.add_new_project_to_db()
        projectdatabase.Database.create_and_config_db_project()
        # настраиваем контроллеры
        # настраиваем структуру execdoc
        structureexecdoc.StructureExecDoc.update_structure_exec_doc()
        pagestemplate.PagesTemplate.create_pages_template()

        filefoldermanager.FileFolderManager.add_forms_folders_to_new_project()
        Project.set_true_actives_project()
        # сообщение для статусбара
        statusbar.StatusBar.set_message_for_statusbar(
            f"Проект c именем {Project.get_current_name()} создан и открыт."
        )

    @staticmethod
    def save_project():
        """
        Сохранение проекта.
        """
        log.Log.debug_logger("IN save_project()")
        # TODO Сделать сохранение проекта
        if Project.is_active_status():
            scrollareainput.ScroolAreaInput.save_data()
            Project.set_status_save(True)

    @staticmethod
    def open_project():
        """Открытие проекта."""
        log.Log.debug_logger("IN open_project()")
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
        log.Log.debug_logger("IN config_open_project()")

        Project.set_current_name(
            os.path.basename(dirpathsmanager.DirPathManager.get_project_dirpath())
        )
        # настраиваем базы данных
        settingsdatabase.Database.add_or_update_open_project_to_db()
        projectdatabase.Database.create_and_config_db_project()
        # настраиваем структуру execdoc
        structureexecdoc.StructureExecDoc.update_structure_exec_doc()
        Project.set_true_actives_project()
        # сообщение для статусбара
        statusbar.StatusBar.set_message_for_statusbar(
            f"Проект c именем {Project.get_current_name()} открыт."
        )

    @staticmethod
    def open_recent_project():
        """Открытие недавнего проекта."""
        log.Log.debug_logger("IN open_recent_project()")
        # TODO Проверить папку на проектность
        pass

    @staticmethod
    def set_true_actives_project():
        """
        Задает активность проекта.
        """
        log.Log.debug_logger("IN set_true_actives_project()")
        Project.set_status_active(True)
        Project.set_status_save(True)


