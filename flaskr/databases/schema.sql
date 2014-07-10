DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  tag        TEXT,
  hash       TEXT,
  title      TEXT NOT NULL,
  abstract   TEXT NOT NULL,
  text       TEXT NOT NULL,
  user_id    INTEGER,
  created_at DATE NOT NULL,
  public     BOOLEAN,
  deleted    BOOLEAN
);

DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  name       TEXT NOT NULL,
  password   TEXT NOT NULL,
  created_at DATE NOT NULL,
  created_ip TEXT NOT NULL
)