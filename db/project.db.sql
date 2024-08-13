BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Project_documents" (
	"id_docx"	INTEGER NOT NULL UNIQUE,
	"name_docx"	TEXT,
	"filename_docx"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_docx" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Project_nodes" (
	"id_node"	INTEGER NOT NULL UNIQUE,
	"name_node"	TEXT UNIQUE,
	"id_parent"	INTEGER,
	"order_node"	TEXT NOT NULL,
	"type_node"	TEXT,
	"id_active_template"	INTEGER,
	"included"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("id_node" AUTOINCREMENT),
	FOREIGN KEY("id_active_template") REFERENCES "Project_templates"("id_template")
);
CREATE TABLE IF NOT EXISTS "Project_nodes_data" (
	"id_pair"	INTEGER NOT NULL UNIQUE,
	"id_node"	INTEGER NOT NULL,
	"id_tag"	INTEGER NOT NULL,
	"name_tag"	TEXT,
	"value"	TEXT,
	PRIMARY KEY("id_pair" AUTOINCREMENT),
	FOREIGN KEY("id_node") REFERENCES "Project_nodes"("id_node"),
	FOREIGN KEY("id_tag") REFERENCES "Project_tags"("id_tag")
);
CREATE TABLE IF NOT EXISTS "Project_pages" (
	"id_page"	INTEGER NOT NULL UNIQUE,
	"id_parent_template"	INTEGER,
	"name_page"	TEXT UNIQUE,
	"filename_page"	TEXT UNIQUE,
	"order_page"	INTEGER NOT NULL,
	"included"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("id_page" AUTOINCREMENT),
	FOREIGN KEY("id_parent_template") REFERENCES "Project_templates"("id_template")
);
CREATE TABLE IF NOT EXISTS "Project_pages_data" (
	"id_pair"	INTEGER NOT NULL UNIQUE,
	"id_page"	INTEGER NOT NULL,
	"id_tag"	INTEGER NOT NULL,
	"name_tag"	TEXT,
	"value"	TEXT,
	PRIMARY KEY("id_pair" AUTOINCREMENT),
	FOREIGN KEY("id_page") REFERENCES "Project_pages"("id_page"),
	FOREIGN KEY("id_tag") REFERENCES "Project_tags"("id_tag")
);
CREATE TABLE IF NOT EXISTS "Project_tags" (
	"id_tag"	INTEGER NOT NULL UNIQUE,
	"name_tag"	TEXT NOT NULL UNIQUE,
	"type_tag"	TEXT NOT NULL,
	"title_tag"	TEXT,
	"order_tag"	INTEGER NOT NULL,
	"config_tag"	TEXT,
	"description_tag"	TEXT,
	"is_global"	INTEGER,
	PRIMARY KEY("id_tag" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Project_templates" (
	"id_template"	INTEGER NOT NULL UNIQUE,
	"name_template"	TEXT,
	"id_parent_node"	INTEGER,
	PRIMARY KEY("id_template" AUTOINCREMENT),
	FOREIGN KEY("id_parent_node") REFERENCES "Project_nodes"("id_node")
);
CREATE TABLE IF NOT EXISTS "Project_templates_data" (
	"id_pair"	INTEGER NOT NULL UNIQUE,
	"id_template"	INTEGER NOT NULL,
	"id_tag"	INTEGER NOT NULL,
	"name_tag"	TEXT,
	"value"	TEXT,
	PRIMARY KEY("id_pair" AUTOINCREMENT),
	FOREIGN KEY("id_tag") REFERENCES "Project_tags"("id_tag"),
	FOREIGN KEY("id_template") REFERENCES "Project_templates"("id_template")
);
INSERT INTO "Project_documents" VALUES (110,NULL,'');
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
INSERT INTO "Project_tags" VALUES (1000,'организационно_правовая_форма','TEXT','Организационно-правовая форма',0,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1001,'название_компании','TEXT','Название компании',1,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1002,'адрес_компании','TEXT','Адрес компании',2,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1003,'название_объекта','TEXT','Название объекта',3,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1004,'участок','TEXT','Участок',4,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1005,'номер_кабеля','TEXT','Номер кабеля',5,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1006,'заказчик','TEXT','Заказчик',6,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1007,'строительно_монтажная_организация','TEXT','Строительно-монтажная организация',7,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1008,'город','TEXT','Город',8,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1009,'год','DATE','Год',9,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1100,'инж_про_ком','TEXT','Компания инженера-проектировщика',10,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1101,'инж_про_ком_фио','TEXT','ФИО инженера-проектировщика',11,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1102,'гла_инж_компания','TEXT','Компания главного инженера',12,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1103,'гла_инж_фио','TEXT','ФИО главного инженера',13,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1200,'реестр_ид_паспорт_трассы','TABLE','Реестр ИД ВОЛС. Паспорт трассы',14,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1201,'реестр_ид_эл_паспорт_трассы','TABLE','Реестр ИД ВОЛС. Электрический паспорт трассы',15,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1202,'рабочая_документация','TABLE','Реестр ИД ВОЛС. Рабочая документация',16,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1208,'дата','DATE','Дата',17,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1209,'пт_опись_документов','TABLE','Паспорт трассы. Опись документов.',18,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1220,'кабеля','TABLE','Кабеля.',19,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1225,'общая_физ_длина','TEXT','Общая физическая длина',20,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1226,'общая_опт_длина','TEXT','Общая оптическая длина',21,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1227,'год_прокладки_кабеля','DATE','Год прокладки кабеля',22,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1228,'год_составления_паспорта','DATE','Год составления паспорта',23,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1229,'отв_пред_орг_фио ','TEXT','ФИО ответственного представителя организации',24,NULL,NULL,0);
INSERT INTO "Project_tags" VALUES (1230,'скелетная_схема_ВОЛП','IMAGE','Скелетная схема ВОЛП',25,NULL,NULL,0);
INSERT INTO "Project_templates" VALUES (1,'main',10);
INSERT INTO "Project_templates" VALUES (2,'main',11);
INSERT INTO "Project_templates" VALUES (3,'main',1201);
INSERT INTO "Project_templates" VALUES (4,'main',1202);
INSERT INTO "Project_templates" VALUES (5,'main',1203);
COMMIT;
