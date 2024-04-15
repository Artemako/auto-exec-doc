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
INSERT INTO "Projects" VALUES (13,'Новая папочка с мамочкой','C:/Users/hayar/OneDrive/Документы/AutoExecDoc Projects/Новая папочка с мамочкой','2024-04-14 19:03:15','2024-04-14 19:03:15');
INSERT INTO "Templates" VALUES (0,NULL,NULL,NULL,NULL);
COMMIT;
