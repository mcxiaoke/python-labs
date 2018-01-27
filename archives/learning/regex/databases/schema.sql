CREATE TABLE IF NOT EXISTS actions (
  _id              INTEGER PRIMARY KEY AUTOINCREMENT,
  uid              TEXT NOT NULL,
  id               INTEGER,
  action_user      INTEGER,
  action_following INTEGER,
  action_followers INTEGER,
  action_notes     INTEGER,
  action_albums    INTEGER,
  action_movie     INTEGER,
  action_book      INTEGER,
  action_music     INTEGER,
  action_online    INTEGER,
  action_group     INTEGER,
  action_shuo      INTEGER,
  action_event     INTEGER,

  UNIQUE (uid)
    ON CONFLICT IGNORE

);

CREATE TABLE IF NOT EXISTS users (
  _id             INTEGER PRIMARY KEY AUTOINCREMENT,
  id              INTEGER NOT NULL,
  uid             TEXT    NOT NULL,
  name            TEXT    NOT NULL,
  created         DATE    NOT NULL,
  notes_count     INTEGER,
  albums_count    INTEGER,
  following_count INTEGER,
  followers_count INTEGER,
  statuses_count  INTEGER,
  avatar          TEXT    NOT NULL,
  large_avatar    TEXT    NOT NULL,
  alt             TEXT,
  signature       TEXT,
  desc            TEXT,
  loc_id          INTEGER,
  loc_name        TEXT,
  type            TEXT,
  raw_data        TEXT,

  UNIQUE (id)
    ON CONFLICT REPLACE

);

CREATE TABLE IF NOT EXISTS notes (

  _id            INTEGER PRIMARY KEY AUTOINCREMENT,
  id             INTEGER NOT NULL,
  user_id        INTEGER,
  update_time    DATE    NOT NULL,
  publish_time   DATE    NOT NULL,
  alt            TEXT    NOT NULL,
  title          TEXT    NOT NULL,
  privacy        TEXT,
  summary        TEXT,
  content        TEXT,
  recs_count     INTEGER,
  comments_count INTEGER,
  liked_count    INTEGER,
  images         TEXT,
  photos         TEXT,
  raw_data       TEXT,
  FOREIGN KEY (user_id) REFERENCES users (id),

  UNIQUE (id)
    ON CONFLICT REPLACE


);

CREATE TABLE IF NOT EXISTS albums (
  _id         INTEGER PRIMARY KEY AUTOINCREMENT,
  id          INTEGER   NOT NULL,
  user_id     INTEGER,
  created     DATE TEXT NOT NULL,
  updated     DATE TEXT NOT NULL,
  cover       TEXT      NOT NULL,
  title       TEXT      NOT NULL,
  alt         TEXT      NOT NULL,
  size        INTEGER   NOT NULL,
  desc        TEXT,
  recs_count  INTEGER,
  liked_count INTEGER,
  reply_limit BOOLEAN,
  privacy     TEXT,
  photo_order TEXT,
  raw_data    TEXT,


  FOREIGN KEY (user_id) REFERENCES users (id),
  UNIQUE (id)
    ON CONFLICT REPLACE
);
















