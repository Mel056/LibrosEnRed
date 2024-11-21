from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

engine = create_engine("mysql+mysqlconnector://root@localhost:3308/LibrosEnREd")

def run_query(query, parameters=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), parameters)
        conn.commit()

    return result

def new_user(username, email, password, profile_photo):
    return run_query(
        "INSERT INTO Users (username, email, password, profile_photo) VALUES (username, email, password, profile_photo)"
    ).fetchall()

def login(user_id):
    ""

def get_user(user_id):
    return run_query(
        "SELECT username, email FROM Users WHERE id_users = user_id"
    ).fetchall()

def get_all_users():
    return run_query(
        "SELECT username, email FROM Users"
    )

def update_user(user_id, username, email, password, profile_photo):
   return run_query(
       "UPDATE Users SET username = username, email = email, password = password, porfile_photo = profile_photo, WHERE id_users = user_id"
   )

def delete_user(user_id):
    return run_query(
        "DELETE FROM Users WHERE id_users = user_id"
    )

def new_book(book_id, name_book, author, photo, descripcion, status, genre):
    return run_query(
        "INSERT INTO Books (name_book, author, photo, descripcion, status, genre) VALUES (name_book = name_book, author = author, photo = photo, descripcion = descripcion, status = status, genre = genre)"
    )

def get_book(book_id):
    return run_query(
        "SELECT name_book, author, owner FROM Books WHERE id_books = book_id"
    ).fetchall()

def get_book_by_genre(book_genre):
    return run_query(
        "SELECT name_book, author, owner FROM Books WHERE genre = book_genre"
    ).fetchall()

def get_all_books():
    return run_query(
        "SELECT name_book, author, owner FROM Books"
    ).fetchall()

def update_book(book_id, name_book, author, photo, descripcion, status, genre):
    return run_query(
       "UPDATE Books SET name_book = name_book, author = author, photo = photo, descripcion = descripcion, status = status, genre = genre, WHERE id_books = book_id"
    )

def delete_book(book_id):
    return run_query(
        "DELETE FROM Books WHERE id_books = book_id"
    )