CREATE TABLE "Yhtiö" (
  "Id"               INTEGER PRIMARY KEY,
  "Nimi"             TEXT NOT NULL,
  "Kirjanpitotunnus" TEXT NOT NULL UNIQUE
);

CREATE TABLE "Kustannuspaikka" (
  "Id"   INTEGER PRIMARY KEY,
  "Nimi" TEXT NOT NULL UNIQUE
);

CREATE TABLE "TOT" (
  "Id"                         INTEGER PRIMARY KEY AUTOINCREMENT,
  "Yhtiötunnus"                INTEGER REFERENCES "Yhtiö" ("Id"),
  "Vuosikuukausi"              TEXT NOT NULL,   -- ISO date, first day of month
  "Tilin numero"               INTEGER,
  "Kustannuspaikka"            INTEGER REFERENCES "Kustannuspaikka" ("Id"),
  "Konsernikustannuspaikka"    INTEGER REFERENCES "Kustannuspaikka" ("Id"),
  "Summa_snt"                  INTEGER NOT NULL, -- euros * 100
  "Vyörytetty kustannuspaikka" INTEGER REFERENCES "Kustannuspaikka" ("Id")
);

CREATE TABLE "Kustannuspaikkahierarkia" (
    "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Kustannuspaikka" TEXT NOT NULL,
    "Emokustannuspaikka" TEXT,
    "Voimassa alkaen" TEXT NOT NULL
);

-- Store a history of changes made to the current TOT data.
-- Each record represents an insertion, update or deletion.
CREATE TABLE "TOT_Muutoshistoria" (
    "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "TOT_Id" INTEGER NOT NULL,
    "Muutos" TEXT NOT NULL CHECK ("Muutos" IN ('INSERT', 'UPDATE', 'DELETE')),
    "Muutosaika" TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "Vanha_summa_snt" INTEGER,
    "Uusi_summa_snt" INTEGER
);

-- Speed up lookups of hierarchy relationships by cost centre and
-- effective start date which are commonly used when traversing history.
CREATE INDEX "idx_kustannuspaikkahierarkia_haku"
ON "Kustannuspaikkahierarkia" (
    "Kustannuspaikka",
    "Voimassa alkaen"
);

CREATE INDEX "TOT_Yhtiötunnus"                ON "TOT" ("Yhtiötunnus");
CREATE INDEX "TOT_Vuosikuukausi"              ON "TOT" ("Vuosikuukausi");
CREATE INDEX "TOT_Tilin numero"               ON "TOT" ("Tilin numero");
CREATE INDEX "TOT_Kustannuspaikka"            ON "TOT" ("Kustannuspaikka");
CREATE INDEX "TOT_Konsernikustannuspaikka"    ON "TOT" ("Konsernikustannuspaikka");
CREATE INDEX "TOT_Vyörytetty kustannuspaikka" ON "TOT" ("Vyörytetty kustannuspaikka");
