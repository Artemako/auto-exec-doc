import sqlite3
import os


class ProjectDatabase:
    def __init__(self, obs_manager):
        self.__obs_manager = obs_manager
        self.__obs_manager.obj_l.debug_logger("ProjectDatabase __init__()")

    def create_and_config_db_project(self):
        """
        Настройка базы данных перед использованием проекта
        """
        self.__obs_manager.obj_l.debug_logger(
            "ProjectDatabase create_and_config_db_project()"
        )

        if not os.path.exists(self.__obs_manager.obj_dpm.get_db_project_dirpath()):
            # Добавляем данные в пустую БД
            self.add_tables_and_datas_to_empty_db_project()

        # set всем included = True
        self.set_all_included_in_db_project_to_true()

    def add_tables_and_datas_to_empty_db_project(self):
        """
        Добавление таблиц и данных в БД программы при запуске.
        """
        self.__obs_manager.obj_l.debug_logger(
            "ProjectDatabase add_tables_and_datas_to_empty_db_project()"
        )
        conn = sqlite3.connect(self.__obs_manager.obj_dpm.get_db_project_dirpath())
        cursor = conn.cursor()
        cursor.executescript(
            """
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Project_tag_config_date" (
	"id_config"	INTEGER UNIQUE,
	"id_tag"	INTEGER,
	"type_config"	TEXT,
	"value_config"	TEXT,
	"note_config"	TEXT,
	FOREIGN KEY("id_tag") REFERENCES "Project_tags"("id_tag"),
	PRIMARY KEY("id_config" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Project_tag_config_table" (
	"id_config"	INTEGER UNIQUE,
	"id_tag"	INTEGER,
	"type_config"	TEXT,
	"value_config"	TEXT,
	"note_config"	TEXT,
	"order_config"	INTEGER,
	FOREIGN KEY("id_tag") REFERENCES "Project_tags"("id_tag"),
	PRIMARY KEY("id_config" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Project_nodes_data" (
	"id_pair"	INTEGER UNIQUE,
	"id_node"	INTEGER,
	"id_tag"	INTEGER,
	"name_tag"	TEXT,
	"value"	TEXT,
	FOREIGN KEY("id_tag") REFERENCES "Project_tags"("id_tag"),
	FOREIGN KEY("id_node") REFERENCES "Project_nodes"("id_node"),
	PRIMARY KEY("id_pair" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Project_pages_data" (
	"id_pair"	INTEGER UNIQUE,
	"id_page"	INTEGER,
	"id_tag"	INTEGER,
	"name_tag"	TEXT,
	"value"	TEXT,
	FOREIGN KEY("id_page") REFERENCES "Project_pages"("id_page"),
	FOREIGN KEY("id_tag") REFERENCES "Project_tags"("id_tag"),
	PRIMARY KEY("id_pair" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Project_templates" (
	"id_template"	INTEGER NOT NULL UNIQUE,
	"name_template"	TEXT,
	"id_parent_node"	INTEGER,
	FOREIGN KEY("id_parent_node") REFERENCES "Project_nodes"("id_node"),
	PRIMARY KEY("id_template" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Project_pages" (
	"id_page"	INTEGER NOT NULL UNIQUE,
	"id_parent_template"	INTEGER,
	"page_name"	TEXT,
	"page_filename"	TEXT,
	"order_page"	INTEGER,
	"included"	INTEGER NOT NULL DEFAULT 1,
	FOREIGN KEY("id_parent_template") REFERENCES "Project_templates"("id_template"),
	PRIMARY KEY("id_page" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Project_templates_data" (
	"id_pair"	INTEGER UNIQUE,
	"id_template"	INTEGER,
	"id_tag"	INTEGER,
	"name_tag"	TEXT,
	"value"	TEXT,
	FOREIGN KEY("id_template") REFERENCES "Project_templates"("id_template"),
	FOREIGN KEY("id_tag") REFERENCES "Project_tags"("id_tag"),
	PRIMARY KEY("id_pair" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Project_nodes" (
	"id_node"	INTEGER NOT NULL UNIQUE,
	"name_node"	TEXT,
	"id_parent"	INTEGER,
	"order_node"	TEXT,
	"type_node"	TEXT,
	"id_active_template"	INTEGER,
	"included"	INTEGER NOT NULL DEFAULT 1,
	FOREIGN KEY("id_active_template") REFERENCES "Project_templates"("id_template"),
	PRIMARY KEY("id_node" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Project_tags" (
	"id_tag"	INTEGER NOT NULL UNIQUE,
	"name_tag"	TEXT NOT NULL UNIQUE,
	"type_tag"	TEXT NOT NULL,
	"title_tag"	TEXT,
	"description_tag"	TEXT,
	"is_global"	INTEGER,
	PRIMARY KEY("id_tag" AUTOINCREMENT)
);
INSERT INTO "Project_tag_config_date" VALUES (100,1208,'FORMAT','yyyy',NULL);
INSERT INTO "Project_tag_config_date" VALUES (101,1009,'FORMAT','yyyy',NULL);
INSERT INTO "Project_tag_config_date" VALUES (103,1227,'FORMAT','yyyy',NULL);
INSERT INTO "Project_tag_config_date" VALUES (104,1228,'FORMAT','yyyy',NULL);
INSERT INTO "Project_tag_config_table" VALUES (100,1200,'HEADER','Форма','',0);
INSERT INTO "Project_tag_config_table" VALUES (101,1200,'HEADER','Наименование','',1);
INSERT INTO "Project_tag_config_table" VALUES (102,1200,'HEADER','Количество листов','',2);
INSERT INTO "Project_tag_config_table" VALUES (103,1200,'HEADER','Номера страниц','',3);
INSERT INTO "Project_tag_config_table" VALUES (104,1200,'HEADER','Примечание','',4);
INSERT INTO "Project_tag_config_table" VALUES (110,1200,'CONTENT','форма','',0);
INSERT INTO "Project_tag_config_table" VALUES (111,1200,'CONTENT','наименование_документа','',1);
INSERT INTO "Project_tag_config_table" VALUES (112,1200,'CONTENT','кол_листов','',2);
INSERT INTO "Project_tag_config_table" VALUES (113,1200,'CONTENT','номера_стр','',3);
INSERT INTO "Project_tag_config_table" VALUES (114,1200,'CONTENT','примечание','',4);
INSERT INTO "Project_tag_config_table" VALUES (200,1201,'HEADER','Форма','',0);
INSERT INTO "Project_tag_config_table" VALUES (201,1201,'HEADER','Наименование','',1);
INSERT INTO "Project_tag_config_table" VALUES (202,1201,'HEADER','Количество листов','',2);
INSERT INTO "Project_tag_config_table" VALUES (203,1201,'HEADER','Номера страниц','',3);
INSERT INTO "Project_tag_config_table" VALUES (204,1201,'HEADER','Примечание','',4);
INSERT INTO "Project_tag_config_table" VALUES (205,1201,'CONTENT','форма','',0);
INSERT INTO "Project_tag_config_table" VALUES (206,1201,'CONTENT','наименование_документа','',1);
INSERT INTO "Project_tag_config_table" VALUES (207,1201,'CONTENT','кол_листов','',2);
INSERT INTO "Project_tag_config_table" VALUES (208,1201,'CONTENT','номера_стр','',3);
INSERT INTO "Project_tag_config_table" VALUES (209,1201,'CONTENT','примечание','',4);
INSERT INTO "Project_tag_config_table" VALUES (300,1202,'HEADER','Форма','',0);
INSERT INTO "Project_tag_config_table" VALUES (301,1202,'HEADER','Наименование','',1);
INSERT INTO "Project_tag_config_table" VALUES (302,1202,'HEADER','Количество листов','',2);
INSERT INTO "Project_tag_config_table" VALUES (303,1202,'HEADER','Номера страниц','',3);
INSERT INTO "Project_tag_config_table" VALUES (304,1202,'HEADER','Примечание','',4);
INSERT INTO "Project_tag_config_table" VALUES (305,1202,'CONTENT','форма','',0);
INSERT INTO "Project_tag_config_table" VALUES (306,1202,'CONTENT','наименование_документа','',1);
INSERT INTO "Project_tag_config_table" VALUES (307,1202,'CONTENT','кол_листов','',2);
INSERT INTO "Project_tag_config_table" VALUES (308,1202,'CONTENT','номера_стр','',3);
INSERT INTO "Project_tag_config_table" VALUES (309,1202,'CONTENT','примечание','',4);
INSERT INTO "Project_tag_config_table" VALUES (400,1209,'HEADER','Номер формы','',0);
INSERT INTO "Project_tag_config_table" VALUES (401,1209,'HEADER','Наименование документа','',1);
INSERT INTO "Project_tag_config_table" VALUES (402,1209,'HEADER','Количество листов','',2);
INSERT INTO "Project_tag_config_table" VALUES (403,1209,'HEADER','Номера страниц','',3);
INSERT INTO "Project_tag_config_table" VALUES (404,1209,'HEADER','Примечания','',4);
INSERT INTO "Project_tag_config_table" VALUES (405,1209,'CONTENT','номер_формы','',0);
INSERT INTO "Project_tag_config_table" VALUES (406,1209,'CONTENT','наименование_документа','',1);
INSERT INTO "Project_tag_config_table" VALUES (407,1209,'CONTENT','кол_листов','',2);
INSERT INTO "Project_tag_config_table" VALUES (408,1209,'CONTENT','номера_стр','',3);
INSERT INTO "Project_tag_config_table" VALUES (409,1209,'CONTENT','примечание','',4);
INSERT INTO "Project_tag_config_table" VALUES (500,1220,'HEADER','Марка кабеля','',0);
INSERT INTO "Project_tag_config_table" VALUES (501,1220,'HEADER','Длина кабеля (всего) в м.','',1);
INSERT INTO "Project_tag_config_table" VALUES (502,1220,'HEADER','Оптическая длина в м.','',2);
INSERT INTO "Project_tag_config_table" VALUES (503,1220,'HEADER','Информация','',3);
INSERT INTO "Project_tag_config_table" VALUES (504,1220,'CONTENT','марка','',0);
INSERT INTO "Project_tag_config_table" VALUES (505,1220,'CONTENT','длина_всего','',1);
INSERT INTO "Project_tag_config_table" VALUES (506,1220,'CONTENT','длина_опт','',2);
INSERT INTO "Project_tag_config_table" VALUES (507,1220,'CONTENT','инфо','',3);
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
INSERT INTO "Project_templates" VALUES (1,'main',10);
INSERT INTO "Project_templates" VALUES (2,'main',11);
INSERT INTO "Project_templates" VALUES (3,'main',1201);
INSERT INTO "Project_templates" VALUES (4,'main',1202);
INSERT INTO "Project_templates" VALUES (5,'main',1203);
INSERT INTO "Project_pages" VALUES (10,1,'Л.1. Титульный лист.','1-ТЛ-1',0,1);
INSERT INTO "Project_pages" VALUES (11,1,'Л.2. Титульный лист.','1-ТЛ-2',1,1);
INSERT INTO "Project_pages" VALUES (20,2,'Л.1. Реестр исполнительной документации ВОЛС.','2-РД-1',0,1);
INSERT INTO "Project_pages" VALUES (30,3,'Л.1. Паспорт трассы. Опись документов.','3-ПТ1-1',0,1);
INSERT INTO "Project_pages" VALUES (40,4,'Л.1. Паспорт трассы волоконно-оптической линии связи на участке.','3-ПТ2-1',0,1);
INSERT INTO "Project_pages" VALUES (50,5,'Л.1. Скелетная схема ВОЛП и основные данные цепей кабеля.','3-ПТ3-1',0,1);
INSERT INTO "Project_nodes" VALUES (0,'Проект',NULL,'0','PROJECT',NULL,1);
INSERT INTO "Project_nodes" VALUES (10,'Титульный лист',0,'1','FORM',1,1);
INSERT INTO "Project_nodes" VALUES (11,'Реестр документации',0,'2','FORM',2,1);
INSERT INTO "Project_nodes" VALUES (12,'Паспорт трассы',0,'3','GROUP',NULL,1);
INSERT INTO "Project_nodes" VALUES (1201,'ПТ-1',12,'1','FORM',3,1);
INSERT INTO "Project_nodes" VALUES (1202,'ПТ-2',12,'2','FORM',4,1);
INSERT INTO "Project_nodes" VALUES (1203,'ПТ-3',12,'3','FORM',5,1);
INSERT INTO "Project_tags" VALUES (1000,'организационно_правовая_форма','TEXT','Организационно-правовая форма',NULL,0);
INSERT INTO "Project_tags" VALUES (1001,'название_компании','TEXT','Название компании',NULL,0);
INSERT INTO "Project_tags" VALUES (1002,'адрес_компании','TEXT','Адрес компании',NULL,0);
INSERT INTO "Project_tags" VALUES (1003,'название_объекта','TEXT','Название объекта',NULL,0);
INSERT INTO "Project_tags" VALUES (1004,'участок','TEXT','Участок',NULL,0);
INSERT INTO "Project_tags" VALUES (1005,'номер_кабеля','TEXT','Номер кабеля',NULL,0);
INSERT INTO "Project_tags" VALUES (1006,'заказчик','TEXT','Заказчик',NULL,0);
INSERT INTO "Project_tags" VALUES (1007,'строительно_монтажная_организация','TEXT','Строительно-монтажная организация',NULL,0);
INSERT INTO "Project_tags" VALUES (1008,'город','TEXT','Город',NULL,0);
INSERT INTO "Project_tags" VALUES (1009,'год','DATE','Год',NULL,0);
INSERT INTO "Project_tags" VALUES (1100,'инж_про_ком','TEXT','Компания инженера-проектировщика',NULL,0);
INSERT INTO "Project_tags" VALUES (1101,'инж_про_ком_фио','TEXT','ФИО инженера-проектировщика',NULL,0);
INSERT INTO "Project_tags" VALUES (1102,'гла_инж_компания','TEXT','Компания главного инженера',NULL,0);
INSERT INTO "Project_tags" VALUES (1103,'гла_инж_фио','TEXT','ФИО главного инженера',NULL,0);
INSERT INTO "Project_tags" VALUES (1200,'реестр_ид_паспорт_трассы','TABLE','Реестр ИД ВОЛС. Паспорт трассы',NULL,0);
INSERT INTO "Project_tags" VALUES (1201,'реестр_ид_эл_паспорт_трассы','TABLE','Реестр ИД ВОЛС. Электрический паспорт трассы',NULL,0);
INSERT INTO "Project_tags" VALUES (1202,'рабочая_документация','TABLE','Реестр ИД ВОЛС. Рабочая документация',NULL,0);
INSERT INTO "Project_tags" VALUES (1208,'дата','DATE','Дата',NULL,0);
INSERT INTO "Project_tags" VALUES (1209,'пт_опись_документов','TABLE','Паспорт трассы. Опись документов.',NULL,0);
INSERT INTO "Project_tags" VALUES (1220,'кабеля','TABLE','Кабеля.',NULL,0);
INSERT INTO "Project_tags" VALUES (1225,'общая_физ_длина','TEXT','Общая физическая длина',NULL,0);
INSERT INTO "Project_tags" VALUES (1226,'общая_опт_длина','TEXT','Общая оптическая длина',NULL,0);
INSERT INTO "Project_tags" VALUES (1227,'год_прокладки_кабеля','DATE','Год прокладки кабеля',NULL,0);
INSERT INTO "Project_tags" VALUES (1228,'год_составления_паспорта','DATE','Год составления паспорта',NULL,0);
INSERT INTO "Project_tags" VALUES (1229,'отв_пред_орг_фио ','TEXT','ФИО ответственного представителя организации',NULL,0);
INSERT INTO "Project_tags" VALUES (1230,'скелетная_схема_ВОЛП','IMAGE','Скелетная схема ВОЛП',NULL,0);
COMMIT;

        """
        )
        conn.commit()
        conn.close()

    def get_conn(self) -> object:
        """
        Запрос курсора.
        """
        self.__obs_manager.obj_l.debug_logger("ProjectDatabase get_conn() -> object")
        conn = sqlite3.connect(self.__obs_manager.obj_dpm.get_db_project_dirpath())
        conn.row_factory = sqlite3.Row
        return conn

    def get_fetchall(self, cursor):
        self.__obs_manager.obj_l.debug_logger(
            "ProjectDatabase get_fetchall(cursor, conn) -> list"
        )
        cursor_result = cursor.fetchall()
        result = [dict(row) for row in cursor_result] if cursor_result else []
        return result

    def get_fetchone(self, cursor):
        self.__obs_manager.obj_l.debug_logger(
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
        self.__obs_manager.obj_l.debug_logger(
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
        self.__obs_manager.obj_l.debug_logger(
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
        self.__obs_manager.obj_l.debug_logger(
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
        self.__obs_manager.obj_l.debug_logger(
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
        self.__obs_manager.obj_l.debug_logger(
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
        self.__obs_manager.obj_l.debug_logger(
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
        self.__obs_manager.obj_l.debug_logger(
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
        """,
            [template.get("id_template")],
        )

        result = self.get_fetchall(cursor)
        conn.close()
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase get_pages_by_template(template) -> list: template = {template}\nresult = {result}"
        )
        return result

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
        self.__obs_manager.obj_l.debug_logger(
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
        self.__obs_manager.obj_l.debug_logger(
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
        self.__obs_manager.obj_l.debug_logger(
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
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase get_node_by_id(id_node) -> object: id_node = {id_node}\nresult = {result}"
        )
        return result

    def get_config_tag_by_id(self, id_tag) -> object:
        """
        Запрос на получение config_tag по имени формы.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_tags
        WHERE id_tag = ?
        """,
            [id_tag],
        )
        result = self.get_fetchone(cursor)
        conn.close()
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase get_config_tag(id_tag) -> list: id_tag = {id_tag}\nresult = {result}"
        )
        return result

    def get_config_date_by_id(self, id_tag) -> list:
        """
        Запрос на получение config_date по имени формы.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_tag_config_date
        WHERE id_tag = ?
        """,
            [id_tag],
        )
        result = self.get_fetchall(cursor)
        conn.close()
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase get_config_date(id_tag) -> list: name_tag = {id_tag}\nresult = {result}"
        )
        return result

    def get_config_table_by_id(self, id_tag) -> list:
        """
        Запрос на получение config_table по имени формы.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_tag_config_table
        WHERE id_tag = ?
        """,
            [id_tag],
        )
        result = self.get_fetchall(cursor)
        conn.close()
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase get_config_table(id_tag) -> list: id_tag = {id_tag}\nresult = {result}"
        )
        return result

    def set_included_for_node(self, node, state):
        """
        Запрос на установку включенности для вершины.
        """
        self.__obs_manager.obj_l.debug_logger(
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
        self.__obs_manager.obj_l.debug_logger(
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
        self.__obs_manager.obj_l.debug_logger(
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
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase get_template_data(template) -> list: template = {template}\nresult = {result}"
        )
        return result

    def get_node_data(self, node) -> list:
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
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase get_node_data(node) -> list: node = {node}\nresult = {result}"
        )
        return result

    def update_page_data(self, id_pair, value):
        """
        Запрос на обновление данных страницы в Project_pages_data.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase update_page_data(id_pair, value): id_pair = {id_pair}, value = {value}"
        )

        conn = self.get_conn()
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

    def update_template_data(self, id_pair, value):
        """
        Запрос на обновление данных шаблона в Project_templates_data.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase update_template_data(id_pair, value): id_pair = {id_pair}, value = {value}"
        )

        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_templates_data
        SET value = ?
        WHERE id_pair = ?
        """,
            [value, id_pair],
        )
        conn.commit()
        conn.close()

    def update_node_data(self, id_pair, value):
        """
        Запрос на обновление данных вершины в Project_nodes_data.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase update_node_data(id_pair, value): id_pair = {id_pair}, value = {value}"
        )

        conn = self.get_conn()
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

    def get_page_pair_value_by_id(self, id_pair):
        """
        Запрос на получение значения по id_pair в Project_pages_data.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT value FROM Project_pages_data
        WHERE id_pair = ?
        """,
            [id_pair],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase get_page_pair_value_by_id(id_pair): id_pair = {id_pair}\nresult = {result}"
        )
        return result

    def get_template_pair_value_by_id(self, id_pair):
        """
        Запрос на получение значения по id_pair в Project_templates_data.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT value FROM Project_templates_data
        WHERE id_pair = ?
        """,
            [id_pair],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase get_template_pair_value_by_id(id_pair): id_pair = {id_pair}\nresult = {result}"
        )
        return result

    def get_node_pair_value_by_id(self, id_pair):
        """
        Запрос на получение значения по id_pair в Project_nodes_data.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT value FROM Project_nodes_data
        WHERE id_pair = ?
        """,
            [id_pair],
        )

        result = self.get_fetchone(cursor)
        conn.close()
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase get_node_pair_value_by_id(id_pair): id_pair = {id_pair}\nresult = {result}"
        )
        return result

    def set_all_included_in_db_project_to_true(self):
        """
        Установка всех included = True
        """
        self.__obs_manager.obj_l.debug_logger(
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

    def get_project_tags(self) -> list:
        """
        Запрос на получение тегов проекта.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_tags
        """
        )
        result = self.get_fetchall(cursor)
        conn.close()
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase get_project_tags() -> list\nresult = {result}"
        )
        return result

    def get_tag_config_by_id(self, id_tag):
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        SELECT * FROM Project_tags
        WHERE id_tag = ?
        """,
            [id_tag],
        )
        result = self.get_fetchall(cursor)
        conn.close()
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase get_tag_config_by_id(id_tag): id_tag = {id_tag}\nresult = {result}"
        )
        return result

    def delete_node_data(self, node):
        """
        Удаление всех тегов у вершины.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase delete_node_data(node): node = {node}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.executescript(
            """
        DELETE FROM Project_nodes_data
        WHERE id_node = ?
        """,
            [node.get("id_node")],
        )
        conn.commit()
        conn.close()

    def insert_node_datas(self, node, pair_list):
        """
        Запрос на обновление данных вершины в Project_nodes_data.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase insert_node_datas(node, pair_list):\nnode = {node}\npair_list = {pair_list}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        for pair in pair_list:
            cursor.execute(
                """
            INSERT INTO Project_nodes_data
            (id_node, id_tag)
            VALUES
            (?, ?)
            """,
                [node.get("id_node"), pair.get("id_tag")],
            )
        conn.commit()
        conn.close()

    def insert_template_datas(self, template, pair_list):
        """
        Запрос на обновление данных вершины в Project_nodes_data.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase insert_template_datas(template, pair_list):\ntemplate = {template}\npair_list = {pair_list}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        for pair in pair_list:
            cursor.execute(
                """
            INSERT INTO Project_templates_data
            (id_template, id_tag)
            VALUES
            (?, ?)
            """,
                [template.get("id_template"), pair.get("id_tag")],
            )
        conn.commit()
        conn.close()

    def insert_page_datas(self, page, pair_list):
        """
        Запрос на обновление данных страницы в Project_pages_data.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase insert_page_datas(page, pair_list):\npage = {page}\npair_list = {pair_list}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        for pair in pair_list:
            cursor.execute(
                """
            INSERT INTO Project_pages_data
            (id_page, id_tag)
            VALUES
            (?, ?)
            """,
                [page.get("id_page"), pair.get("id_tag")],
            )
        conn.commit()
        conn.close()

    def delete_node_datas(self, node, pair_list):
        """
        Запрос на удаление данных вершины в Project_nodes_data.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase delete_node_datas(node, pair_list):\nnode = {node}\npair_list = {pair_list}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        for pair in pair_list:
            cursor.execute(
                """
            DELETE FROM Project_nodes_data
            WHERE id_node = ?
            AND id_tag = ?
            """,
                [node.get("id_node"), pair.get("id_tag")],
            )
        conn.commit()
        conn.close()

    def delete_template_datas(self, template, pair_list):
        """
        Запрос на удаление данных вершины в Project_nodes_data.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase delete_template_datas(template, pair_list):\ntemplate = {template}\npair_list = {pair_list}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        for pair in pair_list:
            cursor.execute(
                """
            DELETE FROM Project_templates_data
            WHERE id_template = ?
            AND id_tag = ?
            """,
                [template.get("id_template"), pair.get("id_tag")],
            )
        conn.commit()
        conn.close()

    def delete_page_datas(self, page, pair_list):
        """
        Запрос на удаление данных страницы в Project_pages_data.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase delete_page_datas(page, pair_list):\npage = {page}\npair_list = {pair_list}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        for pair in pair_list:
            cursor.execute(
                """
            DELETE FROM Project_pages_data
            WHERE id_page = ?
            AND id_tag = ?
            """,
                [page.get("id_page"), pair.get("id_tag")],
            )
        conn.commit()
        conn.close()

    def delete_tag(self, tag):
        """
        Запрос на удаление данных тега в Project_tags.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase delete_tag(tag):\ntag = {tag}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        DELETE FROM Project_tags
        WHERE id_tag = ?
        """,
            [tag.get("id_tag")],
        )
        conn.commit()
        conn.close()

    def update_node(self, node):
        """
        Обновление данных вершины.
        """
        self.__obs_manager.obj_l.debug_logger(
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
        self.__obs_manager.obj_l.debug_logger(
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
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase delete_node(node): node = {node}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
        """
        DELETE FROM Project_nodes
        WHERE id_node = ?
        """,
            [node.get("id_node")],
        )
        conn.commit()
        conn.close()


    def set_group_parent_for_child_group(self, node, child_node):
        """
        Установка родительской вершины для дочерей группы.
        """
        self.__obs_manager.obj_l.debug_logger(
            f"ProjectDatabase set_group_parent_for_child_group(node, child_node):\nnode = {node}\nchild_node = {child_node}"
        )
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE Project_nodes
        SET id_parent = ?, order_node = ?
        WHERE id_node = ?
        """,
            [node.get("id_parent"), node.get("order_node"), child_node.get("id_node")],
        )
        conn.commit()
        conn.close()


    def set_order_for_node(self, node, new_order):
        """
        Установка порядка для вершины.
        """
        self.__obs_manager.obj_l.debug_logger(
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


# obj_pd = ProjectDatabase()
