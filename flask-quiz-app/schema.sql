DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Rating;

CREATE TABLE User(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    first_name text NOT NULL,
    second_name text NOT NULL,
    username text NOT NULL UNIQUE,
    email text NOT NULL UNIQUE,
    password text NOT NULL,
    rating INTEGER,
    FOREIGN KEY (rating) REFERENCES Rating (id)
);

CREATE TABLE Rating(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    battles_number INTEGER,
    correct_answers INTEGER,
    wrong_answers INTEGER,
    correct_percent FLOAT,
    rating_value FLOAT
);
