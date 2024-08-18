import sqlite3
import datetime
import os

class SettingsDatabaseObjectsManager:
    def __init__(self, osbm):
        self.obj_logg = osbm.obj_logg
        self.obj_dirm = osbm.obj_dirm

class SettingsDatabase:
    def __init__(self):
        pass

    def setting_osbm(self, osbm):
        self.__osbm = SettingsDatabaseObjectsManager(osbm)

    def create_and_setting_db_settings(self):
        """
        Настройка базы данных перед использованием приложения
        """
        self.__osbm.obj_logg.debug_logger(
            "SettingsDatabase create_and_setting_db_settings()"
        )
        if not os.path.exists(self.__osbm.obj_dirm.get_db_settings_dirpath()):
            # создать путь
            os.mkdir(self.__osbm.obj_dirm.get_db_settings_dirpath())
            # Добавляем данные в пустую БД
            self.add_tables_and_datas_to_empty_db_settings()

    # region Методы add (tables, values)

    def add_tables_and_datas_to_empty_db_settings(self):
        """
        Добавление таблиц и данных в БД программы.
        """
        self.__osbm.obj_logg.debug_logger(
            "SettingsDatabase add_tables_and_datas_to_empty_db_settings()"
        )
        conn = sqlite3.connect(self.__osbm.obj_dirm.get_db_settings_dirpath())
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
INSERT INTO "Projects" VALUES (20,'gdgffdg','C:/Users/hayar/Documents/AutoExecDoc Projects/gdgffdg','2024-08-10 16:36:35','2024-08-10 16:54:21');
INSERT INTO "Projects" VALUES (21,'dsdf','C:/Users/hayar/Documents/AutoExecDoc Projects/dsdf','2024-08-10 16:57:31','2024-08-10 21:16:56');
INSERT INTO "Settings" VALUES (1,'app_converter','LIBREOFFICE');
INSERT INTO "Settings" VALUES (2,'libreoffice_path','C:\Program Files\LibreOffice\program\soffice.exe');
INSERT INTO "Settings" VALUES (3,'project_current_name',NULL);
COMMIT;
        """)

        conn.commit()
        conn.close()

    def get_conn(self) -> object:
        """
        Запрос курсора.
        """
        self.__osbm.obj_logg.debug_logger("SettingsDatabase get_conn() -> object")
        conn = sqlite3.connect(self.__osbm.obj_dirm.get_db_settings_dirpath())
        conn.row_factory = sqlite3.Row
        return conn

    def get_fetchall(self, cursor):
        self.__osbm.obj_logg.debug_logger(
            "SettingsDatabase get_fetchall(cursor, conn) -> list"
        )
        cursor_result = cursor.fetchall()
        result = [dict(row) for row in cursor_result] if cursor_result else []
        return result

    def get_fetchone(self, cursor):
        self.__osbm.obj_logg.debug_logger(
            "SettingsDatabase get_fetchone(cursor, conn) -> list"
        )
        cursor_result = cursor.fetchone()
        result = dict(cursor_result) if cursor_result else {}
        return result

    def add_new_project_to_db(self):
        """
        Добавление в БД новый проекта.
        """
        self.__osbm.obj_logg.debug_logger(
            "SettingsDatabase add_new_project_to_db()"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        name_project = os.path.basename(
            self.__osbm.obj_dirm.get_project_dirpath()
        )
        directory_project = self.__osbm.obj_dirm.get_project_dirpath()
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
        self.__osbm.obj_logg.debug_logger("SettingsDatabase update_project_to_db()")

        conn = self.get_conn()
        cursor = conn.cursor()
        name_project = os.path.basename(
            self.__osbm.obj_dirm.get_project_dirpath()
        )
        directory_project = self.__osbm.obj_dirm.get_project_dirpath()
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
        self.__osbm.obj_logg.debug_logger(
            "SettingsDatabase add_or_update_open_project_to_db()"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        name_project = os.path.basename(
            self.__osbm.obj_dirm.get_project_dirpath()
        )
        directory_project = self.__osbm.obj_dirm.get_project_dirpath()
        print(f"name_project = {name_project}")
        # узнать, если проект в БД по имени и директории
        cursor.execute(
            "SELECT * FROM Projects WHERE name_project = ? AND directory_project = ?",
            (name_project, directory_project),
        )
        result = self.get_fetchone(cursor)
        conn.commit()
        conn.close()
        print(f"result = {result}")
        if result == {}:
            self.add_new_project_to_db()
        else:
            self.update_project_to_db()

    def get_app_converter(self) -> str:
        """
        Запрос значения app_converter из БД.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT value_setting FROM Settings WHERE name_setting = 'app_converter'"
        )
        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"SettingsDatabase get_app_converter():\nresult = {result}"
        )
        return result.get("value_setting")

    def set_app_converter(self, app_converter: str):
        """
        Установка значения app_converter в БД.
        """
        self.__osbm.obj_logg.debug_logger(
            f"SettingsDatabase set_app_converter(app_converter):\napp_converter = {app_converter}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Settings SET value_setting = ? WHERE name_setting = 'app_converter'",
            (app_converter,),
        )
        conn.commit()
        conn.close()

    def get_last_projects(self) -> list:
        """
        Запрос последних пяти проектов из БД.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Projects ORDER BY date_last_open_project DESC LIMIT 5"
        )
        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"SettingsDatabase get_last_projects():\nresult = {result}"
        )
        return result


    def get_libreoffice_path(self) -> str:
        """
        Запрос значения libreoffice_path из БД.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT value_setting FROM Settings WHERE name_setting = 'libreoffice_path'"
        )
        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"SettingsDatabase get_libreoffice_path():\nresult = {result}"
        )
        return result.get("value_setting")
        
    def get_project_current_name(self):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT value_setting FROM Settings WHERE name_setting = 'project_current_name'"
        )
        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"SettingsDatabase get_project_current_name():\nresult = {result}"
        )
        return result.get("value_setting")
    
    def set_project_current_name(self, project_name):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Settings SET value_setting = ? WHERE name_setting = 'project_current_name'",
            (project_name,),
        )
        self.__osbm.obj_logg.debug_logger(
            f"SettingsDatabase set_project_current_name(project_name):\nproject_name = {project_name}"
        )
        conn.commit()
        conn.close()

    def delete_project_from_db(self, project):
        self.__osbm.obj_logg.debug_logger(
            f"SettingsDatabase delete_project_from_db(project):\nproject = {project}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM Projects WHERE name_project = ? AND directory_project = ?",
            (project.get("name_project"), project.get("directory_project")),
        )
        conn.commit()
        conn.close()

# obj_setdb = SettingsDatabase()
