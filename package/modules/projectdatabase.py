import sqlite3
import os


class ProjectDatabaseObjectsManager:
    def __init__(self, osbm):
        self.obj_logg = osbm.obj_logg
        self.obj_dirm = osbm.obj_dirm


class ProjectDatabase:
    def __init__(self):
        pass

    def setting_osbm(self, osbm):
        self.__osbm = ProjectDatabaseObjectsManager(osbm)
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase setting_osbm():\nself.__osbm = {self.__osbm}"
        )

    def create_and_config_db_project(self):
        """
        Настройка базы данных перед использованием проекта
        """
        self.__osbm.obj_logg.debug_logger(
            "ProjectDatabase create_and_config_db_project()"
        )

        if not os.path.exists(self.__osbm.obj_dirm.get_db_project_dirpath()):
            # Добавляем данные в пустую БД
            self.add_tables_and_datas_to_empty_db_project()

        # set всем included = True
        self.set_all_included_in_db_project_to_true()

    def add_tables_and_datas_to_empty_db_project(self):
        """
        Добавление таблиц и данных в БД программы при запуске.
        """
        self.__osbm.obj_logg.debug_logger(
            "ProjectDatabase add_tables_and_datas_to_empty_db_project()"
        )
        conn = sqlite3.connect(self.__osbm.obj_dirm.get_db_project_dirpath())
        cursor = conn.cursor()
        cursor.executescript(
            """
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Project_nodes" (
	"id_node"	INTEGER NOT NULL UNIQUE,
	"name_node"	TEXT UNIQUE,
	"id_parent"	INTEGER,
	"order_node"	TEXT NOT NULL,
	"type_node"	TEXT,
	"id_active_template"	INTEGER,
	"included"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("id_node" AUTOINCREMENT),
	UNIQUE("name_node"),
	FOREIGN KEY("id_active_template") REFERENCES "Project_templates"("id_template") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Project_nodes_data" (
	"id_pair"	INTEGER NOT NULL UNIQUE,
	"id_node"	INTEGER NOT NULL,
	"id_variable"	INTEGER NOT NULL,
	"name_variable"	TEXT,
	"value_pair"	TEXT,
	PRIMARY KEY("id_pair" AUTOINCREMENT),
	FOREIGN KEY("id_node") REFERENCES "Project_nodes"("id_node") ON DELETE CASCADE,
	FOREIGN KEY("id_variable") REFERENCES "Project_variables"("id_variable") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Project_pages" (
	"id_page"	INTEGER NOT NULL UNIQUE,
	"id_parent_template"	INTEGER,
	"name_page"	TEXT UNIQUE,
	"filename_page"	TEXT UNIQUE,
	"order_page"	INTEGER NOT NULL,
	"included"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("id_page" AUTOINCREMENT),
	FOREIGN KEY("id_parent_template") REFERENCES "Project_templates"("id_template") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Project_pages_data" (
	"id_pair"	INTEGER NOT NULL UNIQUE,
	"id_page"	INTEGER NOT NULL,
	"id_variable"	INTEGER NOT NULL,
	"name_variable"	TEXT,
	"value_pair"	TEXT,
	PRIMARY KEY("id_pair" AUTOINCREMENT),
	FOREIGN KEY("id_page") REFERENCES "Project_pages"("id_page") ON DELETE CASCADE,
	FOREIGN KEY("id_variable") REFERENCES "Project_variables"("id_variable") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Project_variables" (
	"id_variable"	INTEGER NOT NULL UNIQUE,
	"name_variable"	TEXT NOT NULL UNIQUE,
	"type_variable"	TEXT NOT NULL,
	"title_variable"	TEXT,
	"order_variable"	INTEGER NOT NULL,
	"config_variable"	TEXT,
	"description_variable"	TEXT,
	"is_global"	INTEGER,
	PRIMARY KEY("id_variable" AUTOINCREMENT),
	UNIQUE("name_variable")
);
CREATE TABLE IF NOT EXISTS "Project_templates" (
	"id_template"	INTEGER NOT NULL UNIQUE,
	"name_template"	TEXT,
	"id_parent_node"	INTEGER,
	PRIMARY KEY("id_template" AUTOINCREMENT),
	FOREIGN KEY("id_parent_node") REFERENCES "Project_nodes"("id_node") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Project_templates_data" (
	"id_pair"	INTEGER NOT NULL UNIQUE,
	"id_template"	INTEGER NOT NULL,
	"id_variable"	INTEGER NOT NULL,
	"name_variable"	TEXT,
	"value_pair"	TEXT,
	PRIMARY KEY("id_pair" AUTOINCREMENT),
	FOREIGN KEY("id_variable") REFERENCES "Project_variables"("id_variable") ON DELETE CASCADE,
	FOREIGN KEY("id_template") REFERENCES "Project_templates"("id_template") ON DELETE CASCADE
);
INSERT INTO "Project_nodes" VALUES (0,'Проект',NULL,'0','PROJECT',NULL,1);
INSERT INTO "Project_nodes" VALUES (10,'Титульный лист',0,'1','FORM',1,1);
INSERT INTO "Project_nodes" VALUES (11,'Реестр документации',0,'2','FORM',2,1);
INSERT INTO "Project_nodes" VALUES (12,'Паспорт трассы',0,'3','GROUP',NULL,1);
INSERT INTO "Project_nodes" VALUES (1201,'ПТ-1',12,'1','FORM',3,1);
INSERT INTO "Project_nodes" VALUES (1202,'ПТ-2',12,'2','FORM',4,1);
INSERT INTO "Project_nodes" VALUES (1203,'ПТ-3',12,'3','FORM',5,1);
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
INSERT INTO "Project_pages" VALUES (10,1,'Л.1. Титульный лист.','10',0,1);
INSERT INTO "Project_pages" VALUES (11,1,'Л.2. Титульный лист.','11',1,1);
INSERT INTO "Project_pages" VALUES (20,2,'Л.1. Реестр исполнительной документации ВОЛС.','20',0,1);
INSERT INTO "Project_pages" VALUES (30,3,'Л.1. Паспорт трассы. Опись документов.','30',0,1);
INSERT INTO "Project_pages" VALUES (40,4,'Л.1. Паспорт трассы волоконно-оптической линии связи на участке.','40',0,1);
INSERT INTO "Project_pages" VALUES (50,5,'Л.1. Скелетная схема ВОЛП и основные данные цепей кабеля.','50',0,1);
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
INSERT INTO "Project_variables" VALUES (1000,'организационно_правовая_форма','TEXT','Организационно-правовая форма',0,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1001,'название_компании','TEXT','Название компании',1,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1002,'адрес_компании','TEXT','Адрес компании',2,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1003,'название_объекта','TEXT','Название объекта',3,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1004,'участок','TEXT','Участок',4,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1005,'номер_кабеля','TEXT','Номер кабеля',5,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1006,'заказчик','TEXT','Заказчик',6,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1007,'строительно_монтажная_организация','TEXT','Строительно-монтажная организация',7,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1008,'город','TEXT','Город',8,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1009,'год','DATE','Год',9,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1100,'инж_про_ком','TEXT','Компания инженера-проектировщика',10,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1101,'инж_про_ком_фио','TEXT','ФИО инженера-проектировщика',11,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1102,'гла_инж_компания','TEXT','Компания главного инженера',12,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1103,'гла_инж_фио','TEXT','ФИО главного инженера',13,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1200,'реестр_ид_паспорт_трассы','TABLE','Реестр ИД ВОЛС. Паспорт трассы',14,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1201,'реестр_ид_эл_паспорт_трассы','TABLE','Реестр ИД ВОЛС. Электрический паспорт трассы',15,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1202,'рабочая_документация','TABLE','Реестр ИД ВОЛС. Рабочая документация',16,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1208,'дата','DATE','Дата',17,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1209,'пт_опись_документов','TABLE','Паспорт трассы. Опись документов.',18,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1220,'кабеля','TABLE','Кабеля.',19,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1225,'общая_физ_длина','TEXT','Общая физическая длина',20,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1226,'общая_опт_длина','TEXT','Общая оптическая длина',21,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1227,'год_прокладки_кабеля','DATE','Год прокладки кабеля',22,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1228,'год_составления_паспорта','DATE','Год составления паспорта',23,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1229,'отв_пред_орг_фио ','TEXT','ФИО ответственного представителя организации',24,NULL,NULL,0);
INSERT INTO "Project_variables" VALUES (1230,'скелетная_схема_ВОЛП','IMAGE','Скелетная схема ВОЛП',25,NULL,NULL,0);
INSERT INTO "Project_templates" VALUES (1,'main',10);
INSERT INTO "Project_templates" VALUES (2,'main',11);
INSERT INTO "Project_templates" VALUES (3,'main',1201);
INSERT INTO "Project_templates" VALUES (4,'main',1202);
INSERT INTO "Project_templates" VALUES (5,'main',1203);
COMMIT;

        """
        )
        conn.commit()
        conn.close()

    def get_conn(self) -> object:
        """
        Запрос курсора.
        """
        self.__osbm.obj_logg.debug_logger("ProjectDatabase get_conn() -> object")
        conn = sqlite3.connect(self.__osbm.obj_dirm.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row
        return conn

    def get_fetchall(self, cursor):
        self.__osbm.obj_logg.debug_logger(
            "ProjectDatabase get_fetchall(cursor, conn) -> list"
        )
        cursor_result = cursor.fetchall()
        result = [dict(row) for row in cursor_result] if cursor_result else []
        return result

    def get_fetchone(self, cursor):
        self.__osbm.obj_logg.debug_logger(
            "ProjectDatabase get_fetchone(cursor, conn) -> list"
        )
        cursor_result = cursor.fetchone()
        result = dict(cursor_result) if cursor_result else {}
        return result

    def get_nodes(self) -> list:
        """
        Запрос на все вершины.
        """
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM Project_nodes;
        """)

        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_nodes() -> list:\nresult = {result}"
        )
        return result

    def get_project_node(self) -> object:
        """
        Запрос на вершину проекта.
        """
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM Project_nodes
        WHERE type_node = "PROJECT";
        """)

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_project_node() -> object:\nresult = {result}"
        )
        return result

    def get_group_nodes(self) -> list:
        """
        Получение вершин групп.
        """
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM Project_nodes
        WHERE type_node = "GROUP";
        """)

        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_group_nodes() -> list:\nresult = {result}"
        )
        return result

    def get_form_nodes(self) -> list:
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM Project_nodes
        WHERE type_node = "FORM";
        """)

        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_form_nodes() -> list:\nresult = {result}"
        )
        return result

    def get_childs(self, parent_node) -> list:
        """
        Запрос на детей вершины.
        """
        conn = self.get_conn()
        cursor = conn.cursor()

        cursor.execute(
            """
        SELECT * FROM Project_nodes
        WHERE id_parent = ?
        ORDER BY order_node ASC
        """,
            [parent_node.get("id_node")],
        )

        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_childs(parent_node) -> list: parent_node = {parent_node}\nresult = {result}"
        )
        return result

    def get_template_by_id(self, id_template) -> object:
        """
        Запрос на получение template из таблицы Project_templates.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_templates
        WHERE id_template = ?
        """,
            [id_template],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_template_by_id(id_template) -> object: id_template = {id_template}\nresult = {result}"
        )
        return result

    def get_templates_by_form(self, form) -> list:
        """
        Получение templates определенной form.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_templates
        WHERE id_parent_node = ?
        """,
            [form.get("id_node")],
        )

        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_templates_by_form(form) -> list: form = {form}\nresult = {result}"
        )
        return result

    def get_pages_by_template(self, template) -> list:
        """
        Запрос на получение pages из таблицы Project_pages.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_pages
        WHERE id_parent_template = ?
        ORDER BY order_page
        """,
            [template.get("id_template")],
        )

        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_pages_by_template(template) -> list: template = {template}\nresult = {result}"
        )
        return result

    def insert_page(self, page) -> int:
        """
        Добавление page в таблицу Project_pages.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase insert_page(page) -> int: page = {page}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        INSERT INTO Project_pages
        (id_parent_template, name_page, filename_page, order_page, included)
        VALUES (?, ?, ?, ?, ?)
        """,
            [
                page.get("id_parent_template"),
                page.get("name_page"),
                page.get("filename_page"),
                page.get("order_page"),
                page.get("included"),
            ],
        )
        conn.commit()
        primary_key = cursor.lastrowid
        conn.close()
        return primary_key

    def get_parent_template(self, page) -> object:
        """
        Определение родителя parent_template для page.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_templates
        WHERE id_template = ?
        """,
            [page.get("id_parent_template")],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_parent_template() -> object\nresult = {result}"
        )
        return result

    def get_parent_node_template(self, template) -> object:
        """
        Определение родителя parent_node для template.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_nodes
        WHERE id_node = ?
        """,
            [template.get("id_parent_node")],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_parent_node_template() -> object\nresult = {result}"
        )
        return result

    def get_node_parent(self, node) -> object:
        """
        Запрос на получение node_parent из таблицы Project_nodes.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_nodes
        WHERE id_node = ?
        """,
            [node.get("id_parent")],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_node_parent(node) -> object: node = {node}\nresult = {result}"
        )
        return result

    def get_node_by_id(self, id_node) -> object:
        """
        Запрос на получение node по id.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_nodes
        WHERE id_node = ?
        """,
            [id_node],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_node_by_id(id_node) -> object: id_node = {id_node}\nresult = {result}"
        )
        return result

    def get_variable_by_id(self, id_variable) -> object:
        """
        Запрос на получение variable по id.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_variables
        WHERE id_variable = ?
        """,
            [id_variable],
        )
        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_config_variable(id_variable) -> list: id_variable = {id_variable}\nresult = {result}"
        )
        return result

    def get_page_by_id(self, id_page) -> object:
        """
        Запрос на получение page по id.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_pages
        WHERE id_page = ?
        """,
            [id_page],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_page_by_id(id_page) -> object: id_page = {id_page}\nresult = {result}"
        )
        return result

    def set_included_for_node(self, node, state):
        """
        Запрос на установку включенности для вершины.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase set_included_for_node(node, state): node = {node}, state = {state}"
        )

        conn = self.get_conn()
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

    def delete_page(self, page):
        """
        Запрос на удаление страницы из Project_pages.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase delete_page(page): page = {page}"
        )

        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(
            """
        DELETE FROM Project_pages
        WHERE id_page = ?
        """,
            [page.get("id_page")],
        )
        conn.commit()
        conn.close()

    def get_page_data(self, page) -> list:
        """
        Запрос на получение данных страницы из Project_pages_data.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_pages_data
        WHERE id_page = ?
        """,
            [page.get("id_page")],
        )
        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_page_data(page) -> list: page = {page}\nresult = {result}"
        )
        return result

    def get_templates(self) -> list:
        """
        Запрос на получение шаблонов из Project_templates.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_templates
        """
        )
        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_templates() -> list:\nresult = {result}"
        )
        return result

    def get_template_data(self, template) -> list:
        """
        Запрос на получение данных шаблона из Project_templates_data.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_templates_data
        WHERE id_template = ?
        """,
            [template.get("id_template")],
        )

        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_template_data(template) -> list: template = {template}\nresult = {result}"
        )
        return result

    def get_node_data(self, node) -> object:
        """
        Запрос на получение данных вершины из Project_nodes_data.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_nodes_data
        WHERE id_node = ?
        """,
            [node.get("id_node")],
        )

        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_node_data(node) -> list: node = {node}\nresult = {result}"
        )
        return result

    def update_page(self, page):
        """
        Запрос на обновление страницы в Project_pages.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase update_page(page): page = {page}"
        )

        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_pages
        SET name_page = ?, filename_page = ?
        WHERE id_page = ?
        """,
            [page.get("name_page"), page.get("filename_page"), page.get("id_page")],
        )
        conn.commit()
        conn.close()

    def update_page_data(self, id_pair, value_pair):
        """
        Запрос на обновление данных страницы в Project_pages_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase update_page_data(id_pair, value_pair): id_pair = {id_pair}, value_pair = {value_pair}"
        )

        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_pages_data
        SET value_pair = ?
        WHERE id_pair = ?
        """,
            [value_pair, id_pair],
        )
        conn.commit()
        conn.close()

    def update_template_data(self, id_pair, value_pair):
        """
        Запрос на обновление данных шаблона в Project_templates_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase update_template_data(id_pair, value_pair): id_pair = {id_pair}, value_pair = {value_pair}"
        )

        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_templates_data
        SET value_pair = ?
        WHERE id_pair = ?
        """,
            [value_pair, id_pair],
        )
        conn.commit()
        conn.close()

    def update_node_data(self, id_pair, value_pair):
        """
        Запрос на обновление данных вершины в Project_nodes_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase update_node_data(id_pair, value_pair): id_pair = {id_pair}, value_pair = {value_pair}"
        )

        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_nodes_data
        SET value_pair = ?
        WHERE id_pair = ?
        """,
            [value_pair, id_pair],
        )
        conn.commit()
        conn.close()

    def get_page_value_pair_by_id_pair(self, id_pair):
        """
        Запрос на получение значения по id_pair в Project_pages_data.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT value_pair FROM Project_pages_data
        WHERE id_pair = ?
        """,
            [id_pair],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_page_value_pair_by_id_pair(id_pair): id_pair = {id_pair}\nresult = {result}"
        )
        return result

    def get_template_value_pair_by_id_pair(self, id_pair):
        """
        Запрос на получение значения по id_pair в Project_templates_data.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT value_pair FROM Project_templates_data
        WHERE id_pair = ?
        """,
            [id_pair],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_template_value_pair_by_id_pair(id_pair): id_pair = {id_pair}\nresult = {result}"
        )
        return result

    def get_node_value_pair_by_id_pair(self, id_pair):
        """
        Запрос на получение значения по id_pair в Project_nodes_data.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT value_pair FROM Project_nodes_data
        WHERE id_pair = ?
        """,
            [id_pair],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_node_value_pair_by_id_pair(id_pair): id_pair = {id_pair}\nresult = {result}"
        )
        return result

    def set_all_included_in_db_project_to_true(self):
        """
        Установка всех included = True
        """
        self.__osbm.obj_logg.debug_logger(
            "ProjectDatabase set_all_included_in_db_project_to_true()"
        )
        conn = self.get_conn()
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

    def get_variables(self) -> list:
        """
        Запрос на получение переменных проекта.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_variables
        ORDER BY order_variable
        """
        )
        result = self.get_fetchall(cursor)
        conn.close()
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_variables() -> list\nresult = {result}"
        )
        return result

    def insert_node_datas(self, node, pair_list):
        """
        Запрос на обновление данных вершины в Project_nodes_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase insert_node_datas(node, pair_list):\nnode = {node}\npair_list = {pair_list}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        for pair in pair_list:
            cursor.execute(
                """
            INSERT INTO Project_nodes_data
            (id_node, id_variable)
            VALUES
            (?, ?)
            """,
                [node.get("id_node"), pair.get("id_variable")],
            )
        conn.commit()
        conn.close()

    def insert_template_data(self, template, pair):
        """
        Запрос на вставку одной строки данных вершины в Project_templates_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase insert_template_data(template, pair):\ntemplate = {template}\npair = {pair}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        INSERT INTO Project_templates_data
        (id_template, id_variable)
        VALUES
        (?, ?)
        """,
            [template.get("id_template"), pair.get("id_variable")],
        )
        conn.commit()
        conn.close()

    def insert_template_datas(self, template, pair_list):
        """
        Запрос на обновление данных вершины в Project_nodes_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase insert_template_datas(template, pair_list):\ntemplate = {template}\npair_list = {pair_list}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        for pair in pair_list:
            cursor.execute(
                """
            INSERT INTO Project_templates_data
            (id_template, id_variable)
            VALUES
            (?, ?)
            """,
                [template.get("id_template"), pair.get("id_variable")],
            )
        conn.commit()
        conn.close()

    def insert_page_data(self, page, pair):
        """
        Запрос на вставку одной строки данных вершины в Project_pages_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase insert_page_data(page, pair):\npage = {page}\npair = {pair}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        INSERT INTO Project_pages_data
        (id_page, id_variable)
        VALUES
        (?, ?)
        """,
            [page.get("id_page"), pair.get("id_variable")],
        )
        conn.commit()
        conn.close()

    def insert_page_datas(self, page, pair_list):
        """
        Запрос на обновление данных страницы в Project_pages_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase insert_page_datas(page, pair_list):\npage = {page}\npair_list = {pair_list}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        for pair in pair_list:
            cursor.execute(
                """
            INSERT INTO Project_pages_data
            (id_page, id_variable)
            VALUES
            (?, ?)
            """,
                [page.get("id_page"), pair.get("id_variable")],
            )
        conn.commit()
        conn.close()

    def delete_node_datas(self, node, pair_list):
        """
        Запрос на удаление данных вершины в Project_nodes_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase delete_node_datas(node, pair_list):\nnode = {node}\npair_list = {pair_list}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        for pair in pair_list:
            cursor.execute(
                """
            DELETE FROM Project_nodes_data
            WHERE id_node = ?
            AND id_variable = ?
            """,
                [node.get("id_node"), pair.get("id_variable")],
            )
        conn.commit()
        conn.close()

    def delete_template_datas(self, template, pair_list):
        """
        Запрос на удаление данных вершины в Project_nodes_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase delete_template_datas(template, pair_list):\ntemplate = {template}\npair_list = {pair_list}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        for pair in pair_list:
            cursor.execute(
                """
            DELETE FROM Project_templates_data
            WHERE id_template = ?
            AND id_variable = ?
            """,
                [template.get("id_template"), pair.get("id_variable")],
            )
        conn.commit()
        conn.close()

    def delete_page_datas(self, page, pair_list):
        """
        Запрос на удаление данных страницы в Project_pages_data.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase delete_page_datas(page, pair_list):\npage = {page}\npair_list = {pair_list}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        for pair in pair_list:
            cursor.execute(
                """
            DELETE FROM Project_pages_data
            WHERE id_page = ?
            AND id_variable = ?
            """,
                [page.get("id_page"), pair.get("id_variable")],
            )
        conn.commit()
        conn.close()

    def insert_variable(self, variable) -> int:
        """
        Запрос на вставку данных переменной в Project_variables.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase insert_variable(variable):\nvariable = {variable}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        INSERT INTO Project_variables
        (name_variable, type_variable, title_variable, order_variable, config_variable, description_variable)
        VALUES
        (?, ?, ?, ?, ?, ?)
        """,
            [
                variable.get("name_variable"),
                variable.get("type_variable"),
                variable.get("title_variable"),
                variable.get("order_variable"),
                variable.get("config_variable"),
                variable.get("description_variable"),
            ],
        )
        conn.commit()
        primary_key = cursor.lastrowid
        conn.close()
        return primary_key

    def update_variable(self, variable):
        """
        Запрос на обновление данных переменной в Project_variables.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase update_variable(variable):\nvariable = {variable}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_variables
        SET
        name_variable = ?,
        type_variable = ?,
        title_variable = ?,
        order_variable = ?,
        config_variable = ?,
        description_variable = ?
        WHERE id_variable = ?
        """,
            [
                variable.get("name_variable"),
                variable.get("type_variable"),
                variable.get("title_variable"),
                variable.get("order_variable"),
                variable.get("config_variable"),
                variable.get("description_variable"),
                variable.get("id_variable"),
            ],
        )
        conn.commit()
        conn.close()

    def delete_variable(self, variable):
        """
        Запрос на удаление данных переменной в Project_variables.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase delete_variable(variable):\nvariable = {variable}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(
            """
        DELETE FROM Project_variables
        WHERE id_variable = ?
        """,
            [variable.get("id_variable")],
        )
        conn.commit()
        conn.close()

    def get_variable_by_name(self, name_variable):
        """
        Запрос на получение переменной по имени в Project_variables.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_variable_by_name(name_variable):\nname_variable = {name_variable}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT *
        FROM Project_variables
        WHERE name_variable = ?
        """,
            [name_variable],
        )
        result = self.get_fetchone(cursor)
        conn.close()
        return result

    def get_node_by_name(self, name_node):
        """
        Запрос на получение вершины по имени в Project_nodes.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase get_node_by_name(name_node):\nname_node = {name_node}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT *
        FROM Project_nodes
        WHERE name_node = ?
        """,
            [name_node],
        )
        result = self.get_fetchone(cursor)
        conn.close()
        return result

    def update_node(self, node):
        """
        Обновление данных вершины.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase update_node(node): node = {node}"
        )

        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_nodes
        SET name_node = ?, id_parent = ?, order_node = ?, type_node = ?, id_active_template = ?, included = ?
        WHERE id_node = ?
        """,
            [
                node.get("name_node"),
                node.get("id_parent"),
                node.get("order_node"),
                node.get("type_node"),
                node.get("id_active_template"),
                node.get("included"),
                node.get("id_node"),
            ],
        )
        conn.commit()
        conn.close()

    def add_node(self, edit_node):
        """
        Добавление вершины.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase add_node(edit_node): edit_node = {edit_node}"
        )

        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        INSERT INTO Project_nodes (id_active_template, id_parent, included, name_node, order_node, type_node)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
            [
                edit_node.get("id_active_template"),
                edit_node.get("id_parent"),
                edit_node.get("included"),
                edit_node.get("name_node"),
                edit_node.get("order_node"),
                edit_node.get("type_node"),
            ],
        )
        conn.commit()
        conn.close()

    def delete_node(self, node):
        """
        Удаление вершины по объекту node.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase delete_node(node): node = {node}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(
            """
        DELETE FROM Project_nodes
        WHERE id_node = ?
        """,
            [node.get("id_node")],
        )
        conn.commit()
        conn.close()

    def set_new_parent_for_child_node(self, current_node, child_node):
        """
        Установка родительской вершины для дочерей группы.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase set_new_parent_for_child_node(current_node, child_node):\nnode = {current_node}\nchild_node = {child_node}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_nodes
        SET id_parent = ?, order_node = ?
        WHERE id_node = ?
        """,
            [
                current_node.get("id_parent"),
                current_node.get("order_node"),
                child_node.get("id_node"),
            ],
        )
        conn.commit()
        conn.close()

    def set_order_for_node(self, node, new_order):
        """
        Установка порядка для вершины.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase set_order_for_node(node, new_order):\nnode = {node}\nnew_order = {new_order}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_nodes
        SET order_node = ?
        WHERE id_node = ?
        """,
            [new_order, node.get("id_node")],
        )
        conn.commit()
        conn.close()

    def set_order_for_page(self, page, new_order):
        """
        Установка порядка для страницы.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase set_order_for_page(page, new_order):\npage = {page}\nnew_order = {new_order}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_pages
        SET order_page = ?
        WHERE id_page = ?
        """,
            [new_order, page.get("id_page")],
        )
        conn.commit()
        conn.close()

    def set_order_for_variable(self, variable, new_order):
        """
        Установка порядка для переменной.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase set_order_for_variable(variable, new_order):\nvariable = {variable}\nnew_order = {new_order}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_variables
        SET order_variable = ?
        WHERE id_variable = ?
        """,
            [new_order, variable.get("id_variable")],
        )
        conn.commit()
        conn.close()

    def add_template(self, name_template, form) -> int:
        """
        Добавление шаблона.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase add_template(name_template, form):\nname_template = {name_template}\nform = {form}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        INSERT INTO Project_templates (name_template, id_parent_node)
        VALUES (?, ?)
        """,
            [name_template, form.get("id_node")],
        )
        conn.commit()
        primary_key = cursor.lastrowid
        conn.close()
        return primary_key

    def set_new_name_for_template(self, template, name_template):
        """
        Установка нового имени шаблона.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase set_new_name_for_template(template, name_template):\ntemplate = {template}\nname_template = {name_template}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_templates
        SET name_template = ?
        WHERE id_template = ?
        """,
            [name_template, template.get("id_template")],
        )
        conn.commit()
        conn.close()

    def delete_template(self, template):
        """
        Удаление шаблона.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase delete_template(template):\ntemplate = {template}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(
            """
        DELETE FROM Project_templates
        WHERE id_template = ?
        """,
            [template.get("id_template")],
        )
        conn.commit()
        conn.close()

    def set_active_template_for_node_by_id(self, id_node, id_template):
        """
        Установка активного шаблона для вершины.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase set_active_template_for_node_by_id(id_node, id_template):\nid_node = {id_node}\nid_template = {id_template}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_nodes
        SET id_active_template = ?
        WHERE id_node = ?
        """,
            [id_template, id_node],
        )
        conn.commit()
        conn.close()

    def set_new_name_and_filename_for_page(self, page, name_page, filename_page):
        """
        Установка нового имени и имени файла для страницы.
        """
        self.__osbm.obj_logg.debug_logger(
            f"ProjectDatabase set_new_name_and_filename_for_page(page, name_page, filename_page):\npage = {page}\nname_page = {name_page}\nfilename_page = {filename_page}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_pages
        SET name_page = ?, filename_page = ?
        WHERE id_page = ?
        """,
            [name_page, filename_page, page.get("id_page")],
        )
        conn.commit()
        conn.close()


# obj_prodb = ProjectDatabase()
