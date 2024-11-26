from faker import Faker
import mysql.connector
from random import uniform, choice, randint
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_DATABASE")
}

fake = Faker()

# URL fija para las imágenes
DEFAULT_BOOK_IMAGE = "https://images.cdn2.buscalibre.com/fit-in/360x360/3b/5e/3b5efaf14facaf0246cc6cd2ee086970.jpg"
DEFAULT_PROFILE_IMAGE = "https://images.unsplash.com/photo-1511367461989-f85a21fda167"

# Géneros de libros más realistas
BOOK_GENRES = [
    "Fiction", "Non-Fiction", "Mystery", "Science Fiction", 
    "Fantasy", "Romance", "Thriller", "Horror", "Biography",
    "Historical Fiction", "Young Adult", "Children's"
]

def insert_test_data():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Insertar usuarios
        user_ids = []
        for _ in range(10):
            username = fake.user_name()
            email = fake.email()
            password = "password123"  # Contraseña simple para pruebas
            latitude = uniform(-34.6690, -34.5390)  # Coordenadas de Buenos Aires
            longitude = uniform(-58.5317, -58.3539)
            
            cursor.execute(
                """INSERT INTO Users 
                (username, email, password, profile_photo, latitude, longitude, created_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (username, email, password, DEFAULT_PROFILE_IMAGE, latitude, longitude, 
                 fake.date_time_between(start_date='-1y', end_date='now'))
            )
            user_ids.append(cursor.lastrowid)

        # Insertar libros
        book_ids = []
        for _ in range(20):
            name = fake.catch_phrase()
            author = fake.name()
            description = fake.paragraph(nb_sentences=3)
            availability_status = choice([True, False])
            genre = choice(BOOK_GENRES)
            owner_id = choice(user_ids)
            
            cursor.execute(
                """INSERT INTO Books 
                (name, author, photo, description, availability_status, genre, owner_id, created_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (name, author, DEFAULT_BOOK_IMAGE, description, availability_status, 
                 genre, owner_id, fake.date_time_between(start_date='-6m', end_date='now'))
            )
            book_ids.append(cursor.lastrowid)

        # Insertar comentarios de usuarios
        for _ in range(30):
            commenter_id = choice(user_ids)
            receiver_id = choice([u for u in user_ids if u != commenter_id])
            comment = fake.paragraph(nb_sentences=2)
            
            cursor.execute(
                """INSERT INTO UserComments 
                (commenter_id, receiver_id, comment, created_at) 
                VALUES (%s, %s, %s, %s)""",
                (commenter_id, receiver_id, comment, 
                 fake.date_time_between(start_date='-3m', end_date='now'))
            )

        # Insertar calificaciones de usuarios
        for _ in range(25):
            rater_id = choice(user_ids)
            rated_user_id = choice([u for u in user_ids if u != rater_id])
            rating = randint(1, 5)
            
            try:
                cursor.execute(
                    """INSERT INTO UserRatings 
                    (rater_id, rated_user_id, rating, created_at) 
                    VALUES (%s, %s, %s, %s)""",
                    (rater_id, rated_user_id, rating, 
                     fake.date_time_between(start_date='-3m', end_date='now'))
                )
            except mysql.connector.Error:
                continue  # Ignorar si ya existe la calificación

        # Insertar calificaciones de libros
        for _ in range(40):
            book_id = choice(book_ids)
            rater_id = choice(user_ids)
            rating = randint(1, 5)
            
            try:
                cursor.execute(
                    """INSERT INTO BookRatings 
                    (book_id, rater_id, rating, created_at) 
                    VALUES (%s, %s, %s, %s)""",
                    (book_id, rater_id, rating, 
                     fake.date_time_between(start_date='-3m', end_date='now'))
                )
            except mysql.connector.Error:
                continue  # Ignorar si ya existe la calificación

        # Insertar intercambios de libros
        for _ in range(15):
            book_id = choice(book_ids)
            requester_id = choice(user_ids)
            
            # Obtener el owner_id del libro
            cursor.execute("SELECT owner_id FROM Books WHERE id = %s", (book_id,))
            owner_id = cursor.fetchone()[0]
            
            if requester_id != owner_id:  # Evitar auto-intercambios
                status = choice(['pending', 'accepted', 'rejected', 'completed'])
                created_at = fake.date_time_between(start_date='-2m', end_date='now')
                
                cursor.execute(
                    """INSERT INTO BookExchanges 
                    (book_id, requester_id, owner_id, status, created_at, updated_at) 
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                    (book_id, requester_id, owner_id, status, created_at, 
                     created_at + timedelta(days=randint(1, 14)))
                )

        connection.commit()
        print("Datos de prueba insertados exitosamente.")

    except mysql.connector.Error as e:
        print(f"Error al insertar datos de prueba: {e}")
        connection.rollback()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    insert_test_data()
