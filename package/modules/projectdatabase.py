import sqlite3
import os

import package.modules.dirpathsmanager as dirpathsmanager


class Database:
    con_db_project = None

    def __init__(self):
        pass

    @staticmethod
    def create_and_config_db():
        """
        Настройка базы данных перед использованием проекта
        """
        if not os.path.exists(dirpathsmanager.DirPathManager.get_db_project_dirpath()):
            # Добавляем данные в пустую БД
            Database.con_db_project = sqlite3.connect(
                dirpathsmanager.DirPathManager.get_db_project_dirpath()
            )
            Database.add_tables_and_datas_to_empty_db_project()
        else:
            Database.con_db_project = sqlite3.connect(
                dirpathsmanager.DirPathManager.get_db_project_dirpath()
            )

    @staticmethod
    def add_tables_and_datas_to_empty_db_project():
        """
        Добавление таблиц и данных в БД программы при запуске.
        """
        cursor = Database.con_db_project.cursor()
        cursor.executescript(
            """
            BEGIN TRANSACTION;
            CREATE TABLE IF NOT EXISTS "Project_content_list" (
                "id_content"	INTEGER NOT NULL UNIQUE,
                "name_content"	TEXT NOT NULL UNIQUE,
                "type_content"	TEXT NOT NULL,
                "note_content"	TEXT,
                PRIMARY KEY("id_content" AUTOINCREMENT)
            );
            CREATE TABLE IF NOT EXISTS "Project_structure_of_nodes" (
                "id_node"	INTEGER NOT NULL UNIQUE,
                "name_node"	TEXT,
                "id_parent"	INTEGER,Ц
                "type_node"	TEXT NOT NULL,
                "id_left"	INTEGER,
                "id_right"	INTEGER,
                "template_name"	TEXT,
                PRIMARY KEY("id_node" AUTOINCREMENT)
            );
            INSERT INTO "Project_content_list" VALUES (1000,'организационно_правовая_форма','TEXT',NULL);
            INSERT INTO "Project_content_list" VALUES (1001,'название_компании','TEXT',NULL);
            INSERT INTO "Project_content_list" VALUES (1002,'адрес_компании','TEXT',NULL);
            INSERT INTO "Project_content_list" VALUES (1003,'название_объекта','TEXT',NULL);
            INSERT INTO "Project_content_list" VALUES (1004,'участок','TEXT',NULL);
            INSERT INTO "Project_content_list" VALUES (1005,'номер_кабеля','TEXT',NULL);
            INSERT INTO "Project_content_list" VALUES (1006,'заказчик','TEXT',NULL);
            INSERT INTO "Project_content_list" VALUES (1007,'строительно_монтажная_организация','TEXT',NULL);
            INSERT INTO "Project_content_list" VALUES (1008,'город','TEXT',NULL);
            INSERT INTO "Project_content_list" VALUES (1009,'год','DATE','YEAR');
            INSERT INTO "Project_content_list" VALUES (1100,'инж_про_ком','TEXT',NULL);
            INSERT INTO "Project_content_list" VALUES (1101,'инж_про_ком_фио','TEXT',NULL);
            INSERT INTO "Project_content_list" VALUES (1102,'гла_инж_компания','TEXT',NULL);
            INSERT INTO "Project_content_list" VALUES (1103,'гла_инж_фио','TEXT',NULL);
            INSERT INTO "Project_structure_of_nodes" VALUES (0,'Проект',NULL,'PROJECT',NULL,NULL,'');
            INSERT INTO "Project_structure_of_nodes" VALUES (10,'Титульный лист',0,'FORM',NULL,11,'main');
            INSERT INTO "Project_structure_of_nodes" VALUES (11,'Реестр документации',0,'FORM',10,12,'main');
            INSERT INTO "Project_structure_of_nodes" VALUES (12,'Паспорт трассы',0,'GROUP',11,NULL,NULL);
            INSERT INTO "Project_structure_of_nodes" VALUES (1201,'ПТ-1',12,'FORM',NULL,1202,'main');
            INSERT INTO "Project_structure_of_nodes" VALUES (1202,'ПТ-2',12,'FORM',1201,1203,'main');
            INSERT INTO "Project_structure_of_nodes" VALUES (1203,'ПТ-3',12,'FORM',1202,1204,'main');
            INSERT INTO "Project_structure_of_nodes" VALUES (1204,'ПТ-4',12,'FORM',1203,1205,'main');
            INSERT INTO "Project_structure_of_nodes" VALUES (1205,'ПТ-5',12,'FORM',1204,1206,'main');
            INSERT INTO "Project_structure_of_nodes" VALUES (1206,'ПТ-6',12,'FORM',1205,1207,'main');
            INSERT INTO "Project_structure_of_nodes" VALUES (1207,'ПТ-7',12,'FORM',1206,1208,'main');
            INSERT INTO "Project_structure_of_nodes" VALUES (1208,'ПТ-8',12,'FORM',1207,1209,'main');
            INSERT INTO "Project_structure_of_nodes" VALUES (1209,'ПТ-9',12,'FORM',1208,1210,'main');
            INSERT INTO "Project_structure_of_nodes" VALUES (1210,'ПТ-10',12,'FORM',1209,1211,'main');
            INSERT INTO "Project_structure_of_nodes" VALUES (1211,'ПТ-11',12,'FORM',1210,1212,'main');
            INSERT INTO "Project_structure_of_nodes" VALUES (1212,'ПТ-12',12,'FORM',1211,1213,'main');
            INSERT INTO "Project_structure_of_nodes" VALUES (1213,'ПТ-13',12,'FORM',1212,1214,'main');
            INSERT INTO "Project_structure_of_nodes" VALUES (1214,'ПТ-14',12,'FORM',1213,1215,'main');
            INSERT INTO "Project_structure_of_nodes" VALUES (1215,'ПТ-15',12,'FORM',1214,1216,'main');
            INSERT INTO "Project_structure_of_nodes" VALUES (1216,'ПТ-16',12,'FORM',1215,NULL,'main');
            COMMIT;
            """
        )
