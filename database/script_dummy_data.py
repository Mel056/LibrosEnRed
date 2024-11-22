from faker import Faker
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "test", # Cambiar si se usa un usuario diferente
    "password": "123", # Cambiar si se usa un usuario diferente
    "database": "LibrosEnRed"
}

fake = Faker()

def insert_test_data():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Insertar usuarios
        for _ in range(3):
            username = fake.user_name()
            email = fake.email()
            password = fake.password(length=12)
            profile_photo = fake.image_url()
            cursor.execute(
                "INSERT INTO Users (username, email, password, profile_photo) VALUES (%s, %s, %s, %s)",
                (username, email, password, profile_photo)
            )

        # Insertar libros
        for _ in range(10):
            name_book = fake.catch_phrase()
            author = fake.name()
            photo = fake.image_url()
            descripcion = fake.paragraph(nb_sentences=3)
            status = fake.random_element(elements=["disponible", "prestado", "reservado"])
            genre = fake.random_element(elements=["Ficción", "No Ficción", "Ciencia Ficción", "Fantasía", "Historia"])
            cursor.execute(
                "INSERT INTO Books (name_book, author, photo, descripcion, status, genre) VALUES (%s, %s, %s, %s, %s, %s)",
                (name_book, author, photo, descripcion, status, genre)
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
