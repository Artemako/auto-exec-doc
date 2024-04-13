BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Projects" (
	"id_project"	INTEGER NOT NULL UNIQUE,
	"name_project"	TEXT NOT NULL,
	"directory_project"	TEXT NOT NULL,
	"date_create_project"	TEXT NOT NULL,
	"date_last_open_project"	TEXT NOT NULL,
	PRIMARY KEY("id_project" AUTOINCREMENT)
);
INSERT INTO "Projects" VALUES (6,'FFFFF','C:/Users/hayar/OneDrive/Документы/AutoExecDoc Projects/FFFFF','2024-04-13 22:26:49','2024-04-13 22:26:49');
INSERT INTO "Projects" VALUES (7,'dfghjk','C:/Users/hayar/OneDrive/Документы/AutoExecDoc Projects/dfghjk','2024-04-13 22:27:14','2024-04-13 22:27:14');
INSERT INTO "Projects" VALUES (8,'gfdfgdf','C:/Users/hayar/OneDrive/Документы/AutoExecDoc Projects/gfdfgdf','2024-04-13 22:46:12','2024-04-13 22:46:12');
INSERT INTO "Projects" VALUES (9,'ЗАЗЗАЗАЗ','C:/Users/hayar/OneDrive/Документы/AutoExecDoc Projects/ЗАЗЗАЗАЗ','2024-04-13 22:48:44','2024-04-13 22:49:23');
COMMIT;
