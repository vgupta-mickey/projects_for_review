CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR  UNIQUE,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER  NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE,
    password VARCHAR NOT NULL); 

CREATE TABLE bookreviews (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books,
    user_id INTEGER REFERENCES users,
    rating  INTEGER CHECK (rating > 0 AND RATING <= 5),
    review  VARCHAR);
