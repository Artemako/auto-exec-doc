import os
import time

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
    def __init__(self):
        # по умолчанию None
        self.__current_name = None
        # по умолчанию False
        self.__status_active = False
        self.__status_save = False

    # region методы get

    def get_current_name(self) -> str:
        log.obj_l.debug_logger(f"get_current_name() -> str: {self.__current_name}")
        return self.__current_name

    # endregion
    # region методы is, check

    def is_active_status(self) -> bool:
        log.obj_l.debug_logger(f"is_active_status() -> bool: {self.__status_active}")
        return self.__status_active

    def is_status_save(self) -> bool:
        log.obj_l.debug_logger(f"is_status_save() -> bool: {self.__status_save}")
        return self.__status_save

    def check_project_before_new_or_open(self) -> bool:
        """
        Проверка текущего проекта до создания или открытия нового.
        """
        # появление диалогового окна, когда проект активен, но не сохранен
        if self.__status_active and not self.__status_save:
            answer = dialogwindows.obj_dw.save_active_project()
            if answer == "Yes":
                self.save_project()
                return True
            elif answer == "Cancel":
                # отменяет создание проекта
                return False
        return True

    # endregion

    def set_project_dirpaths(self, folder_path: str):
        """
        Установка путей к папке проекта.
        Установка пути к project.db проекта.
        """
        log.obj_l.debug_logger(
            f"IN set_project_dirpaths(folder_path: str): folder_path = {folder_path}"
        )
        # Установка пути к папке проекта
        dirpathsmanager.obj_dpm.set_project_dirpath(folder_path)
        # Установка пути к project.db проекта
        dirpathsmanager.obj_dpm.set_db_project_dirpath(
            os.path.join(
                dirpathsmanager.obj_dpm.get_project_dirpath(), "project.db"
            )
        )

    def new_project(self):
        """
        Действие создание проекта.
        """
        log.obj_l.debug_logger("IN new_project()")
        # продолжить, если проверка успешна и не отменена
        if self.check_project_before_new_or_open():
            # выбор директории будущего проекта
            folder_path = dialogwindows.obj_dw.select_folder_for_new_project()
            if folder_path:
                self.set_project_dirpaths(folder_path)
                self.config_new_project()

    def config_new_project(self):
        """
        Конфигурация нового проекта.
        """
        log.obj_l.debug_logger("IN config_new_project()")

        self.__current_name = os.path.basename(
            dirpathsmanager.obj_dpm.get_project_dirpath()
        )

        settingsdatabase.obj_sd.add_new_project_to_db()
        projectdatabase.obj_pd.create_and_config_db_project()
        # настраиваем контроллеры
        # настраиваем структуру execdoc
        structureexecdoc.obj_sed.update_structure_exec_doc()
        pagestemplate.obj_pt.create_pages_template()
        # пути для проекта
        dirpathsmanager.obj_dpm.set_new_dirpaths_for_project()
        # добавляем папки форм в новый проект
        filefoldermanager.obj_ffm.create_folders_for_new_project()
        filefoldermanager.obj_ffm.copy_templates_to_forms_folder()
        # активируем проект
        self.set_true_actives_project()
        # сообщение для статусбара
        statusbar.obj_sb.set_message_for_statusbar(
            f"Проект c именем {self.__current_name} создан и открыт."
        )

    def save_project(self):
        """
        Сохранение проекта.
        """
        log.obj_l.debug_logger("IN save_project()")
        if self.__status_active and pagestemplate.obj_pt.is_page_template_selected():
            # сохранить в базу данных
            sectionsinfo.obj_si.save_data_to_database()
            # NOT (current_page_to_pdf() расположен в save_data_to_database())
            pagestemplate.obj_pt.current_page_to_pdf()
            # настроить статус
            self.__status_save = True
            statusbar.obj_sb.set_message_for_statusbar(
                f"Проект c именем {self.__current_name} сохранён."
            )
        else:
            statusbar.obj_sb.set_message_for_statusbar(
                "Нечего сохранять. Либо проект не открыт, либо форма не выбрана."
            )
            dialogwindows.obj_dw.warning_message(
                "Нечего сохранять.\nЛибо проект не открыт, либо форма не выбрана.",
            )

    def open_project(self):
        """Открытие проекта."""
        log.obj_l.debug_logger("IN open_project()")
        # продолжить, если проверка успешна и не отменена
        if self.check_project_before_new_or_open():
            # выбор директории будущего проекта
            folder_path = dialogwindows.obj_dw.select_folder_for_open_project()
            if folder_path:
                self.set_project_dirpaths(folder_path)
                self.config_open_project()

    def config_open_project(self):
        """
        Конфигурация открытого проекта.
        """
        log.obj_l.debug_logger("IN config_open_project()")

        self.__current_name = os.path.basename(
            dirpathsmanager.obj_dpm.get_project_dirpath()
        )
        # настраиваем базы данных
        settingsdatabase.obj_sd.add_or_update_open_project_to_db()
        projectdatabase.obj_pd.create_and_config_db_project()
        # настраиваем структуру execdoc
        structureexecdoc.obj_sed.update_structure_exec_doc()
        # пути для проекта
        dirpathsmanager.obj_dpm.set_new_dirpaths_for_project()
        # добавляем папки в новый проект
        filefoldermanager.obj_ffm.create_folders_for_new_project()

        self.set_true_actives_project()
        # сообщение для статусбара
        statusbar.obj_sb.set_message_for_statusbar(
            f"Проект c именем {self.__current_name} открыт."
        )

    def open_recent_project(self):
        """Открытие недавнего проекта."""
        log.obj_l.debug_logger("IN open_recent_project()")
        # TODO open_recent_project
        pass

    def set_true_actives_project(self):
        """
        Задает активность проекта.
        """
        log.obj_l.debug_logger("IN set_true_actives_project()")
        self.__status_active = True
        self.__status_save = True

    def export_to_pdf(self):
        """
        Экспорт проекта в pdf.
        """
        log.obj_l.debug_logger("IN export_to_pdf()")
        if not self.__status_active:
            statusbar.obj_sb.set_message_for_statusbar(
                "Нечего экспортировать. Проект не открыт."
            )
            dialogwindows.obj_dw.warning_message(
                "Нечего экспортировать.\nПроект не открыт."
            )
            return False

        multipage_pdf_path = dialogwindows.obj_dw.select_name_and_dirpath_export_pdf()
        if multipage_pdf_path:
            start_time = time.time()
            statusbar.obj_sb.set_message_for_statusbar("Процесс экспорта в PDF...")
            converter.obj_c.export_to_pdf(multipage_pdf_path)
            end_time = time.time()
            log.obj_l.debug_logger(f"export_to_pdf() -> time: {end_time - start_time}")



obj_p = Project()