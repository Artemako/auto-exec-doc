import sqlite3
import datetime
import os

class SettingsDatabase:
    
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager 

    def create_and_config_db_settings(self):
        """
        Настройка базы данных перед использованием приложения
        """
        self.__obs_manager.obj_l.debug_logger("IN create_and_config_db_settings()")
        if not os.path.exists(self.__obs_manager.obj_dpm.get_db_settings_dirpath()):
            # создать путь
            os.mkdir(self.__obs_manager.obj_dpm.get_db_settings_dirpath())
            # Добавляем данные в пустую БД
            self.add_tables_and_datas_to_empty_db_settings()

    # region Методы add (tables, values)
    
    def add_tables_and_datas_to_empty_db_settings(self):
        """
        Добавление таблиц и данных в БД программы.
        """
        self.__obs_manager.obj_l.debug_logger("IN add_tables_and_datas_to_empty_db_settings()")
        conn = sqlite3.connect(self.__obs_manager.obj_dpm.get_db_settings_dirpath())
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
CREATE TABLE IF NOT EXISTS "Settings" (
	"id_setting"	INTEGER NOT NULL UNIQUE,
	"name_setting"	TEXT NOT NULL UNIQUE,
	"value_setting"	TEXT,
	PRIMARY KEY("id_setting" AUTOINCREMENT)
);
INSERT INTO "Settings" VALUES (1,'app_converter','LIBREOFFICE');
COMMIT;
        """)

        conn.commit()
        conn.close()

    
    def get_conn(self) -> object:
        """
        Запрос курсора.
        """
        self.__obs_manager.obj_l.debug_logger("get_conn() -> object")
        conn = sqlite3.connect(self.__obs_manager.obj_dpm.get_db_settings_dirpath())
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_fetchall(self, cursor):
        self.__obs_manager.obj_l.debug_logger("get_fetchall(cursor, conn) -> list")
        cursor_result = cursor.fetchall()
        result = [dict(row) for row in cursor_result] if cursor_result else []
        return result

    def get_fetchone(self, cursor):
        self.__obs_manager.obj_l.debug_logger("get_fetchone(cursor, conn) -> list")
        cursor_result = cursor.fetchone()
        result = dict(cursor_result) if cursor_result else {}
        return result

    def add_new_project_to_db(self):
        """
        Добавление в БД новый проекта.
        """
        self.__obs_manager.obj_l.debug_logger("IN add_new_project_to_db()")

        conn = self.get_conn()
        cursor = conn.cursor()

        name_project = os.path.basename(
            self.__obs_manager.obj_dpm.get_project_dirpath()
        )
        directory_project = self.__obs_manager.obj_dpm.get_project_dirpath()        

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
        self.__obs_manager.obj_l.debug_logger("IN update_project_to_db()")

        conn = self.get_conn()
        cursor = conn.cursor()

        name_project = os.path.basename(
            self.__obs_manager.obj_dpm.get_project_dirpath()
        )
        directory_project = self.__obs_manager.obj_dpm.get_project_dirpath()

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
        self.__obs_manager.obj_l.debug_logger("IN add_or_update_open_project_to_db()")

        conn = self.get_conn()
        cursor = conn.cursor()

        name_project = os.path.basename(
            self.__obs_manager.obj_dpm.get_project_dirpath()
        )
        directory_project = self.__obs_manager.obj_dpm.get_project_dirpath()

        # узнать, если проект в БД по имени и директории
        cursor.execute(
            "SELECT * FROM Projects WHERE name_project = ? AND directory_project = ?",
            (name_project, directory_project),
        )
        result = self.get_fetchone(cursor)

        conn.commit()
        conn.close()

        if result is None:
            self.add_new_project_to_db()
        else:
            self.update_project_to_db()

    def get_app_converter(self) -> str:
        """
        Запрос значения app_converter из БД.
        """
        self.__obs_manager.obj_l.debug_logger("IN get_app_converter()")

        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute("SELECT value_setting FROM Settings WHERE name_setting = 'app_converter'")

        result = self.get_fetchone(cursor)
        conn.close()

        if result is None:
            return None
        else:
            return result.get("value_setting")

    def set_app_converter(self, app_converter: str):
        """
        Установка значения app_converter в БД.
        """
        self.__obs_manager.obj_l.debug_logger(f"IN set_app_converter(app_converter):\napp_converter = {app_converter}")

        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE Settings SET value_setting = ? WHERE name_setting = 'app_converter'",
            (app_converter,),
        )

        conn.commit()
        conn.close()

# obj_sd = SettingsDatabase()