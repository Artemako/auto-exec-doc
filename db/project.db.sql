BEGIN TRANSACTION;
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
CREATE TABLE IF NOT EXISTS "Project_nodes_data" (
	"id_pair"	INTEGER UNIQUE,
	"id_node"	INTEGER,
	"id_content"	INTEGER,
	"value"	TEXT,
	FOREIGN KEY("id_content") REFERENCES "Project_content_config_list"("id_content"),
	FOREIGN KEY("id_node") REFERENCES "Project_nodes"("id_node"),
	PRIMARY KEY("id_pair" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Project_pages_data" (
	"id_pair"	INTEGER UNIQUE,
	"id_page"	INTEGER,
	"id_content"	INTEGER,
	"value"	TEXT,
	FOREIGN KEY("id_page") REFERENCES "Project_pages"("id_page"),
	FOREIGN KEY("id_content") REFERENCES "Project_content_config_list"("id_content"),
	PRIMARY KEY("id_pair" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Project_nodes" (
	"id_node"	INTEGER NOT NULL UNIQUE,
	"name_node"	TEXT,
	"id_parent"	INTEGER,
	"order_node"	TEXT,
	"type_node"	TEXT,
	"template_name"	TEXT,
	"included"	TEXT DEFAULT 'True',
	PRIMARY KEY("id_node" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Project_pages" (
	"id_page"	INTEGER NOT NULL UNIQUE,
	"id_node_parent"	INTEGER,
	"page_name"	TEXT,
	"template_name"	TEXT,
	"page_order"	INTEGER,
	"included"	TEXT DEFAULT 'True',
	PRIMARY KEY("id_page" AUTOINCREMENT)
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
INSERT INTO "Project_nodes_data" VALUES (100,0,1003,NULL);
INSERT INTO "Project_nodes_data" VALUES (101,0,1004,NULL);
INSERT INTO "Project_nodes_data" VALUES (102,0,1001,NULL);
INSERT INTO "Project_nodes_data" VALUES (1000,NULL,NULL,NULL);
INSERT INTO "Project_nodes_data" VALUES (1001,10,1002,NULL);
INSERT INTO "Project_nodes_data" VALUES (1002,10,1003,NULL);
INSERT INTO "Project_nodes_data" VALUES (1003,10,1004,NULL);
INSERT INTO "Project_nodes_data" VALUES (1004,10,1005,NULL);
INSERT INTO "Project_nodes_data" VALUES (1005,10,1006,NULL);
INSERT INTO "Project_nodes_data" VALUES (1110,10,NULL,NULL);
INSERT INTO "Project_pages_data" VALUES (100,10,1007,NULL);
INSERT INTO "Project_pages_data" VALUES (101,10,1008,NULL);
INSERT INTO "Project_pages_data" VALUES (102,10,1009,NULL);
INSERT INTO "Project_pages_data" VALUES (200,NULL,NULL,NULL);
INSERT INTO "Project_pages_data" VALUES (201,11,1101,NULL);
INSERT INTO "Project_pages_data" VALUES (202,11,1102,NULL);
INSERT INTO "Project_pages_data" VALUES (203,11,1103,NULL);
INSERT INTO "Project_pages_data" VALUES (300,NULL,NULL,NULL);
INSERT INTO "Project_pages_data" VALUES (301,NULL,NULL,NULL);
INSERT INTO "Project_pages_data" VALUES (302,20,1202,NULL);
INSERT INTO "Project_pages_data" VALUES (400,NULL,NULL,NULL);
INSERT INTO "Project_pages_data" VALUES (500,NULL,NULL,NULL);
INSERT INTO "Project_pages_data" VALUES (501,40,1225,NULL);
INSERT INTO "Project_pages_data" VALUES (502,40,1226,NULL);
INSERT INTO "Project_pages_data" VALUES (503,40,1227,NULL);
INSERT INTO "Project_pages_data" VALUES (504,40,1228,NULL);
INSERT INTO "Project_pages_data" VALUES (505,40,1229,NULL);
INSERT INTO "Project_pages_data" VALUES (600,NULL,NULL,NULL);
INSERT INTO "Project_nodes" VALUES (0,'Проект',NULL,'0','PROJECT',NULL,NULL);
INSERT INTO "Project_nodes" VALUES (10,'Титульный лист',0,'1','FORM','main','1');
INSERT INTO "Project_nodes" VALUES (11,'Реестр документации',0,'2','FORM','main','1');
INSERT INTO "Project_nodes" VALUES (12,'Паспорт трассы',0,'3','GROUP',NULL,'1');
INSERT INTO "Project_nodes" VALUES (1201,'ПТ-1',12,'1','FORM','main','1');
INSERT INTO "Project_nodes" VALUES (1202,'ПТ-2',12,'2','FORM','main','1');
INSERT INTO "Project_nodes" VALUES (1203,'ПТ-3',12,'3','FORM','main','1');
INSERT INTO "Project_pages" VALUES (10,10,'Л.1. Титульный лист.','1-ТЛ-1',1,NULL);
INSERT INTO "Project_pages" VALUES (11,10,'Л.2. Титульный лист.','1-ТЛ-2',2,NULL);
INSERT INTO "Project_pages" VALUES (20,11,'Л.1. Реестр исполнительной документации ВОЛС.','2-РД-1',1,NULL);
INSERT INTO "Project_pages" VALUES (30,1201,'Л.1. Паспорт трассы. Опись документов.','3-ПТ1-1',1,NULL);
INSERT INTO "Project_pages" VALUES (40,1202,'Л.1. Паспорт трассы волоконно-оптической линии связи на участке.','3-ПТ2-1',1,NULL);
INSERT INTO "Project_pages" VALUES (50,1203,'Л.1. Скелетная схема ВОЛП и основные данные цепей кабеля.','3-ПТ3-1',1,NULL);
COMMIT;
