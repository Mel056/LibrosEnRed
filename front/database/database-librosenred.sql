CREATE DATABASE LibrosEnREd;
USE LibrosEnREd;

CREATE TABLE Users (
    id_users INT AUTO_INCREMENT PRIMARY KEY,
    id_books INT,
    username VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    maps VARCHAR(200) NOT NULL,
    password VARCHAR(300) NOT NULL,
    profile_photo VARCHAR(255),
FOREIGN KEY (id_books) REFERENCES Books(id_books)
);

CREATE TABLE Books (
    id_books INT AUTO_INCREMENT PRIMARY KEY,
    name_book VARCHAR(150) NOT NULL,
    owner INT,
    photo VARCHAR(255),
    description TEXT,
    status VARCHAR(250),
    genre VARCHAR(250),
FOREIGN KEY (owner) REFERENCES Users(id_users)
);