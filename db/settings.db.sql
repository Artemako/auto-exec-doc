BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Projects" (
	"id_project"	INTEGER NOT NULL UNIQUE,
	"name_project"	TEXT NOT NULL,
	"directory_project"	TEXT NOT NULL,
	"date_create_project"	TEXT NOT NULL,
	"date_last_open_project"	TEXT NOT NULL,
	PRIMARY KEY("id_project" AUTOINCREMENT)
);
COMMIT;
