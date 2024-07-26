import os
import time

class Project:
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager 
        # по умолчанию None
        self.__current_name = None
        # по умолчанию False
        self.__status_active = False
        self.__status_save = False

    # region методы get

    def get_current_name(self) -> str:
        self.__obs_manager.obj_l.debug_logger(f"get_current_name() -> str: {self.__current_name}")
        return self.__current_name

    # endregion
    # region методы is, check

    def is_active_status(self) -> bool:
        self.__obs_manager.obj_l.debug_logger(f"is_active_status() -> bool: {self.__status_active}")
        return self.__status_active

    def is_status_save(self) -> bool:
        self.__obs_manager.obj_l.debug_logger(f"is_status_save() -> bool: {self.__status_save}")
        return self.__status_save

    def check_project_before_new_or_open(self) -> bool:
        """
        Проверка текущего проекта до создания или открытия нового.
        """
        # появление диалогового окна, когда проект активен, но не сохранен
        if self.__status_active and not self.__status_save:
            answer = self.__obs_manager.obj_dw.save_active_project()
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
        self.__obs_manager.obj_l.debug_logger(
            f"IN set_project_dirpaths(folder_path: str):\nfolder_path = {folder_path}"
        )
        # Установка пути к папке проекта
        self.__obs_manager.obj_dpm.set_project_dirpath(folder_path)
        # Установка пути к project.db проекта
        self.__obs_manager.obj_dpm.set_db_project_dirpath(
            os.path.join(
                self.__obs_manager.obj_dpm.get_project_dirpath(), "project.db"
            )
        )

    def new_project(self):
        """
        Действие создание проекта.
        """
        self.__obs_manager.obj_l.debug_logger("IN new_project()")
        # продолжить, если проверка успешна и не отменена
        if self.check_project_before_new_or_open():
            # выбор директории будущего проекта
            folder_path = self.__obs_manager.obj_dw.select_folder_for_new_project()
            if folder_path:
                self.set_project_dirpaths(folder_path)
                self.config_new_project()

    def config_new_project(self):
        """
        Конфигурация нового проекта.
        """
        self.__obs_manager.obj_l.debug_logger("IN config_new_project()")

        self.__current_name = os.path.basename(
            self.__obs_manager.obj_dpm.get_project_dirpath()
        )

        self.__obs_manager.obj_sd.add_new_project_to_db()
        self.__obs_manager.obj_pd.create_and_config_db_project()
        # настраиваем контроллеры
        # настраиваем структуру execdoc
        self.__obs_manager.obj_sed.update_structure_exec_doc()
        self.__obs_manager.obj_pt.create_pages_template()
        # пути для проекта
        self.__obs_manager.obj_dpm.set_new_dirpaths_for_project()
        # добавляем папки форм в новый проект
        self.__obs_manager.obj_ffm.create_folders_and_aed_for_project()
        self.__obs_manager.obj_ffm.copy_templates_to_forms_folder()
        # активируем проект
        self.set_true_actives_project()
        # сообщение для статусбара
        self.__obs_manager.obj_sb.set_message_for_statusbar(
            f"Проект c именем {self.__current_name} создан и открыт."
        )

    def save_project(self):
        """
        Сохранение проекта.
        """
        self.__obs_manager.obj_l.debug_logger("IN save_project()")
        if self.__status_active:
            # сохранить в базу данных
            self.__obs_manager.obj_si.save_data_to_database()
            if self.__obs_manager.obj_pt.is_page_template_selected():
                # получить значение высоты страницы
                saved_view_height = self.__obs_manager.obj_mw.get_view_height()
                # сохранить в pdf
                self.__obs_manager.obj_pt.current_page_to_pdf()
                # восстановить высоту страницы
                self.__obs_manager.obj_mw.set_view_height(saved_view_height)
            # настроить статус
            self.__status_save = True
            self.__obs_manager.obj_sb.set_message_for_statusbar(
                f"Проект c именем {self.__current_name} сохранён."
            )
        else:
            self.__obs_manager.obj_sb.set_message_for_statusbar(
                "Нечего сохранять. Либо проект не открыт, либо форма не выбрана."
            )
            self.__obs_manager.obj_dw.warning_message(
                "Нечего сохранять.\nЛибо проект не открыт, либо форма не выбрана.",
            )

    def saveas_project(self):
        """
        Сохранение проекта под новым именем или в новом месте.
        """
        self.__obs_manager.obj_l.debug_logger("IN saveas_project()")
        if self.__status_active:
            old_folder_path = self.__obs_manager.obj_dpm.get_project_dirpath()
            # Запрашиваем новое имя или новую директорию для сохранения
            new_folder_path = self.__obs_manager.obj_dw.select_folder_for_saveas_project()
            if new_folder_path:
                # Установка путей к новому проекту
                self.set_project_dirpaths(new_folder_path)
                # копирование проекта 
                self.__obs_manager.obj_ffm.copy_project_for_saveas(
                    old_folder_path, new_folder_path
                )    
                # открытие проекта
                self.config_open_project()                          
            else:
                self.__obs_manager.obj_sb.set_message_for_statusbar("Сохранение отменено.")
                self.__obs_manager.obj_dw.warning_message("Сохранение отменено.")
        else:
            self.__obs_manager.obj_sb.set_message_for_statusbar(
                "Нечего сохранять. Либо проект не открыт, либо форма не выбрана."
            )


    def open_project(self):
        """Открытие проекта."""
        self.__obs_manager.obj_l.debug_logger("IN open_project()")
        # продолжить, если проверка успешна и не отменена
        if self.check_project_before_new_or_open():
            # выбор директории будущего проекта
            folder_path = self.__obs_manager.obj_dw.select_folder_for_open_project()
            if folder_path:
                self.set_project_dirpaths(folder_path)
                self.config_open_project()

    def config_open_project(self):
        """
        Конфигурация открытого проекта.
        """
        self.__obs_manager.obj_l.debug_logger("IN config_open_project()")

        self.__current_name = os.path.basename(
            self.__obs_manager.obj_dpm.get_project_dirpath()
        )
        # настраиваем базы данных
        self.__obs_manager.obj_sd.add_or_update_open_project_to_db()
        self.__obs_manager.obj_pd.create_and_config_db_project()
        # настраиваем структуру execdoc
        self.__obs_manager.obj_sed.update_structure_exec_doc()
        # пути для проекта
        self.__obs_manager.obj_dpm.set_new_dirpaths_for_project()

        self.set_true_actives_project()
        # сообщение для статусбара
        self.__obs_manager.obj_sb.set_message_for_statusbar(
            f"Проект c именем {self.__current_name} открыт."
        )
        # добавляем папки в новый проект
        self.__obs_manager.obj_ffm.create_folders_and_aed_for_project()

    def open_recent_project(self):
        """Открытие недавнего проекта."""
        self.__obs_manager.obj_l.debug_logger("IN open_recent_project()")
        # TODO open_recent_project
        pass

    def set_true_actives_project(self):
        """
        Задает активность проекта.
        """
        self.__obs_manager.obj_l.debug_logger("IN set_true_actives_project()")
        self.__status_active = True
        self.__status_save = True
        # активировать qactions в статусбаре
        self.__obs_manager.obj_mw.enable_qt_actions()

    def export_to_pdf(self):
        """
        Экспорт проекта в pdf.
        """
        self.__obs_manager.obj_l.debug_logger("IN export_to_pdf()")
        multipage_pdf_path = self.__obs_manager.obj_dw.select_name_and_dirpath_export_pdf()
        if multipage_pdf_path:
            start_time = time.time()
            self.__obs_manager.obj_sb.set_message_for_statusbar("Процесс экспорта в PDF...")
            self.__obs_manager.obj_c.export_to_pdf(multipage_pdf_path)
            end_time = time.time()
            self.__obs_manager.obj_l.debug_logger(f"export_to_pdf() -> time: {end_time - start_time}")




# obj_p = Project()