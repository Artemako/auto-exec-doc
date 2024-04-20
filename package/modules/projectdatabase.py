import sqlite3
import os

import package.modules.dirpathsmanager as dirpathsmanager
import package.modules.log as log


class Database:
    @staticmethod
    def create_and_config_db_project():
        """
        Настройка базы данных перед использованием проекта
        """
        log.Log.debug_logger("IN create_and_config_db_project()")

        if not os.path.exists(dirpathsmanager.DirPathManager.get_db_project_dirpath()):
            # Добавляем данные в пустую БД
            Database.add_tables_and_datas_to_empty_db_project()

    @staticmethod
    def add_tables_and_datas_to_empty_db_project():
        """
        Добавление таблиц и данных в БД программы при запуске.
        """
        log.Log.debug_logger("IN add_tables_and_datas_to_empty_db_project()")
        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        cursor = conn.cursor()
        cursor.executescript(
            """
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Project_pages" (
	"id_page"	INTEGER NOT NULL UNIQUE,
	"id_node_parent"	INTEGER,
	"name_page"	TEXT,
	"folder_page"	TEXT,
	"included"	TEXT DEFAULT 'True',
	PRIMARY KEY("id_page" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Project_content_config_table" (
	"id_config"	INTEGER UNIQUE,
	"id_content"	INTEGER,
	"type_config"	TEXT,
	"value_config"	TEXT,
	"note_config"	TEXT,
	FOREIGN KEY("id_content") REFERENCES "Project_content_config_list"("id_content"),
	PRIMARY KEY("id_config" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Project_content_config_date" (
	"id_config"	INTEGER UNIQUE,
	"id_content"	INTEGER,
	"type_config"	TEXT,
	"value_config"	TEXT,
	"note_config"	TEXT,
	FOREIGN KEY("id_content") REFERENCES "Project_content_config_list"("id_content"),
	PRIMARY KEY("id_config" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Project_content_config_list" (
	"id_content"	INTEGER NOT NULL UNIQUE,
	"name_content"	TEXT NOT NULL UNIQUE,
	"type_content"	TEXT NOT NULL,
	"title_content"	TEXT,
	"description_content"	TEXT,
	"enable"	INTEGER,
	PRIMARY KEY("id_content" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Project_structure_of_nodes" (
	"id_node"	INTEGER NOT NULL UNIQUE,
	"name_node"	TEXT,
	"id_parent"	INTEGER,
	"order_node"	TEXT,
	"type_node"	TEXT,
	"template_name"	TEXT,
	"folder_form"	TEXT,
	"name_json"	TEXT,
	"included"	TEXT DEFAULT 'True',
	PRIMARY KEY("id_node" AUTOINCREMENT)
);
INSERT INTO "Project_pages" VALUES (1,10,'Л.1. Титульный лист.','1-ТЛ-1',NULL);
INSERT INTO "Project_pages" VALUES (2,10,'Л.2. Титульный лист.','1-ТЛ-2',NULL);
INSERT INTO "Project_pages" VALUES (3,11,'Л.1. Реестр исполнительной документации ВОЛС.','2-РД-1',NULL);
INSERT INTO "Project_pages" VALUES (4,1201,'Л.1. Паспорт трассы. Опись документов.','3-ПТ1-1',NULL);
INSERT INTO "Project_pages" VALUES (5,1202,'Л.1. Паспорт трассы волоконно-оптической линии связи на участке.','3-ПТ2-1',NULL);
INSERT INTO "Project_pages" VALUES (6,1203,'Л.1. Скелетная схема ВОЛП и основные данные цепей кабеля.','3-ПТ3-1',NULL);
INSERT INTO "Project_content_config_table" VALUES (100,1200,'HEADER','Форма',NULL);
INSERT INTO "Project_content_config_table" VALUES (101,1200,'HEADER','Наименование',NULL);
INSERT INTO "Project_content_config_table" VALUES (102,1200,'HEADER','Количество листов',NULL);
INSERT INTO "Project_content_config_table" VALUES (103,1200,'HEADER','Номера страниц',NULL);
INSERT INTO "Project_content_config_table" VALUES (104,1200,'HEADER','Примечание',NULL);
INSERT INTO "Project_content_config_table" VALUES (110,1200,'CONTENT','форма',NULL);
INSERT INTO "Project_content_config_table" VALUES (111,1200,'CONTENT','наименование_документа',NULL);
INSERT INTO "Project_content_config_table" VALUES (112,1200,'CONTENT','кол_листов',NULL);
INSERT INTO "Project_content_config_table" VALUES (113,1200,'CONTENT','номера_стр',NULL);
INSERT INTO "Project_content_config_table" VALUES (114,1200,'CONTENT','примечание',NULL);
INSERT INTO "Project_content_config_table" VALUES (200,1201,'HEADER','Форма',NULL);
INSERT INTO "Project_content_config_table" VALUES (201,1201,'HEADER','Наименование',NULL);
INSERT INTO "Project_content_config_table" VALUES (202,1201,'HEADER','Количество листов',NULL);
INSERT INTO "Project_content_config_table" VALUES (203,1201,'HEADER','Номера страниц',NULL);
INSERT INTO "Project_content_config_table" VALUES (204,1201,'HEADER','Примечание',NULL);
INSERT INTO "Project_content_config_table" VALUES (205,1201,'CONTENT','форма',NULL);
INSERT INTO "Project_content_config_table" VALUES (206,1201,'CONTENT','наименование_документа',NULL);
INSERT INTO "Project_content_config_table" VALUES (207,1201,'CONTENT','кол_листов',NULL);
INSERT INTO "Project_content_config_table" VALUES (208,1201,'CONTENT','номера_стр',NULL);
INSERT INTO "Project_content_config_table" VALUES (209,1201,'CONTENT','примечание',NULL);
INSERT INTO "Project_content_config_table" VALUES (300,1202,'HEADER','Форма',NULL);
INSERT INTO "Project_content_config_table" VALUES (301,1202,'HEADER','Наименование',NULL);
INSERT INTO "Project_content_config_table" VALUES (302,1202,'HEADER','Количество листов',NULL);
INSERT INTO "Project_content_config_table" VALUES (303,1202,'HEADER','Номера страниц',NULL);
INSERT INTO "Project_content_config_table" VALUES (304,1202,'HEADER','Примечание',NULL);
INSERT INTO "Project_content_config_table" VALUES (305,1202,'CONTENT','форма',NULL);
INSERT INTO "Project_content_config_table" VALUES (306,1202,'CONTENT','наименование_документа',NULL);
INSERT INTO "Project_content_config_table" VALUES (307,1202,'CONTENT','кол_листов',NULL);
INSERT INTO "Project_content_config_table" VALUES (308,1202,'CONTENT','номера_стр',NULL);
INSERT INTO "Project_content_config_table" VALUES (309,1202,'CONTENT','примечание',NULL);
INSERT INTO "Project_content_config_table" VALUES (400,1209,'HEADER','Номер формы',NULL);
INSERT INTO "Project_content_config_table" VALUES (401,1209,'HEADER','Наименование документа',NULL);
INSERT INTO "Project_content_config_table" VALUES (402,1209,'HEADER','Количество листов',NULL);
INSERT INTO "Project_content_config_table" VALUES (403,1209,'HEADER','Номера страниц',NULL);
INSERT INTO "Project_content_config_table" VALUES (404,1209,'HEADER','Примечания',NULL);
INSERT INTO "Project_content_config_table" VALUES (405,1209,'CONTENT','номер_формы',NULL);
INSERT INTO "Project_content_config_table" VALUES (406,1209,'CONTENT','наименование_документа',NULL);
INSERT INTO "Project_content_config_table" VALUES (407,1209,'CONTENT','кол_листов',NULL);
INSERT INTO "Project_content_config_table" VALUES (408,1209,'CONTENT','номера_стр',NULL);
INSERT INTO "Project_content_config_table" VALUES (409,1209,'CONTENT','примечание',NULL);
INSERT INTO "Project_content_config_table" VALUES (500,1220,'HEADER','Марка кабеля',NULL);
INSERT INTO "Project_content_config_table" VALUES (501,1220,'HEADER','Длина кабеля (всего) в м.',NULL);
INSERT INTO "Project_content_config_table" VALUES (502,1220,'HEADER','Оптическая длина в м.',NULL);
INSERT INTO "Project_content_config_table" VALUES (503,1220,'HEADER','Информация',NULL);
INSERT INTO "Project_content_config_table" VALUES (504,1220,'CONTENT','марка',NULL);
INSERT INTO "Project_content_config_table" VALUES (505,1220,'CONTENT','длина_всего',NULL);
INSERT INTO "Project_content_config_table" VALUES (506,1220,'CONTENT','длина_опт',NULL);
INSERT INTO "Project_content_config_table" VALUES (507,1220,'CONTENT','инфо',NULL);
INSERT INTO "Project_content_config_date" VALUES (100,1208,'FORMAT','yyyy',NULL);
INSERT INTO "Project_content_config_date" VALUES (101,1227,'FORMAT','yyyy',NULL);
INSERT INTO "Project_content_config_date" VALUES (102,1228,'FORMAT','yyyy',NULL);
INSERT INTO "Project_content_config_list" VALUES (1000,'организационно_правовая_форма','TEXT','Организационно-правовая форма',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1001,'название_компании','TEXT','Название компании',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1002,'адрес_компании','TEXT','Адрес компании',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1003,'название_объекта','TEXT','Название объекта',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1004,'участок','TEXT','Участок',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1005,'номер_кабеля','TEXT','Номер кабеля',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1006,'заказчик','TEXT','Заказчик',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1007,'строительно_монтажная_организация','TEXT','Строительно-монтажная организация',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1008,'город','TEXT','Город',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1009,'год','DATE','Год',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1100,'инж_про_ком','TEXT','Компания инженера-проектировщика',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1101,'инж_про_ком_фио','TEXT','ФИО инженера-проектировщика',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1102,'гла_инж_компания','TEXT','Компания главного инженера',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1103,'гла_инж_фио','TEXT','ФИО главного инженера',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1200,'реестр_ид_паспорт_трассы','TABLE','Реестр ИД ВОЛС. Паспорт трассы',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1201,'реестр_ид_эл_паспорт_трассы','TABLE','Реестр ИД ВОЛС. Электрический паспорт трассы',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1202,'рабочая_документация','TABLE','Реестр ИД ВОЛС. Рабочая документация',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1208,'дата','DATE','Дата',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1209,'пт_опись_документов','TABLE','Паспорт трассы. Опись документов.',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1220,'кабеля','TABLE','Кабеля.',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1225,'общая_физ_длина','TEXT','Общая физическая длина',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1226,'общая_опт_длина','TEXT','Общая оптическая длина',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1227,'год_прокладки_кабеля','DATE','Год прокладки кабеля',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1228,'год_составления_паспорта','DATE','Год составления паспорта',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1229,'отв_пред_орг_фио ','TEXT','ФИО ответственного представителя организации',NULL,NULL);
INSERT INTO "Project_content_config_list" VALUES (1230,'скелетная_схема_ВОЛП','IMAGE','Скелетная схема ВОЛП',NULL,NULL);
INSERT INTO "Project_structure_of_nodes" VALUES (0,'Проект',NULL,'0','PROJECT',NULL,NULL,'project',NULL);
INSERT INTO "Project_structure_of_nodes" VALUES (10,'Титульный лист',0,'1','FORM','main','1-ТЛ','1-ТЛ','1');
INSERT INTO "Project_structure_of_nodes" VALUES (11,'Реестр документации',0,'2','FORM','main','2-РД',NULL,'1');
INSERT INTO "Project_structure_of_nodes" VALUES (12,'Паспорт трассы',0,'3','GROUP',NULL,NULL,NULL,'1');
INSERT INTO "Project_structure_of_nodes" VALUES (1201,'ПТ-1',12,'1','FORM','main','3-ПТ1',NULL,'1');
INSERT INTO "Project_structure_of_nodes" VALUES (1202,'ПТ-2',12,'2','FORM','main','3-ПТ2',NULL,'1');
INSERT INTO "Project_structure_of_nodes" VALUES (1203,'ПТ-3',12,'3','FORM','main','3-ПТ3',NULL,'1');
COMMIT;

            """
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_project_node() -> object:
        """
        Запрос на вершину проекта.
        """
        log.Log.debug_logger("IN get_project_node()")

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM Project_structure_of_nodes
        WHERE type_node = "PROJECT";
        """)

        cursor_result = cursor.fetchone()
        result = dict(cursor_result) if cursor_result else {}
        return result

    @staticmethod
    def get_childs(parent_node: object) -> list:
        """
        Запрос на детей вершины.
        """
        log.Log.debug_logger(f"IN get_childs({parent_node}: int) ")

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_structure_of_nodes
        WHERE id_parent = ?
        """,
            [parent_node.get("id_node")],
        )

        cursor_result = cursor.fetchall()
        result = [dict(row) for row in cursor_result] if cursor_result else []
        conn.close()
        return result

    @staticmethod
    def get_pages(node) -> list:
        """
        Запрос на получение всех страниц выбранной формы.
        """
        log.Log.debug_logger(f"get_pages(node) -> list: node = {node}")

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_pages
        WHERE id_node_parent = ?
        """,
            [node.get("id_node")],
        )

        cursor_result = cursor.fetchall()
        result = [dict(row) for row in cursor_result] if cursor_result else []
        conn.close()
        return result

    @staticmethod
    def get_node_parent_from_pages(page) -> object:
        """
        Запрос на получение node_parent из таблицы Project_pages.
        """
        log.Log.debug_logger(
            f"get_node_parent_from_pages(page) -> object: page = {page}"
        )

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_structure_of_nodes
        WHERE id_node = ?
        """,
            [page.get("id_node_parent")],
        )

        cursor_result = cursor.fetchone()
        result = dict(cursor_result) if cursor_result else {}
        conn.close()
        return result
    

    @staticmethod
    def get_node_parent(node) -> object:
        """
        Запрос на получение node_parent из таблицы Project_structure_of_nodes.
        """
        log.Log.debug_logger(f"get_node_parent(node) -> object: node = {node}")

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_structure_of_nodes
        WHERE id_node = ?
        """,
            [node.get("id_parent")],
        )

        cursor_result = cursor.fetchone()
        result = dict(cursor_result) if cursor_result else {}
        conn.close()
        return result

    @staticmethod
    def get_config_content(name_content) -> object:
        """
        Запрос на получение config_content по имени формы.
        """
        log.Log.debug_logger(
            f"get_config_content(name_content) -> list: name_content = {name_content}"
        )

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_content_config_list
        WHERE name_content = ?
        """,
            [name_content],
        )

        cursor_result = cursor.fetchone()
        result = dict(cursor_result) if cursor_result else {}
        conn.close()
        return result

    @staticmethod
    def get_config_date(id_content) -> list:
        """
        Запрос на получение config_date по имени формы.
        """
        log.Log.debug_logger(
            f"get_config_date(id_content) -> list: name_content = {id_content}"
        )

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_content_config_date
        WHERE id_content = ?
        """,
            [id_content],
        )

        cursor_result = cursor.fetchall()
        result = [dict(row) for row in cursor_result] if cursor_result else []
        conn.close()
        return result


    @staticmethod
    def set_included_for_node(node, state):
        """
        Запрос на установку включенности для вершины.
        """
        log.Log.debug_logger(f"set_included_for_node(node, state): node = {node}, state = {state}")

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_structure_of_nodes
        SET included = ?
        WHERE id_node = ?
        """,
            [state, node.get("id_node")],
        )
        conn.commit()
        conn.close()
    