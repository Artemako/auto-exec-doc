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
        CREATE TABLE IF NOT EXISTS "Project_content_config_table" (
            "id_config"	INTEGER NOT NULL UNIQUE,
            "id_content"	INTEGER NOT NULL,
            "type_config"	TEXT NOT NULL,
            "value_config"	TEXT NOT NULL,
            "note_config"	TEXT,
            PRIMARY KEY("id_config" AUTOINCREMENT),
            FOREIGN KEY("id_content") REFERENCES "Project_content_config_list"("id_content")
        );
        CREATE TABLE IF NOT EXISTS "Project_structure_of_nodes" (
            "id_node"	INTEGER NOT NULL UNIQUE,
            "name_node"	TEXT,
            "id_parent"	INTEGER,
            "order_node"	INTEGER,
            "type_node"	TEXT NOT NULL,
            "template_name"	TEXT,
            "folder_form"	TEXT,
            PRIMARY KEY("id_node" AUTOINCREMENT)
        );
        CREATE TABLE IF NOT EXISTS "Project_pages" (
            "id_page"	INTEGER NOT NULL UNIQUE,
            "id_node_parent"	INTEGER,
            "name_page"	TEXT,
            "folder_page"	TEXT,
            PRIMARY KEY("id_page" AUTOINCREMENT)
        );
        CREATE TABLE IF NOT EXISTS "Project_content_config_list" (
            "id_content"	INTEGER NOT NULL UNIQUE,
            "name_content"	TEXT NOT NULL UNIQUE,
            "type_content"	TEXT NOT NULL,
            "note_content"	TEXT,
            "title_content"	TEXT,
            "description_content"	TEXT,
            PRIMARY KEY("id_content" AUTOINCREMENT)
        );
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
        INSERT INTO "Project_content_config_table" VALUES (405,1209,'CONTENT','номер_формы ',NULL);
        INSERT INTO "Project_content_config_table" VALUES (406,1209,'CONTENT','наименование_документа',NULL);
        INSERT INTO "Project_content_config_table" VALUES (407,1209,'CONTENT','кол_листов ',NULL);
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
        INSERT INTO "Project_structure_of_nodes" VALUES (0,'Проект',NULL,0,'PROJECT',NULL,NULL);
        INSERT INTO "Project_structure_of_nodes" VALUES (10,'Титульный лист',0,1,'FORM','main','1-ТЛ');
        INSERT INTO "Project_structure_of_nodes" VALUES (11,'Реестр документации',0,2,'FORM','main','2-РД');
        INSERT INTO "Project_structure_of_nodes" VALUES (12,'Паспорт трассы',0,3,'GROUP',NULL,NULL);
        INSERT INTO "Project_structure_of_nodes" VALUES (1201,'ПТ-1',12,1,'FORM','main','3-ПТ1');
        INSERT INTO "Project_structure_of_nodes" VALUES (1202,'ПТ-2',12,2,'FORM','main','3-ПТ2');
        INSERT INTO "Project_structure_of_nodes" VALUES (1203,'ПТ-3',12,3,'FORM','main','3-ПТ3');
        INSERT INTO "Project_pages" VALUES (1,10,'Лист 1','1-ТЛ-1');
        INSERT INTO "Project_pages" VALUES (2,10,'Лист 2','1-ТЛ-2');
        INSERT INTO "Project_pages" VALUES (3,11,'Лист 3','2-РД-1');
        INSERT INTO "Project_pages" VALUES (4,1201,'Лист 1','3-ПТ1-1');
        INSERT INTO "Project_pages" VALUES (5,1202,'Лист 1','3-ПТ2-1');
        INSERT INTO "Project_pages" VALUES (6,1203,'Лист 1','3-ПТ3-1');
        INSERT INTO "Project_content_config_list" VALUES (1000,'организационно_правовая_форма','TEXT',NULL,'Организационно-правовая форма',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1001,'название_компании','TEXT',NULL,'Название компании',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1002,'адрес_компании','TEXT',NULL,'Адрес компании',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1003,'название_объекта','TEXT',NULL,'Название объекта',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1004,'участок','TEXT',NULL,'Участок',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1005,'номер_кабеля','TEXT',NULL,'Номер кабеля',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1006,'заказчик','TEXT',NULL,'Заказчик',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1007,'строительно_монтажная_организация','TEXT',NULL,'Строительно-монтажная организация',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1008,'город','TEXT',NULL,'Город',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1009,'год','DATE','YEAR','Год',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1100,'инж_про_ком','TEXT',NULL,'Компания инженера-проектировщика',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1101,'инж_про_ком_фио','TEXT',NULL,'ФИО инженера-проектировщика',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1102,'гла_инж_компания','TEXT',NULL,'Компания главного инженера',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1103,'гла_инж_фио','TEXT',NULL,'ФИО главного инженера',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1200,'реестр_ид_паспорт_трассы','TABLE',NULL,'Реестр ИД ВОЛС. Паспорт трассы',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1201,'реестр_ид_эл_паспорт_трассы','TABLE',NULL,'Реестр ИД ВОЛС. Электрический паспорт трассы',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1202,'рабочая_документация','TABLE',NULL,'Реестр ИД ВОЛС. Рабочая документация',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1208,'дата','DATE',NULL,'Дата',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1209,'пт_опись_документов','TABLE',NULL,'Паспорт трассы. Опись документов.',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1220,'кабеля','TABLE',NULL,'Кабеля.',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1225,'общая_физ_длина','TEXT',NULL,'Общая физическая длина',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1226,'общая_опт_длина','TEXT',NULL,'Общая оптическая длина',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1227,'год_прокладки_кабеля','TEXT',NULL,'Год прокладки кабеля',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1228,'год_составления_паспорта','TEXT',NULL,'Год составления паспорта',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1229,'отв_пред_орг_фио ','TEXT',NULL,'ФИО ответственного представителя организации',NULL);
        INSERT INTO "Project_content_config_list" VALUES (1230,'скелетная_схема_ВОЛП','IMAGE',NULL,'Скелетная схема ВОЛП',NULL);
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

        result = dict(cursor.fetchone())
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

        result = [dict(row) for row in cursor.fetchall()]
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

        result = [dict(row) for row in cursor.fetchall()]
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

        result = dict(cursor.fetchone())
        conn.close()
        return result

    @staticmethod
    def get_content_config(name_content) -> list:
        """
        Запрос на получение contenr_config по имени формы.
        """
        log.Log.debug_logger(
            f"get_content_config(name_content) -> list: name_content = {name_content}"
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

        result = dict(cursor.fetchone())
        conn.close()
        return result
