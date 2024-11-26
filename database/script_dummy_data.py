from faker import Faker
import mysql.connector
from random import uniform, choice, randint

DB_CONFIG = {
    "host": "localhost",
    "user": "leo",
    "password": "123",
    "database": "LibrosEnRed"
}

fake = Faker()

def insert_test_data():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Insertar usuarios
        user_ids = []  # Para mantener registro de los IDs de usuarios creados
        for _ in range(5):
            username = fake.user_name()
            email = fake.email()
            password = fake.password(length=12)
            profile_photo = fake.image_url()
            # Coordenadas aproximadas para una ciudad (ajustar según necesidad)
            latitude = uniform(-90, 90)
            longitude = uniform(-180, 180)
            
            cursor.execute(
                """INSERT INTO Users 
                (username, email, password, profile_photo, latitude, longitude) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (username, email, password, profile_photo, latitude, longitude)
            )
            user_ids.append(cursor.lastrowid)

        # Insertar libros
        book_ids = []  # Para mantener registro de los IDs de libros creados
        for _ in range(10):
            name_book = fake.catch_phrase()
            author = fake.name()
            photo = fake.image_url()
            descripcion = fake.paragraph(nb_sentences=3)
            status = choice([True, False])  # True para disponible, False para no disponible
            genre = fake.random_element(elements=["Ficción", "No Ficción", "Ciencia Ficción", "Fantasía", "Historia"])
            
            cursor.execute(
                """INSERT INTO Books 
                (name_book, author, photo, descripcion, status, genre) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (name_book, author, photo, descripcion, status, genre)
            )
            book_ids.append(cursor.lastrowid)

        # Insertar intercambios de libros
        for _ in range(3):
            book_id = choice(book_ids)
            user_1 = choice(user_ids)
            # Asegurarse de que user_2 sea diferente de user_1
            user_2 = choice([u for u in user_ids if u != user_1])
            exchange_status = choice([True, False])
            
            cursor.execute(
                """INSERT INTO Book_Exchange 
                (book_id, user_1, user_2, exchange_status) 
                VALUES (%s, %s, %s, %s)""",
                (book_id, user_1, user_2, exchange_status)
            )

        # Insertar comentarios
        for _ in range(8):
            user_id = choice(user_ids)
            comment = fake.paragraph(nb_sentences=2)
            
            cursor.execute(
                """INSERT INTO Comments 
                (id_users, comments) 
                VALUES (%s, %s)""",
                (user_id, comment)
            )

        connection.commit()
        
        # Insertar puntuaciones de los usuarios
        rating = randint(1, 5)
        cursor.execute(
        """INSERT INTO Rating (id_users, rating) 
        VALUES (%s, %s)""",
        (user_id, rating)
        )
        connection.commit()
        
        # Insertar puntuacines de los libros
        book_id = choice(book_ids)  
        book_rating = randint(1, 5)
        cursor.execute(
        """INSERT INTO Rating_Books (id_book, rating)
        VALUES (%s, %s)""",
        (book_id, book_rating)
     )
        connection.commit()
        print("Datos de prueba insertados exitosamente.")

    except mysql.connector.Error as e:
        print(f"Error al insertar datos de prueba: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    insert_test_data()
