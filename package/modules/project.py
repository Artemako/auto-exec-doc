import os

import package.components.dialogwindows as dialogwindows


import package.modules.settingsdatabase as settingsdatabase
import package.modules.projectdatabase as projectdatabase
import package.modules.log as log
import package.modules.filefoldermanager as filefoldermanager
import package.modules.dirpathsmanager as dirpathsmanager
import package.modules.sectionsinfo as sectionsinfo
import package.modules.converter as converter

import package.controllers.structureexecdoc as structureexecdoc
import package.controllers.pagestemplate as pagestemplate
import package.controllers.statusbar as statusbar


class Project:
    # по умолчанию None
    __current_name = None

    # по умолчанию False
    __status_active = False
    # TODO При редактировании __status_save = False
    __status_save = False

    def __init__(self):
        pass

    # region методы get

    @staticmethod
    def get_current_name() -> str:
        log.Log.debug_logger(f"get_current_name() -> str: {Project.__current_name}")
        return Project.__current_name

    # endregion
    # region методы is, check
    @staticmethod
    def is_active_status() -> bool:
        log.Log.debug_logger(f"is_active_status() -> bool: {Project.__status_active}")
        return Project.__status_active

    @staticmethod
    def is_status_save() -> bool:
        log.Log.debug_logger(f"is_status_save() -> bool: {Project.__status_save}")
        return Project.__status_save

    @staticmethod
    def check_project_before_new_or_open() -> bool:
        """
        Проверка текущего проекта до создания или открытия нового.
        """
        # появление диалогового окна, когда проект активен, но не сохранен
        if Project.__status_active and not Project.__status_save:
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

        Project.__current_name = os.path.basename(
            dirpathsmanager.DirPathManager.get_project_dirpath()
        )

        settingsdatabase.Database.add_new_project_to_db()
        projectdatabase.Database.create_and_config_db_project()
        # настраиваем контроллеры
        # настраиваем структуру execdoc
        structureexecdoc.StructureExecDoc.update_structure_exec_doc()
        pagestemplate.PagesTemplate.create_pages_template()
        # пути для проекта
        dirpathsmanager.DirPathManager.set_new_dirpaths_for_project()
        # добавляем папки форм в новый проект
        filefoldermanager.FileFolderManager.create_folders_for_new_project()
        filefoldermanager.FileFolderManager.copy_templates_to_forms_folder()
        # активируем проект
        Project.set_true_actives_project()
        # сообщение для статусбара
        statusbar.StatusBar.set_message_for_statusbar(
            f"Проект c именем {Project.__current_name} создан и открыт."
        )

    @staticmethod
    def save_project():
        """
        Сохранение проекта.
        """
        log.Log.debug_logger("IN save_project()")
        # TODO Сделать сохранение проекта
        if (
            Project.__status_active
            and pagestemplate.PagesTemplate.is_page_template_selected()
        ):
            # сохранить в базу данных
            sectionsinfo.SectionsInfo.save_data_to_database()
            # current_page_to_pdf() расположен в save_data_to_database()
            # настроить статус
            Project.__status_save = True
            statusbar.StatusBar.set_message_for_statusbar(
                f"Проект c именем {Project.__current_name} сохранён."
            )
        else:
            statusbar.StatusBar.set_message_for_statusbar(
                "Нечего сохранять. Либо проект не открыт, либо форма не выбрана."
            )
            dialogwindows.DialogWindows.warning_message(
                "Нечего сохранять.\nЛибо проект не открыт, либо форма не выбрана.",
            )

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

        Project.__current_name = os.path.basename(
            dirpathsmanager.DirPathManager.get_project_dirpath()
        )
        # настраиваем базы данных
        settingsdatabase.Database.add_or_update_open_project_to_db()
        projectdatabase.Database.create_and_config_db_project()
        # настраиваем структуру execdoc
        structureexecdoc.StructureExecDoc.update_structure_exec_doc()
        # пути для проекта
        dirpathsmanager.DirPathManager.set_new_dirpaths_for_project()
        # добавляем папки в новый проект
        filefoldermanager.FileFolderManager.create_folders_for_new_project()

        Project.set_true_actives_project()
        # сообщение для статусбара
        statusbar.StatusBar.set_message_for_statusbar(
            f"Проект c именем {Project.__current_name} открыт."
        )

    @staticmethod
    def open_recent_project():
        """Открытие недавнего проекта."""
        log.Log.debug_logger("IN open_recent_project()")
        # TODO open_recent_project
        pass

    @staticmethod
    def set_true_actives_project():
        """
        Задает активность проекта.
        """
        log.Log.debug_logger("IN set_true_actives_project()")
        Project.__status_active = True
        Project.__status_save = True

    @staticmethod
    def export_to_pdf():
        """
        Экспорт проекта в pdf.
        """
        log.Log.debug_logger("IN export_to_pdf()")
        if not Project.__status_active: 
            statusbar.StatusBar.set_message_for_statusbar(
                "Нечего экспортировать. Проект не открыт."
            )
            dialogwindows.DialogWindows.warning_message(
                "Нечего экспортировать.\nПроект не открыт."
            )
            return False
        
        multipage_pdf_path = dialogwindows.DialogWindows.select_name_and_dirpath_export_pdf()
        if multipage_pdf_path:
            converter.Converter.export_to_pdf(multipage_pdf_path)

        
    



        