BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Projects" (
	"id_project"	INTEGER NOT NULL UNIQUE,
	"name_project"	TEXT NOT NULL,
	"directory_project"	TEXT NOT NULL,
	"date_create_project"	TEXT NOT NULL,
	"date_last_open_project"	TEXT NOT NULL,
	PRIMARY KEY("id_project" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Settings" (
	"id_setting"	INTEGER NOT NULL UNIQUE,
	"name_setting"	TEXT NOT NULL UNIQUE,
	"value_setting"	TEXT,
	PRIMARY KEY("id_setting" AUTOINCREMENT)
);
INSERT INTO "Projects" VALUES (20,'gdgffdg','C:/Users/hayar/Documents/AutoExecDoc Projects/gdgffdg','2024-08-10 16:36:35','2024-08-10 16:54:21');
INSERT INTO "Projects" VALUES (21,'dsdf','C:/Users/hayar/Documents/AutoExecDoc Projects/dsdf','2024-08-10 16:57:31','2024-08-10 21:16:56');
INSERT INTO "Settings" VALUES (1,'app_converter','LIBREOFFICE');
INSERT INTO "Settings" VALUES (2,'libreoffice_path','C:\Program Files\LibreOffice\program\soffice.exe');
INSERT INTO "Settings" VALUES (3,'project_current_name',NULL);
COMMIT;
