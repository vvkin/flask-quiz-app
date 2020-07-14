DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Rating;

CREATE TABLE User(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    full_name text NOT NULL,
    username text NOT NULL UNIQUE,
    email text NOT NULL UNIQUE,
    password text NOT NULL,
    rating INTEGER,
    FOREIGN KEY (rating) REFERENCES Rating (id)
);

CREATE TABLE Rating(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    battles_number INTEGER DEFAULT 0,
    correct_answers INTEGER DEFAULT 0,
    wrong_answers INTEGER DEFAULT 0,
    correct_percent FLOAT DEFAULT 0
);
