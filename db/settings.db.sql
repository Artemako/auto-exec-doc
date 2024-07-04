BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Projects" (
	"id_project"	INTEGER NOT NULL UNIQUE,
	"name_project"	TEXT NOT NULL,
	"directory_project"	TEXT NOT NULL,
	"date_create_project"	TEXT NOT NULL,
	"date_last_open_project"	TEXT NOT NULL,
	PRIMARY KEY("id_project" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Templates" (
	"id_template"	INTEGER UNIQUE,
	"name_template"	TEXT,
	"form_template"	TEXT,
	"date_create_template"	TEXT,
	"date_edit_template"	TEXT,
	PRIMARY KEY("id_template" AUTOINCREMENT)
);
INSERT INTO "Projects" VALUES (114,'Пример','C:/Users/hayar/OneDrive/Документы/AutoExecDoc Projects/Пример','2024-04-25 18:20:31','2024-04-25 18:21:32');
INSERT INTO "Projects" VALUES (115,'Новосергеевка','C:/Users/hayar/OneDrive/Рабочий стол/Новосергеевка','2024-04-25 18:28:37','2024-04-25 18:28:37');
INSERT INTO "Projects" VALUES (116,'мсисми','C:/Users/hayar/OneDrive/Документы/AutoExecDoc Projects/мсисми','2024-04-25 18:29:46','2024-04-25 18:29:46');
INSERT INTO "Projects" VALUES (117,'Новая папка','C:/Users/hayar/OneDrive/Документы/AutoExecDoc Projects/Новая папка','2024-04-25 19:30:38','2024-04-25 20:21:07');
INSERT INTO "Projects" VALUES (118,'Привет Андрей','C:/Users/hayar/OneDrive/Документы/AutoExecDoc Projects/Привет Андрей','2024-04-27 17:20:35','2024-04-27 18:04:40');
INSERT INTO "Projects" VALUES (119,'общая папка','D:/общая папка','2024-05-11 02:20:12','2024-05-11 02:20:12');
INSERT INTO "Projects" VALUES (120,'Новосергеевка','D:/общая папка/Новосергеевка','2024-05-11 02:21:04','2024-05-13 10:52:51');
INSERT INTO "Projects" VALUES (121,'vxcvxv','C:/Users/hayar/Documents/AutoExecDoc Projects/vxcvxv','2024-05-12 00:21:02','2024-05-12 00:21:02');
INSERT INTO "Projects" VALUES (122,'fsdfs','C:/Users/hayar/Documents/AutoExecDoc Projects/fsdfs','2024-05-12 00:30:19','2024-05-12 00:41:32');
INSERT INTO "Projects" VALUES (123,'Новосергеевка','C:/Users/hayar/Documents/AutoExecDoc Projects/Новосергеевка','2024-05-12 00:43:26','2024-05-12 00:43:26');
INSERT INTO "Projects" VALUES (124,'Новосергеевка','C:/Users/hayar/Documents/AutoExecDoc Projects/Новосергеевка','2024-05-12 00:44:37','2024-05-12 00:44:37');
INSERT INTO "Projects" VALUES (125,'Привет','C:/Users/hayar/Documents/AutoExecDoc Projects/Привет','2024-07-03 19:41:14','2024-07-03 19:49:13');
INSERT INTO "Templates" VALUES (0,NULL,NULL,NULL,NULL);
COMMIT;
