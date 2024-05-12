import sqlite3
import datetime
import os

import package.modules.dirpathsmanager as dirpathsmanager
import package.modules.log as log
import package.modules.project as project


class SettingsDatabase:
    
    def create_and_config_db_settings(self):
        """
        Настройка базы данных перед использованием приложения
        """
        log.obj_l.debug_logger("IN create_and_config_db_settings()")
        if not os.path.exists(dirpathsmanager.obj_dpm.get_db_settings_dirpath()):
            # Добавляем данные в пустую БД
            self.add_tables_and_datas_to_empty_db_settings()

    # region Методы add (tables, values)
    
    def add_tables_and_datas_to_empty_db_settings(self):
        """
        Добавление таблиц и данных в БД программы.
        """
        log.obj_l.debug_logger("IN add_tables_and_datas_to_empty_db_settings()")
        conn = sqlite3.connect(dirpathsmanager.obj_dpm.get_db_settings_dirpath())
        cursor = conn.cursor()

        cursor.executescript("""
        BEGIN TRANSACTION;
        CREATE TABLE IF NOT EXISTS "Projects" (
            "id_project"	INTEGER NOT NULL UNIQUE,
            "name_project"	TEXT NOT NULL,
            "directory_project"	TEXT NOT NULL,
            "date_create_project"	TEXT NOT NULL,
            "date_last_open_project"	TEXT NOT NULL,
            PRIMARY KEY("id_project" AUTOINCREMENT)
        );
        COMMIT;
        """)

        conn.commit()
        conn.close()

    
    def add_new_project_to_db(self):
        """
        Добавление в БД новый проекта.
        """
        log.obj_l.debug_logger("IN add_new_project_to_db()")

        conn = sqlite3.connect(dirpathsmanager.obj_dpm.get_db_settings_dirpath())
        cursor = conn.cursor()

        name_project = os.path.basename(
            dirpathsmanager.obj_dpm.get_project_dirpath()
        )
        directory_project = dirpathsmanager.obj_dpm.get_project_dirpath()        

        # текущее время для date_create_project и для date_last_open_project
        current_datetime = datetime.datetime.now().replace(microsecond=0)

        cursor.execute(
            "INSERT INTO Projects (name_project, directory_project, date_create_project, date_last_open_project) VALUES (?, ?, ?, ?)",
            (name_project, directory_project, current_datetime, current_datetime),
        )

        conn.commit()
        conn.close()

    
    def update_project_to_db(self):
        """
        Обновление проекта в БД.
        """
        log.obj_l.debug_logger("IN update_project_to_db()")

        conn = sqlite3.connect(dirpathsmanager.obj_dpm.get_db_settings_dirpath())
        cursor = conn.cursor()

        name_project = os.path.basename(
            dirpathsmanager.obj_dpm.get_project_dirpath()
        )
        directory_project = dirpathsmanager.obj_dpm.get_project_dirpath()

        # текущее время для date_last_open_project
        current_datetime = datetime.datetime.now().replace(microsecond=0)

        cursor.execute(
            "UPDATE Projects SET date_last_open_project = ? WHERE name_project = ? AND directory_project = ?",
            (current_datetime, name_project, directory_project),
        )

        conn.commit()
        conn.close()

    
    def add_or_update_open_project_to_db(self):
        """
        Добавление или обновление открытого проекта в БД.
        """
        log.obj_l.debug_logger("IN add_or_update_open_project_to_db()")

        conn = sqlite3.connect(dirpathsmanager.obj_dpm.get_db_settings_dirpath())
        cursor = conn.cursor()

        name_project = os.path.basename(
            dirpathsmanager.obj_dpm.get_project_dirpath()
        )
        directory_project = dirpathsmanager.obj_dpm.get_project_dirpath()

        # узнать, если проект в БД по имени и директории
        cursor.execute(
            "SELECT * FROM Projects WHERE name_project = ? AND directory_project = ?",
            (name_project, directory_project),
        )
        result = cursor.fetchone()

        conn.commit()
        conn.close()

        if result is None:
            self.add_new_project_to_db()
        else:
            self.update_project_to_db()

    # endregion


obj_sd = SettingsDatabase()