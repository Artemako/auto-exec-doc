import sqlite3
import datetime
import os

import package.modules.dirpathsmanager as dirpathsmanager
import package.modules.log as log
import package.modules.project as project


class Database:
    _conn_db_settings = None
    _сurs_db_settings = None

    def __init__(self):
        pass

    @staticmethod
    def get_conn_db_settings():
        log.Log.debug_logger("get_conn_db_settings()")
        return Database._conn_db_settings

    @staticmethod
    def get_curs_db_settings():
        log.Log.debug_logger("get_curs_db_settings()")
        return Database._сurs_db_settings

    @staticmethod
    def set_conn_db_settings(value):
        log.Log.debug_logger("set_conn_db_settings()")
        Database._conn_db_settings = value

    @staticmethod
    def set_curs_db_settings(value):
        log.Log.debug_logger("set_curs_db_settings()")
        Database._сurs_db_settings = value

    @staticmethod
    def create_and_config_db():
        """
        Настройка базы данных перед использованием приложения
        """
        log.Log.debug_logger("IN create_and_config_db()")
        if not os.path.exists(dirpathsmanager.DirPathManager.get_db_settings_dirpath()):
            # Добавляем данные в пустую БД
            Database.set_conn_db_settings(
                sqlite3.connect(
                    dirpathsmanager.DirPathManager.get_db_settings_dirpath()
                )
            )
            Database.add_tables_and_datas_to_empty_db_settings()
        else:
            Database.set_conn_db_settings(
                sqlite3.connect(
                    dirpathsmanager.DirPathManager.get_db_settings_dirpath()
                )
            )
        Database.set_curs_db_settings(Database.get_conn_db_settings().cursor())

    # region Методы add (tables, values)
    @staticmethod
    def add_tables_and_datas_to_empty_db_settings():
        """
        Добавление таблиц и данных в БД программы.
        """
        log.Log.debug_logger("IN add_tables_and_datas_to_empty_db_settings()")
        cursor = Database.get_curs_db_settings()

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

    @staticmethod
    def add_new_project_to_db():
        """
        Добавление в БД новый проекта.
        """
        log.Log.debug_logger("IN add_new_project_to_db()")

        name_project = os.path.basename(
            dirpathsmanager.DirPathManager.get_project_dirpath()
        )
        directory_project = dirpathsmanager.DirPathManager.get_project_dirpath()

        cursor = Database.get_curs_db_settings()

        # текущее время для date_create_project и для date_last_open_project
        current_datetime = datetime.datetime.now().replace(microsecond=0)

        cursor.execute(
            "INSERT INTO Projects (name_project, directory_project, date_create_project, date_last_open_project) VALUES (?, ?, ?, ?)",
            (name_project, directory_project, current_datetime, current_datetime),
        )

        Database.get_conn_db_settings().commit()

    @staticmethod
    def update_project_to_db():
        """
        Обновление проекта в БД.
        """
        log.Log.debug_logger("IN update_project_to_db()")
        name_project = os.path.basename(
            dirpathsmanager.DirPathManager.get_project_dirpath()
        )
        directory_project = dirpathsmanager.DirPathManager.get_project_dirpath()

        cursor = Database.get_curs_db_settings()

        # текущее время для date_last_open_project
        current_datetime = datetime.datetime.now().replace(microsecond=0)

        cursor.execute(
            "UPDATE Projects SET date_last_open_project = ? WHERE name_project = ? AND directory_project = ?",
            (current_datetime, name_project, directory_project),
        )

        Database.get_conn_db_settings().commit()



    @staticmethod
    def add_or_update_open_project_to_db():
        """
        Добавление или обновление открытого проекта в БД.
        """
        log.Log.debug_logger("IN add_or_update_open_project_to_db()")
        name_project = os.path.basename(
            dirpathsmanager.DirPathManager.get_project_dirpath()
        )
        directory_project = dirpathsmanager.DirPathManager.get_project_dirpath()

        cursor = Database.get_curs_db_settings()

        # узнать, если проект в БД по имени и директории
        cursor.execute(
            "SELECT * FROM Projects WHERE name_project = ? AND directory_project = ?",
            (name_project, directory_project),
        )
        result = cursor.fetchone()
        print(result)

        if result is None:
            Database.add_new_project_to_db()
        else:
            Database.update_project_to_db()

        


    # endregion
