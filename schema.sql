CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS collection (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    player_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    strategy INTEGER,
    theme INTEGER,
    ease INTEGER,
    replay INTEGER,
    length INTEGER,
    aesthetics INTEGER,
    interaction INTEGER,
    best INTEGER,
    fun INTEGER,
    score REAL,
    notes TEXT,
    FOREIGN KEY(player_id) REFERENCES users(id)
);