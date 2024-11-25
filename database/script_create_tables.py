import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "nacho",  # Cambiar si se usa un usuario diferente
    "password": "123",  # Cambiar si se usa una contraseña diferente
}

def create_database_and_tables():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS LibrosEnRed")
        cursor.execute("USE LibrosEnRed")

        create_users_table = """
        CREATE TABLE IF NOT EXISTS Users (
            id_users INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            email VARCHAR(150) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            profile_photo VARCHAR(255),
            latitude DECIMAL(9,6),
            longitude DECIMAL(9,6),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_users_table)

        create_books_table = """
        CREATE TABLE IF NOT EXISTS Books (
            id_books INT AUTO_INCREMENT PRIMARY KEY,
            name_book VARCHAR(150) NOT NULL,
            author VARCHAR(100),
            photo VARCHAR(255),
            descripcion TEXT,
            status BOOLEAN DEFAULT FALSE,
            genre VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_books_table)
        
        create_exchange_table = """
        CREATE TABLE IF NOT EXISTS Book_Exchange (
            id_exchange INT AUTO_INCREMENT PRIMARY KEY,
            book_id INT NOT NULL,
            user_1 INT NOT NULL,
            user_2 INT NOT NULL,
            exchange_status BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (book_id) REFERENCES Books(id_books),
            FOREIGN KEY (user_1) REFERENCES Users(id_users),
            FOREIGN KEY (user_2) REFERENCES Users(id_users)
        )
        """
        cursor.execute(create_exchange_table)

        create_comments_table = """
        CREATE TABLE IF NOT EXISTS Comments (
            id_comments INT AUTO_INCREMENT PRIMARY KEY,
            id_users INT NOT NULL,
            comments TEXT,
            FOREIGN KEY (id_users) REFERENCES Users(id_users)
        )
        """
        cursor.execute(create_comments_table)
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    create_database_and_tables()
