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

        # set всем included = True
        Database.set_all_included_in_db_project_to_true()
        

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
CREATE TABLE IF NOT EXISTS "Project_content_config_date" (
	"id_config"	INTEGER UNIQUE,
	"id_content"	INTEGER,
	"type_config"	TEXT,
	"value_config"	TEXT,
	"note_config"	TEXT,
	PRIMARY KEY("id_config" AUTOINCREMENT),
	FOREIGN KEY("id_content") REFERENCES "Project_content_config_list"("id_content")
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
CREATE TABLE IF NOT EXISTS "Project_nodes_data" (
	"id_pair"	INTEGER UNIQUE,
	"id_node"	INTEGER,
	"id_content"	INTEGER,
	"name_content"	TEXT,
	"value"	TEXT,
	PRIMARY KEY("id_pair" AUTOINCREMENT),
	FOREIGN KEY("id_node") REFERENCES "Project_nodes"("id_node"),
	FOREIGN KEY("id_content") REFERENCES "Project_content_config_list"("id_content")
);
CREATE TABLE IF NOT EXISTS "Project_pages_data" (
	"id_pair"	INTEGER UNIQUE,
	"id_page"	INTEGER,
	"id_content"	INTEGER,
	"name_content"	TEXT,
	"value"	TEXT,
	PRIMARY KEY("id_pair" AUTOINCREMENT),
	FOREIGN KEY("id_content") REFERENCES "Project_content_config_list"("id_content"),
	FOREIGN KEY("id_page") REFERENCES "Project_pages"("id_page")
);
CREATE TABLE IF NOT EXISTS "Project_content_config_table" (
	"id_config"	INTEGER UNIQUE,
	"id_content"	INTEGER,
	"type_config"	TEXT,
	"value_config"	TEXT,
	"note_config"	TEXT,
	"order_config"	INTEGER,
	PRIMARY KEY("id_config" AUTOINCREMENT),
	FOREIGN KEY("id_content") REFERENCES "Project_content_config_list"("id_content")
);
CREATE TABLE IF NOT EXISTS "Project_nodes" (
	"id_node"	INTEGER NOT NULL UNIQUE,
	"name_node"	TEXT,
	"id_parent"	INTEGER,
	"order_node"	TEXT,
	"type_node"	TEXT,
	"template_name"	TEXT,
	"included"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("id_node" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Project_pages" (
	"id_page"	INTEGER NOT NULL UNIQUE,
	"id_node_parent"	INTEGER,
	"page_name"	TEXT,
	"template_name"	TEXT,
	"order_page"	INTEGER,
	"included"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("id_page" AUTOINCREMENT)
);
INSERT INTO "Project_content_config_date" VALUES (100,1208,'FORMAT','yyyy',NULL);
INSERT INTO "Project_content_config_date" VALUES (101,1009,'FORMAT','yyyy',NULL);
INSERT INTO "Project_content_config_date" VALUES (103,1227,'FORMAT','yyyy',NULL);
INSERT INTO "Project_content_config_date" VALUES (104,1228,'FORMAT','yyyy',NULL);
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
INSERT INTO "Project_nodes_data" VALUES (100,0,1003,'название_объекта',NULL);
INSERT INTO "Project_nodes_data" VALUES (101,0,1004,'участок',NULL);
INSERT INTO "Project_nodes_data" VALUES (102,0,1001,'название_компании',NULL);
INSERT INTO "Project_nodes_data" VALUES (1000,10,1000,'организационно_правовая_форма',NULL);
INSERT INTO "Project_nodes_data" VALUES (1001,10,1002,'адрес_компании',NULL);
INSERT INTO "Project_nodes_data" VALUES (1004,10,1005,'номер_кабеля',NULL);
INSERT INTO "Project_nodes_data" VALUES (1005,10,1006,'заказчик',NULL);
INSERT INTO "Project_nodes_data" VALUES (1006,10,1008,'город',NULL);
INSERT INTO "Project_nodes_data" VALUES (1007,10,1009,'год',NULL);
INSERT INTO "Project_nodes_data" VALUES (1100,11,1101,'инж_про_ком_фио',NULL);
INSERT INTO "Project_nodes_data" VALUES (1101,11,1208,'дата',NULL);
INSERT INTO "Project_nodes_data" VALUES (1200,12,1101,'инж_про_ком_фио',NULL);
INSERT INTO "Project_nodes_data" VALUES (1201,12,1208,'дата',NULL);
INSERT INTO "Project_pages_data" VALUES (100,10,1007,'строительно_монтажная_организация',NULL);
INSERT INTO "Project_pages_data" VALUES (200,11,1100,'инж_про_ком',NULL);
INSERT INTO "Project_pages_data" VALUES (201,11,1101,'инж_про_ком_фио',NULL);
INSERT INTO "Project_pages_data" VALUES (202,11,1102,'гла_инж_компания',NULL);
INSERT INTO "Project_pages_data" VALUES (203,11,1103,'гла_инж_фио',NULL);
INSERT INTO "Project_pages_data" VALUES (300,20,1200,'реестр_ид_паспорт_трассы',NULL);
INSERT INTO "Project_pages_data" VALUES (301,20,1201,'реестр_ид_эл_паспорт_трассы',NULL);
INSERT INTO "Project_pages_data" VALUES (302,20,1202,'рабочая_документация',NULL);
INSERT INTO "Project_pages_data" VALUES (400,30,1209,'пт_опись_документов',NULL);
INSERT INTO "Project_pages_data" VALUES (500,40,1220,'кабеля',NULL);
INSERT INTO "Project_pages_data" VALUES (501,40,1225,'общая_физ_длина',NULL);
INSERT INTO "Project_pages_data" VALUES (502,40,1226,'общая_опт_длина',NULL);
INSERT INTO "Project_pages_data" VALUES (503,40,1227,'год_прокладки_кабеля',NULL);
INSERT INTO "Project_pages_data" VALUES (504,40,1228,'год_составления_паспорта',NULL);
INSERT INTO "Project_pages_data" VALUES (505,40,1229,'отв_пред_орг_фио',NULL);
INSERT INTO "Project_pages_data" VALUES (600,50,1230,'скелетная_схема_ВОЛП',NULL);
INSERT INTO "Project_content_config_table" VALUES (100,1200,'HEADER','Форма','',0);
INSERT INTO "Project_content_config_table" VALUES (101,1200,'HEADER','Наименование','',1);
INSERT INTO "Project_content_config_table" VALUES (102,1200,'HEADER','Количество листов','',2);
INSERT INTO "Project_content_config_table" VALUES (103,1200,'HEADER','Номера страниц','',3);
INSERT INTO "Project_content_config_table" VALUES (104,1200,'HEADER','Примечание','',4);
INSERT INTO "Project_content_config_table" VALUES (110,1200,'CONTENT','форма','',0);
INSERT INTO "Project_content_config_table" VALUES (111,1200,'CONTENT','наименование_документа','',1);
INSERT INTO "Project_content_config_table" VALUES (112,1200,'CONTENT','кол_листов','',2);
INSERT INTO "Project_content_config_table" VALUES (113,1200,'CONTENT','номера_стр','',3);
INSERT INTO "Project_content_config_table" VALUES (114,1200,'CONTENT','примечание','',4);
INSERT INTO "Project_content_config_table" VALUES (200,1201,'HEADER','Форма','',0);
INSERT INTO "Project_content_config_table" VALUES (201,1201,'HEADER','Наименование','',1);
INSERT INTO "Project_content_config_table" VALUES (202,1201,'HEADER','Количество листов','',2);
INSERT INTO "Project_content_config_table" VALUES (203,1201,'HEADER','Номера страниц','',3);
INSERT INTO "Project_content_config_table" VALUES (204,1201,'HEADER','Примечание','',4);
INSERT INTO "Project_content_config_table" VALUES (205,1201,'CONTENT','форма','',0);
INSERT INTO "Project_content_config_table" VALUES (206,1201,'CONTENT','наименование_документа','',1);
INSERT INTO "Project_content_config_table" VALUES (207,1201,'CONTENT','кол_листов','',2);
INSERT INTO "Project_content_config_table" VALUES (208,1201,'CONTENT','номера_стр','',3);
INSERT INTO "Project_content_config_table" VALUES (209,1201,'CONTENT','примечание','',4);
INSERT INTO "Project_content_config_table" VALUES (300,1202,'HEADER','Форма','',0);
INSERT INTO "Project_content_config_table" VALUES (301,1202,'HEADER','Наименование','',1);
INSERT INTO "Project_content_config_table" VALUES (302,1202,'HEADER','Количество листов','',2);
INSERT INTO "Project_content_config_table" VALUES (303,1202,'HEADER','Номера страниц','',3);
INSERT INTO "Project_content_config_table" VALUES (304,1202,'HEADER','Примечание','',4);
INSERT INTO "Project_content_config_table" VALUES (305,1202,'CONTENT','форма','',0);
INSERT INTO "Project_content_config_table" VALUES (306,1202,'CONTENT','наименование_документа','',1);
INSERT INTO "Project_content_config_table" VALUES (307,1202,'CONTENT','кол_листов','',2);
INSERT INTO "Project_content_config_table" VALUES (308,1202,'CONTENT','номера_стр','',3);
INSERT INTO "Project_content_config_table" VALUES (309,1202,'CONTENT','примечание','',4);
INSERT INTO "Project_content_config_table" VALUES (400,1209,'HEADER','Номер формы','',0);
INSERT INTO "Project_content_config_table" VALUES (401,1209,'HEADER','Наименование документа','',1);
INSERT INTO "Project_content_config_table" VALUES (402,1209,'HEADER','Количество листов','',2);
INSERT INTO "Project_content_config_table" VALUES (403,1209,'HEADER','Номера страниц','',3);
INSERT INTO "Project_content_config_table" VALUES (404,1209,'HEADER','Примечания','',4);
INSERT INTO "Project_content_config_table" VALUES (405,1209,'CONTENT','номер_формы','',0);
INSERT INTO "Project_content_config_table" VALUES (406,1209,'CONTENT','наименование_документа','',1);
INSERT INTO "Project_content_config_table" VALUES (407,1209,'CONTENT','кол_листов','',2);
INSERT INTO "Project_content_config_table" VALUES (408,1209,'CONTENT','номера_стр','',3);
INSERT INTO "Project_content_config_table" VALUES (409,1209,'CONTENT','примечание','',4);
INSERT INTO "Project_content_config_table" VALUES (500,1220,'HEADER','Марка кабеля','',0);
INSERT INTO "Project_content_config_table" VALUES (501,1220,'HEADER','Длина кабеля (всего) в м.','',1);
INSERT INTO "Project_content_config_table" VALUES (502,1220,'HEADER','Оптическая длина в м.','',2);
INSERT INTO "Project_content_config_table" VALUES (503,1220,'HEADER','Информация','',3);
INSERT INTO "Project_content_config_table" VALUES (504,1220,'CONTENT','марка','',0);
INSERT INTO "Project_content_config_table" VALUES (505,1220,'CONTENT','длина_всего','',1);
INSERT INTO "Project_content_config_table" VALUES (506,1220,'CONTENT','длина_опт','',2);
INSERT INTO "Project_content_config_table" VALUES (507,1220,'CONTENT','инфо','',3);
INSERT INTO "Project_nodes" VALUES (0,'Проект',NULL,'0','PROJECT',NULL,1);
INSERT INTO "Project_nodes" VALUES (10,'Титульный лист',0,'1','FORM','main',1);
INSERT INTO "Project_nodes" VALUES (11,'Реестр документации',0,'2','FORM','main',1);
INSERT INTO "Project_nodes" VALUES (12,'Паспорт трассы',0,'3','GROUP',NULL,1);
INSERT INTO "Project_nodes" VALUES (1201,'ПТ-1',12,'1','FORM','main',1);
INSERT INTO "Project_nodes" VALUES (1202,'ПТ-2',12,'2','FORM','main',1);
INSERT INTO "Project_nodes" VALUES (1203,'ПТ-3',12,'3','FORM','main',1);
INSERT INTO "Project_pages" VALUES (10,10,'Л.1. Титульный лист.','1-ТЛ-1',0,1);
INSERT INTO "Project_pages" VALUES (11,10,'Л.2. Титульный лист.','1-ТЛ-2',1,1);
INSERT INTO "Project_pages" VALUES (20,11,'Л.1. Реестр исполнительной документации ВОЛС.','2-РД-1',0,1);
INSERT INTO "Project_pages" VALUES (30,1201,'Л.1. Паспорт трассы. Опись документов.','3-ПТ1-1',0,1);
INSERT INTO "Project_pages" VALUES (40,1202,'Л.1. Паспорт трассы волоконно-оптической линии связи на участке.','3-ПТ2-1',0,1);
INSERT INTO "Project_pages" VALUES (50,1203,'Л.1. Скелетная схема ВОЛП и основные данные цепей кабеля.','3-ПТ3-1',0,1);
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
        log.Log.debug_logger("IN get_project_node() -> object")

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM Project_nodes
        WHERE type_node = "PROJECT";
        """)

        cursor_result = cursor.fetchone()
        result = dict(cursor_result) if cursor_result else {}
        return result

    @staticmethod
    def get_childs(parent_node) -> list:
        """
        Запрос на детей вершины.
        """
        log.Log.debug_logger(f"IN get_childs(parent_node) -> list: parent_node = {parent_node}")

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_nodes
        WHERE id_parent = ?
        ORDER BY order_node ASC
        """,
            [parent_node.get("id_node")],
        )

        cursor_result = cursor.fetchall()
        result = [dict(row) for row in cursor_result] if cursor_result else []
        conn.close()
        return result

    @staticmethod
    def get_pages_by_node(node) -> list:
        """
        Запрос на получение всех страниц выбранной формы.
        """
        log.Log.debug_logger(f"IN get_pages_by_node(node) -> list: node = {node}")

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_pages
        WHERE id_node_parent = ?
        ORDER BY order_page ASC
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
            f"IN get_node_parent_from_pages(page) -> object: page = {page}"
        )

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_nodes
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
        Запрос на получение node_parent из таблицы Project_nodes.
        """
        log.Log.debug_logger(f"IN get_node_parent(node) -> object: node = {node}")

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_nodes
        WHERE id_node = ?
        """,
            [node.get("id_parent")],
        )

        cursor_result = cursor.fetchone()
        result = dict(cursor_result) if cursor_result else {}
        conn.close()
        return result
    

    def get_node_by_id(id_node) -> object:
        """
        Запрос на получение node по id.
        """
        log.Log.debug_logger(f"IN get_node_by_id(id_node) -> object: id_node = {id_node}")

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_nodes
        WHERE id_node = ?
        """,
            [id_node],
        )

        cursor_result = cursor.fetchone()
        result = dict(cursor_result) if cursor_result else {}
        conn.close()
        return result


    @staticmethod
    def get_config_content_by_id(id_content) -> object:
        """
        Запрос на получение config_content по имени формы.
        """
        log.Log.debug_logger(
            f"IN get_config_content(id_content) -> list: id_content = {id_content}"
        )

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_content_config_list
        WHERE id_content = ?
        """,
            [id_content],
        )

        cursor_result = cursor.fetchone()
        result = dict(cursor_result) if cursor_result else {}
        conn.close()
        return result

    @staticmethod
    def get_config_date_by_id(id_content) -> list:
        """
        Запрос на получение config_date по имени формы.
        """
        log.Log.debug_logger(
            f"IN get_config_date(id_content) -> list: name_content = {id_content}"
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
    def get_config_table_by_id(id_content) -> list:
        """
        Запрос на получение config_table по имени формы.
        """
        log.Log.debug_logger(f"IN get_config_table(id_content) -> list: id_content = {id_content}")

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_content_config_table
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
        log.Log.debug_logger(f"IN set_included_for_node(node, state): node = {node}, state = {state}")

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_nodes
        SET included = ?
        WHERE id_node = ?
        """,
            [state, node.get("id_node")],
        )
        conn.commit()
        conn.close()

        # print(Database.get_node_by_id(node.get("id_node")))
    

    @staticmethod
    def get_page_data(page) -> list:
        """
        Запрос на получение данных страницы из Project_pages_data.
        """
        log.Log.debug_logger(f"IN get_page_data(page) -> list: page = {page}")

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_pages_data
        WHERE id_page = ?
        """,
            [page.get("id_page")],
        )

        cursor_result = cursor.fetchall()
        result = [dict(row) for row in cursor_result] if cursor_result else []
        conn.close()
        return result
    
    
    @staticmethod
    def get_node_data(node) -> list:
        """
        Запрос на получение данных вершины из Project_nodes_data.
        """
        log.Log.debug_logger(f"IN get_node_data(node) -> list: node = {node}")

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_nodes_data
        WHERE id_node = ?
        """,
            [node.get("id_node")],
        )

        cursor_result = cursor.fetchall()
        result = [dict(row) for row in cursor_result] if cursor_result else []
        conn.close()
        return result
    

    @staticmethod
    def update_pages_data(id_pair, value):
        """
        Запрос на обновление данных страницы в Project_pages_data.
        """
        log.Log.debug_logger(f"IN update_pages_data(id_pair, value): id_pair = {id_pair}, value = {value}")

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_pages_data
        SET value = ?
        WHERE id_pair = ?
        """,
            [value, id_pair],
        )
        conn.commit()
        conn.close()
    

    @staticmethod
    def update_nodes_data(id_pair, value):
        """
        Запрос на обновление данных вершины в Project_nodes_data.
        """
        log.Log.debug_logger(f"IN update_nodes_data(id_pair, value): id_pair = {id_pair}, value = {value}")

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_nodes_data
        SET value = ?
        WHERE id_pair = ?
        """,
            [value, id_pair],
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_page_pair_value_by_id(id_pair):
        """
        Запрос на получение значения по id_pair в Project_pages_data.
        """
        log.Log.debug_logger(f"IN get_page_pair_value_by_id(id_pair): id_pair = {id_pair}")

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT value FROM Project_pages_data
        WHERE id_pair = ?
        """,
            [id_pair],
        )

        cursor_result = cursor.fetchone()
        result = cursor_result[0] if cursor_result else None
        conn.close()
        return result
    

    @staticmethod
    def get_node_pair_value_by_id(id_pair):
        """
        Запрос на получение значения по id_pair в Project_nodes_data.
        """
        log.Log.debug_logger(f"IN get_node_pair_value_by_id(id_pair): id_pair = {id_pair}")

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT value FROM Project_nodes_data
        WHERE id_pair = ?
        """,
            [id_pair],
        )

        cursor_result = cursor.fetchone()
        result = cursor_result[0] if cursor_result else None
        conn.close()
        return result
    
    @staticmethod
    def set_all_included_in_db_project_to_true():
        """
        Установка всех included = True
        """
        log.Log.debug_logger("IN set_all_included_in_db_project_to_true()")

        conn = sqlite3.connect(dirpathsmanager.DirPathManager.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.executescript(
            """
        UPDATE Project_pages
        SET included = 1;

        UPDATE Project_nodes
        SET included = 1;
        """
        )
        conn.commit()
        conn.close()