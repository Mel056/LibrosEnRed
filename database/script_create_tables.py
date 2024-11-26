import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Configuración de la base de datos desde variables de entorno
DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
}

def create_database_and_tables():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Crear la base de datos si no existe
        cursor.execute("CREATE DATABASE IF NOT EXISTS LibrosEnRed")
        cursor.execute("USE LibrosEnRed")

        # Tabla de Usuarios
        create_users_table = """
        CREATE TABLE IF NOT EXISTS Users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            email VARCHAR(150) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            profile_photo VARCHAR(255),
            latitude DECIMAL(9,6),
            longitude DECIMAL(9,6),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            average_rating DECIMAL(3,2) DEFAULT 0.00,
            INDEX idx_email (email)
        );
        """
        cursor.execute(create_users_table)

        # Tabla de Comentarios de Usuario
        create_user_comments_table = """
        CREATE TABLE IF NOT EXISTS UserComments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            commenter_id INT NOT NULL,
            receiver_id INT NOT NULL,
            comment TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (commenter_id) REFERENCES Users(id) ON DELETE CASCADE,
            FOREIGN KEY (receiver_id) REFERENCES Users(id) ON DELETE CASCADE,
            INDEX idx_receiver (receiver_id)
        );
        """
        cursor.execute(create_user_comments_table)

        # Tabla de Calificaciones de Usuario
        create_user_ratings_table = """
        CREATE TABLE IF NOT EXISTS UserRatings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            rater_id INT NOT NULL,
            rated_user_id INT NOT NULL,
            rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (rater_id) REFERENCES Users(id) ON DELETE CASCADE,
            FOREIGN KEY (rated_user_id) REFERENCES Users(id) ON DELETE CASCADE,
            UNIQUE KEY unique_rating (rater_id, rated_user_id),
            INDEX idx_rated_user (rated_user_id)
        );
        """
        cursor.execute(create_user_ratings_table)

        # Tabla de Libros
        create_books_table = """
        CREATE TABLE IF NOT EXISTS Books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(150) NOT NULL,
            author VARCHAR(100) NOT NULL,
            photo VARCHAR(255),
            description TEXT,
            availability_status BOOLEAN DEFAULT TRUE,
            genre VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            owner_id INT NOT NULL,
            average_rating DECIMAL(3,2) DEFAULT 0.00,
            FOREIGN KEY (owner_id) REFERENCES Users(id) ON DELETE CASCADE,
            INDEX idx_owner (owner_id),
            INDEX idx_genre (genre)
        );
        """
        cursor.execute(create_books_table)

        # Tabla de Calificaciones de Libros
        create_book_ratings_table = """
        CREATE TABLE IF NOT EXISTS BookRatings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            book_id INT NOT NULL,
            rater_id INT NOT NULL,
            rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (book_id) REFERENCES Books(id) ON DELETE CASCADE,
            FOREIGN KEY (rater_id) REFERENCES Users(id) ON DELETE CASCADE,
            UNIQUE KEY unique_book_rating (book_id, rater_id),
            INDEX idx_book (book_id)
        );
        """
        cursor.execute(create_book_ratings_table)

        # Tabla de Intercambios de Libros
        create_book_exchanges_table = """
        CREATE TABLE IF NOT EXISTS BookExchanges (
            id INT AUTO_INCREMENT PRIMARY KEY,
            book_id INT NOT NULL,
            requester_id INT NOT NULL,
            owner_id INT NOT NULL,
            status ENUM('pending', 'accepted', 'rejected', 'completed') NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (book_id) REFERENCES Books(id) ON DELETE CASCADE,
            FOREIGN KEY (requester_id) REFERENCES Users(id) ON DELETE CASCADE,
            FOREIGN KEY (owner_id) REFERENCES Users(id) ON DELETE CASCADE,
            INDEX idx_book (book_id),
            INDEX idx_requester (requester_id),
            INDEX idx_owner (owner_id)
        );
        """
        cursor.execute(create_book_exchanges_table)

        # Trigger para actualizar el promedio de calificación de usuarios
        update_user_rating_trigger = """
        CREATE TRIGGER IF NOT EXISTS update_user_rating_after_rating
        AFTER INSERT ON UserRatings
        FOR EACH ROW
        BEGIN
            UPDATE Users 
            SET average_rating = (
                SELECT AVG(rating) 
                FROM UserRatings 
                WHERE rated_user_id = NEW.rated_user_id
            )
            WHERE id = NEW.rated_user_id;
        END;
        """
        cursor.execute(update_user_rating_trigger)

        # Trigger para actualizar el promedio de calificación de libros
        update_book_rating_trigger = """
        CREATE TRIGGER IF NOT EXISTS update_book_rating_after_rating
        AFTER INSERT ON BookRatings
        FOR EACH ROW
        BEGIN
            UPDATE Books 
            SET average_rating = (
                SELECT AVG(rating) 
                FROM BookRatings 
                WHERE book_id = NEW.book_id
            )
            WHERE id = NEW.book_id;
        END;
        """
        cursor.execute(update_book_rating_trigger)

        connection.commit()
        print("Base de datos y tablas creadas exitosamente")

    except mysql.connector.Error as error:
        print(f"Error: {error}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    create_database_and_tables()
