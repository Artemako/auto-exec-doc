import sqlite3

def osnova():
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.executescript(
        """
        BEGIN TRANSACTION;
        CREATE TABLE IF NOT EXISTS "Project_structure_of_nodes" (
            "id_node"	INTEGER NOT NULL UNIQUE,
            "name_node"	TEXT,
            "id_parent"	INTEGER,
            "type_node"	TEXT NOT NULL,
            "id_left"	INTEGER,
            "id_right"	INTEGER,
            "template_name"	TEXT,
            PRIMARY KEY("id_node" AUTOINCREMENT)
        );
        CREATE TABLE IF NOT EXISTS "Project_content_config_list" (
            "id_content"	INTEGER NOT NULL UNIQUE,
            "name_content"	TEXT NOT NULL UNIQUE,
            "type_content"	TEXT NOT NULL,
            "note_content"	TEXT,
            PRIMARY KEY("id_content" AUTOINCREMENT)
        );
        CREATE TABLE IF NOT EXISTS "Project_content_config_table" (
            "id_config"	INTEGER NOT NULL UNIQUE,
            "id_content"	INTEGER NOT NULL,
            "type_config"	TEXT NOT NULL,
            "value_config"	TEXT NOT NULL,
            "note_config"	TEXT,
            FOREIGN KEY("id_content") REFERENCES "Project_content_config_list"("id_content"),
            PRIMARY KEY("id_config" AUTOINCREMENT)
        );
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (0,'Проект',NULL,'PROJECT',NULL,NULL,'');
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (10,'Титульный лист',0,'FORM',NULL,11,'main');
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (11,'Реестр документации',0,'FORM',10,12,'main');
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (12,'Паспорт трассы',0,'GROUP',11,NULL,NULL);
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (1201,'ПТ-1',12,'FORM',NULL,1202,'main');
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (1202,'ПТ-2',12,'FORM',1201,1203,'main');
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (1203,'ПТ-3',12,'FORM',1202,1204,'main');
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (1204,'ПТ-4',12,'FORM',1203,1205,'main');
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (1205,'ПТ-5',12,'FORM',1204,1206,'main');
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (1206,'ПТ-6',12,'FORM',1205,1207,'main');
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (1207,'ПТ-7',12,'FORM',1206,1208,'main');
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (1208,'ПТ-8',12,'FORM',1207,1209,'main');
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (1209,'ПТ-9',12,'FORM',1208,1210,'main');
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (1210,'ПТ-10',12,'FORM',1209,1211,'main');
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (1211,'ПТ-11',12,'FORM',1210,1212,'main');
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (1212,'ПТ-12',12,'FORM',1211,1213,'main');
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (1213,'ПТ-13',12,'FORM',1212,1214,'main');
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (1214,'ПТ-14',12,'FORM',1213,1215,'main');
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (1215,'ПТ-15',12,'FORM',1214,1216,'main');
        INSERT OR IGNORE INTO "Project_structure_of_nodes" VALUES (1216,'ПТ-16',12,'FORM',1215,NULL,'main');
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1000,'организационно_правовая_форма','TEXT',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1001,'название_компании','TEXT',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1002,'адрес_компании','TEXT',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1003,'название_объекта','TEXT',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1004,'участок','TEXT',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1005,'номер_кабеля','TEXT',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1006,'заказчик','TEXT',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1007,'строительно_монтажная_организация','TEXT',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1008,'город','TEXT',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1009,'год','DATE','YEAR');
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1100,'инж_про_ком','TEXT',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1101,'инж_про_ком_фио','TEXT',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1102,'гла_инж_компания','TEXT',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1103,'гла_инж_фио','TEXT',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1200,'реестр_ид_паспорт_трассы','TABLE',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1201,'реестр_ид_эл_паспорт_трассы','TABLE',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1202,'рабочая_документация','TABLE',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1208,'дата','DATE',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1209,'пт_опись_документов','TABLE',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1220,'кабеля','TABLE',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1225,'общая_физ_длина','TEXT',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1226,'общая_опт_длина','TEXT',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1227,'год_прокладки_кабеля','TEXT',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1228,'год_составления_паспорта','TEXT',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1229,'отв_пред_орг_фио ','TEXT',NULL);
        INSERT OR IGNORE INTO "Project_content_config_list" VALUES (1230,'скелетная_схема_ВОЛП','IMAGE',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (100,1200,'HEADER','Форма',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (101,1200,'HEADER','Наименование',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (102,1200,'HEADER','Количество листов',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (103,1200,'HEADER','Номера страниц',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (104,1200,'HEADER','Примечание',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (110,1200,'CONTENT','форма',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (111,1200,'CONTENT','наименование_документа',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (112,1200,'CONTENT','кол_листов',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (113,1200,'CONTENT','номера_стр',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (114,1200,'CONTENT','примечание',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (200,1201,'HEADER','Форма',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (201,1201,'HEADER','Наименование',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (202,1201,'HEADER','Количество листов',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (203,1201,'HEADER','Номера страниц',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (204,1201,'HEADER','Примечание',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (205,1201,'CONTENT','форма',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (206,1201,'CONTENT','наименование_документа',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (207,1201,'CONTENT','кол_листов',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (208,1201,'CONTENT','номера_стр',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (209,1201,'CONTENT','примечание',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (300,1202,'HEADER','Форма',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (301,1202,'HEADER','Наименование',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (302,1202,'HEADER','Количество листов',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (303,1202,'HEADER','Номера страниц',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (304,1202,'HEADER','Примечание',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (305,1202,'CONTENT','форма',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (306,1202,'CONTENT','наименование_документа',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (307,1202,'CONTENT','кол_листов',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (308,1202,'CONTENT','номера_стр',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (309,1202,'CONTENT','примечание',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (400,1209,'HEADER','Номер формы',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (401,1209,'HEADER','Наименование документа',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (402,1209,'HEADER','Количество листов',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (403,1209,'HEADER','Номера страниц',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (404,1209,'HEADER','Примечания',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (405,1209,'CONTENT','номер_формы ',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (406,1209,'CONTENT','наименование_документа',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (407,1209,'CONTENT','кол_листов ',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (408,1209,'CONTENT','номера_стр',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (409,1209,'CONTENT','примечание',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (500,1220,'HEADER','Марка кабеля',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (501,1220,'HEADER','Длина кабеля (всего) в м.',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (502,1220,'HEADER','Оптическая длина в м.',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (503,1220,'HEADER','Информация',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (504,1220,'CONTENT','марка',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (505,1220,'CONTENT','длина_всего',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (506,1220,'CONTENT','длина_опт',NULL);
        INSERT OR IGNORE INTO "Project_content_config_table" VALUES (507,1220,'CONTENT','инфо',NULL);
        COMMIT;

        """
    )
    
    conn.commit()
    conn.close()

def traversal(id_parent_node):
    print(id_parent_node)
    childs = get_childs(id_parent_node)
    print(id_parent_node, childs)


def get_id_project_node():
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id_node FROM Project_structure_of_nodes
    WHERE type_node = "PROJECT";
    """)
    conn.commit()
    conn.close()

def get_childs(id_parent_node):
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT id_node FROM Project_structure_of_nodes
    WHERE id_parent = {id_parent_node};
    """)
    conn.commit()
    conn.close()


def main():
    osnova()
    traversal(get_id_project_node())



main()