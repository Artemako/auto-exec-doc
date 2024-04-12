import sqlite3
import datetime

import package.modules.dirpathsmanager as dirpathsmanager


class Database:
    con_db_settings = None

    def __init__(self):
        pass

    @staticmethod
    def create_and_config_database():
        """
        Настройка базы данных перед использованием приложения
        """
        # Подключение к БД
        Database.con_db_settings = sqlite3.connect(
            dirpathsmanager.DirPathManager.get_db_settings_dirpath()
        )

        # Добавление таблиц в БД
        Database.add_tables_to_db_settings()

    # region Методы is
    @staticmethod
    def is_exists_table_projects() -> bool:
        """
        Проверка наличия таблицы Projects в БД
        """
        cursor = Database.con_db_settings.cursor()

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='Projects'"
        )

        table_exists = cursor.fetchall()
        if table_exists:
            return True
        else:
            return False

    # endregion

    # region Методы add (tables, values)
    @staticmethod
    def add_tables_to_db_settings():
        """
        Добавление таблиц в БД программы при запуске.
        """
        cursor = Database.con_db_settings.cursor()

        if not Database.is_exists_table_projects():
            cursor.execute("""
            CREATE TABLE "Projects" (
                "id_project"	INTEGER NOT NULL UNIQUE,
                "name_project"	TEXT NOT NULL,
                "directory_project"	TEXT NOT NULL,
                "date_create_project"	TEXT NOT NULL,
                "date_last_open_project"	TEXT NOT NULL,
                PRIMARY KEY("id_project" AUTOINCREMENT)
            );
            """)

    @staticmethod
    def add_new_project_to_db(name_project, directory_project):
        """
        Добавление в БД новый проекта.
        """
        cursor = Database.con_db_settings.cursor()

        # текущее время для date_create_project и для date_last_open_project
        current_datetime = datetime.datetime.now().replace(microsecond=0)

        cursor.execute(
            "INSERT INTO Projects (name_project, directory_project, date_create_project, date_last_open_project) VALUES (?, ?, ?, ?)",
            (name_project, directory_project, current_datetime, current_datetime),
        )

        Database.con_db_settings.commit()

    @staticmethod
    def add_or_update_open_project_to_db(name_project, directory_project):
        """
        Добапвление или обновление открытого проекта в БД.
        """
        cursor = Database.con_db_settings.cursor()

        # узнать, если проект в БД по имени и директории
        cursor.execute(
            "SELECT * FROM Projects WHERE name_project = ? AND directory_project = ?",
            (name_project, directory_project),
        )
        print(cursor.fetchone())
        # TODO Сделать логи
        # TODO Сделать UPDATE

        # if cursor.fetchone() is not None:
        #     Database.add_new_project_to_db(name_project, directory_project)
        # else:
        #     Database.update_project_to_db()

    # endregion
