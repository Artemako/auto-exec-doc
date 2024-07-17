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
INSERT INTO "Settings" VALUES (1,'app_converter','LIBREOFFICE');
COMMIT;
