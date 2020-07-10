DROP TABLE IF EXISTS User;

CREATE TABLE User(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    first_name text NOT NULL,
    second_name text NOT NULL,
    username text NOT NULL UNIQUE,
    email text NOT NULL UNIQUE,
    password text NOT NULL,
    rating FLOAT NOT NULL,
    average_score FLOAT NOT NULL
);

