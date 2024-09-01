import os
import time


class Project:
    def __init__(self):
        # по умолчанию None
        self.__current_name = None
        # по умолчанию False
        self.__status_active = False
        self.__status_save = False

    def setting_all_osbm(self, osbm):
        self.__osbm = osbm
        self.__osbm.obj_logg.debug_logger("Project setting_all_osbm()")

    def is_active_status(self) -> bool:
        self.__osbm.obj_logg.debug_logger(
            f"Project is_active_status() -> bool: {self.__status_active}"
        )
        return self.__status_active

    def is_status_save(self) -> bool:
        self.__osbm.obj_logg.debug_logger(
            f"Project is_status_save() -> bool: {self.__status_save}"
        )
        return self.__status_save

    def check_project_before_new_or_open(self) -> bool:
        """
        Проверка текущего проекта до создания или открытия нового.
        """
        self.__osbm.obj_logg.debug_logger(
            "Project check_project_before_new_or_open()"
        )
        # появление диалогового окна, когда проект активен, но не сохранен
        if self.__status_active and not self.__status_save:
            answer = self.__osbm.obj_dw.save_active_project()
            if answer == "Yes":
                self.save_project()
                return True
            elif answer == "Cancel":
                # отменяет создание проекта
                return False
        return True

    def set_project_dirpaths(self, folder_path: str):
        """
        Установка путей к папке проекта.
        Установка пути к project.db проекта.
        """
        self.__osbm.obj_logg.debug_logger(
            f"Project set_project_dirpaths(folder_path: str):\nfolder_path = {folder_path}"
        )
        # Установка пути к папке проекта
        self.__osbm.obj_dirm.set_project_dirpath(folder_path)
        # Установка пути к project.db проекта
        self.__osbm.obj_dirm.set_db_project_dirpath(
            os.path.join(self.__osbm.obj_dirm.get_project_dirpath(), "project.db")
        )

    def new_project(self):
        """
        Действие создание проекта.
        """
        self.__osbm.obj_logg.debug_logger("Project new_project()")
        # продолжить, если проверка успешна и не отменена
        if self.check_project_before_new_or_open():
            # выбор директории будущего проекта
            folder_path = self.__osbm.obj_dw.select_folder_for_new_project()
            if folder_path:
                self.set_project_dirpaths(folder_path)
                self.clear_window_before_new_or_open_project()
                self.config_new_project()

    def clear_window_before_new_or_open_project(self):
        self.__osbm.obj_logg.debug_logger(
            "Project clear_window_before_new_or_open_project()"
        )
        # очистка structureexecdoc
        self.__osbm.obj_twsed.clear_sed()
        # очистка comboxts
        self.__osbm.obj_comt.clear_comboxts()
        # очистка pages_template
        self.__osbm.obj_lwpt.clear_pt()
        # очистка pdfview
        self.__osbm.obj_pdfv.set_empty_pdf_view()
        # очистка inputforms
        self.__osbm.obj_saif.delete_all_widgets_in_sa()

    def config_new_project(self):
        """
        Конфигурация нового проекта.
        """
        self.__osbm.obj_logg.debug_logger("Project config_new_project()")

        self.__current_name = os.path.basename(
            self.__osbm.obj_dirm.get_project_dirpath()
        )
        self.__osbm.obj_setdb.set_project_current_name(self.__current_name)

        self.__osbm.obj_setdb.add_new_project_to_db()
        self.__osbm.obj_prodb.create_and_config_db_project()
        # настраиваем контроллеры
        # обновляем окно
        self.__osbm.obj_mw.update_main_window()
        # пути для проекта
        self.__osbm.obj_dirm.set_new_dirpaths_for_project()
        # добавляем папки в новый проект
        self.__osbm.obj_film.create_folders_and_aed_for_project()
        # активируем проект
        self.set_true_actives_project()
        # сообщение для статусбара
        self.__osbm.obj_stab.set_message(
            f"Проект c именем {self.__current_name} создан и открыт."
        )
        # обновляем меню
        self.__osbm.obj_mw.update_menu_recent_projects()

    def save_project(self):
        """
        Сохранение проекта.
        """
        self.__osbm.obj_logg.debug_logger("Project save_project()")
        if self.__status_active:
            # сохранить в базу данных
            self.__osbm.obj_dw.process_save_start()
            self.__osbm.obj_seci.save_data_to_database()
            if self.__osbm.obj_lwpt.is_page_template_selected():
                # получить значение высоты страницы
                saved_view_height = self.__osbm.obj_pdfv.get_view_height()
                # сохранить в pdf (обработчик ошибок внутри obj_lwpt)
                self.__osbm.obj_lwpt.current_page_to_pdf()
                # восстановить высоту страницы
                self.__osbm.obj_pdfv.set_view_height(saved_view_height)
            # настроить статус
            self.__status_save = True
            self.__osbm.obj_stab.set_message(
                f"Проект c именем {self.__current_name} сохранён."
            )
            self.__osbm.obj_dw.process_save_end()
        else:
            self.__osbm.obj_stab.set_message(
                "Нечего сохранять. Либо проект не открыт, либо форма не выбрана."
            )
            self.__osbm.obj_dw.warning_message(
                "Нечего сохранять.\nЛибо проект не открыт, либо форма не выбрана.",
            )

    def saveas_project(self):
        """
        Сохранение проекта под новым именем или в новом месте.
        """
        self.__osbm.obj_logg.debug_logger("Project saveas_project()")
        if self.__status_active:
            old_folder_path = self.__osbm.obj_dirm.get_project_dirpath()
            # Запрашиваем новое имя или новую директорию для сохранения
            new_folder_path = (
                self.__osbm.obj_dw.select_folder_for_saveas_project()
            )
            if new_folder_path:
                # Установка путей к новому проекту
                self.set_project_dirpaths(new_folder_path)
                # копирование проекта
                self.__osbm.obj_film.copy_project_for_saveas(
                    old_folder_path, new_folder_path
                )
                # открытие проекта
                self.config_open_project()
            else:
                self.__osbm.obj_stab.set_message("Сохранение отменено.")
                self.__osbm.obj_dw.warning_message("Сохранение отменено.")
        else:
            self.__osbm.obj_stab.set_message(
                "Нечего сохранять. Либо проект не открыт, либо форма не выбрана."
            )

    def open_project(self):
        """Открытие проекта."""
        self.__osbm.obj_logg.debug_logger("Project open_project()")
        # продолжить, если проверка успешна и не отменена
        if self.check_project_before_new_or_open():
            # выбор директории будущего проекта
            folder_path = self.__osbm.obj_dw.select_folder_for_open_project()
            if folder_path:
                self.set_project_dirpaths(folder_path)
                self.clear_window_before_new_or_open_project()
                self.config_open_project()

    def config_open_project(self):
        """
        Конфигурация открытого проекта.
        """
        self.__osbm.obj_logg.debug_logger("Project config_open_project()")

        self.__current_name = os.path.basename(
            self.__osbm.obj_dirm.get_project_dirpath()
        )
        self.__osbm.obj_setdb.set_project_current_name(self.__current_name)
        # настраиваем базы данных
        self.__osbm.obj_setdb.add_or_update_open_project_to_db()
        self.__osbm.obj_prodb.create_and_config_db_project()
        # обновляем окно
        self.__osbm.obj_mw.update_main_window()
        # пути для проекта
        self.__osbm.obj_dirm.set_new_dirpaths_for_project()

        self.set_true_actives_project()
        # сообщение для статусбара
        self.__osbm.obj_stab.set_message(
            f"Проект c именем {self.__current_name} открыт."
        )
        # добавляем папки в новый проект
        self.__osbm.obj_film.create_folders_and_aed_for_project()
        # обновляем меню
        self.__osbm.obj_mw.update_menu_recent_projects()

    def open_recent_project(self, project):
        """Открытие недавнего проекта."""
        self.__osbm.obj_logg.debug_logger(
            f"Project open_recent_project(project):\nproject = {project}"
        )
        directory_project = project.get("directory_project")
        if os.path.exists(directory_project):
            self.set_project_dirpaths(directory_project)
            self.clear_window_before_new_or_open_project()
            self.config_open_project()
        else:
            self.__osbm.obj_dw.warning_message(
                f"Проект с именем {project.get('name_project')} не существует."
            )
            # удаляем проект из БД и обновляем меню
            self.__osbm.obj_setdb.delete_project_from_db(project)
            self.__osbm.obj_mw.update_menu_recent_projects()

    def set_true_actives_project(self):
        """
        Задает активность проекта.
        """
        self.__osbm.obj_logg.debug_logger("Project set_true_actives_project()")
        self.__status_active = True
        self.__status_save = True
        # активировать qactions в статусбаре
        self.__osbm.obj_mw.enable_qt_actions()
        # значение по умолчанию включить
        self.__osbm.obj_mw.config_combox_default()
        # очистить список выбранных секций
        self.__osbm.obj_saif.clear_sections_checked()


    def export_to_pdf(self):
        """
        Экспорт проекта в pdf.
        """
        self.__osbm.obj_logg.debug_logger("Project export_to_pdf()")
        multipage_pdf_path = (
            self.__osbm.obj_dw.select_name_and_dirpath_export_pdf()
        )
        if multipage_pdf_path:
            self.__osbm.obj_stab.set_message("Процесс экспорта в PDF...")
            # проверка на доступность конвертера
            flag_converter = False
            app_converter = self.__osbm.obj_setdb.get_app_converter()
            status_msword = self.__osbm.obj_offp.get_status_msword()
            status_libreoffice = self.__osbm.obj_offp.get_status_libreoffice()
            if app_converter == "MSWORD" and status_msword:
                flag_converter = True
            elif app_converter == "LIBREOFFICE" and status_libreoffice:
                flag_converter = True
            #
            if flag_converter:
                self.__osbm.obj_dw.process_export_start()
                start_time = time.time()
                try:
                    self.__osbm.obj_conv.export_to_pdf(multipage_pdf_path)
                    end_time = time.time()
                    self.__osbm.obj_stab.set_message(
                        f"Экспорт завершен. Файл {multipage_pdf_path} готов."
                    )
                    # открыть pdf
                    os.startfile(os.path.dirname(multipage_pdf_path))
                    self.__osbm.obj_logg.debug_logger(
                        f"Project export_to_pdf() -> time: {end_time - start_time}"
                    )
                    
                except self.__osbm.obj_com.errors.MsWordError:
                    msg = "Экспорт отменён! Выбранный конвертер перестал работать."
                    self.__osbm.obj_dw.warning_message(msg)
                    self.__osbm.obj_stab.set_message(msg)
                    self.__osbm.obj_offp.terminate_msword()
                    self.__osbm.obj_stab.update_status_msword_label(False)

                except self.__osbm.obj_com.errors.LibreOfficeError:
                    msg = "Экспорт отменён! Выбранный конвертер перестал работать."
                    self.__osbm.obj_dw.warning_message(msg)
                    self.__osbm.obj_stab.set_message(msg)
                    self.__osbm.obj_offp.terminate_libreoffice()
                    self.__osbm.obj_stab.update_status_libreoffice_label(False)
                #
                self.__osbm.obj_dw.process_export_end()
            else:
                msg = "Экспорт отменён! Выбранный конвертер не работает."
                self.__osbm.obj_dw.warning_message(msg)
                self.__osbm.obj_stab.set_message(msg)


# obj_proj = Project()
