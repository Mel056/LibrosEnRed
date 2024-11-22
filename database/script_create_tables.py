import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "test",  # Cambiar si se usa un usuario diferente
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_users_table)

        create_books_table = """
        CREATE TABLE IF NOT EXISTS Books (
            id_books INT AUTO_INCREMENT PRIMARY KEY,
            name_book VARCHAR(150) NOT NULL,
            author VARCHAR(100),
            photo VARCHAR(255),
            descripcion TEXT,
            status ENUM('disponible', 'prestado', 'reservado') DEFAULT 'disponible',
            genre VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_books_table)

        print("Base de datos y tablas creadas exitosamente.")

    except mysql.connector.Error as e:
        print(f"Error al crear la base de datos o tablas: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    create_database_and_tables()
