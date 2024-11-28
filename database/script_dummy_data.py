# Variables globales para ser llenadas manualmente
REAL_BOOKS = [
    {
        "title": "Don Quijote de la Mancha",
        "author": "Miguel de Cervantes",
        "description": "La historia del ingenioso hidalgo Don Quijote de la Mancha, un noble que, debido a su afición a los libros de caballería, pierde el juicio y decide hacerse caballero andante. Con su escudero Sancho Panza, vive múltiples aventuras en las que confunde la realidad con sus fantasías caballerescas.",
        "genre": "Novela Clásica"
    },
    {
        "title": "El Señor de los Anillos",
        "author": "J.R.R. Tolkien",
        "description": "Una épica historia de fantasía que sigue el viaje del hobbit Frodo Bolsón para destruir el Anillo Único, un artefacto poderoso que podría permitir al malvado Sauron dominar la Tierra Media. Junto a la Comunidad del Anillo, Frodo debe enfrentar peligros y desafíos para salvar su mundo.",
        "genre": "Fantasía"
    },
    {
        "title": "Harry Potter y la Piedra Filosofal",
        "author": "J.K. Rowling",
        "description": "El primer libro de la serie sigue a Harry Potter, un joven mago que descubre en su undécimo cumpleaños que es el hijo huérfano de dos magos y que posee poderes mágicos únicos. En la Escuela Hogwarts de Magia y Hechicería, Harry hace amigos entrañables y enfrenta peligrosas aventuras.",
        "genre": "Fantasía Juvenil"
    },
    {
        "title": "El Principito",
        "author": "Antoine de Saint-Exupéry",
        "description": "Una fábula filosófica que narra el encuentro de un piloto averiado en el desierto con un pequeño príncipe proveniente de otro planeta. A través de sus conversaciones, el libro explora temas profundos sobre la vida, el amor y la naturaleza humana.",
        "genre": "Literatura Infantil"
    },
    {
        "title": "Cien Años de Soledad",
        "author": "Gabriel García Márquez",
        "description": "La saga de la familia Buendía a través de siete generaciones en el pueblo ficticio de Macondo. Una obra maestra del realismo mágico que entrelaza lo extraordinario con lo cotidiano, explorando temas de amor, guerra, política y destino.",
        "genre": "Realismo Mágico"
    },
    {
        "title": "El Código Da Vinci",
        "author": "Dan Brown",
        "description": "Un thriller que sigue al profesor Robert Langdon en una búsqueda frenética del Santo Grial, enfrentando antiguas sociedades secretas y descubriendo conspiraciones religiosas. La trama mezcla arte, historia y religión en una aventura trepidante.",
        "genre": "Thriller"
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "description": "Una distopía que retrata un futuro totalitario donde el gobierno mantiene el poder mediante la vigilancia constante, la manipulación de la verdad y el control del pensamiento. La historia sigue a Winston Smith en su rebelión contra el sistema.",
        "genre": "Ciencia Ficción"
    },
    {
        "title": "El Alquimista",
        "author": "Paulo Coelho",
        "description": "La historia de Santiago, un joven pastor andaluz que viaja a Egipto tras un sueño recurrente que le promete un tesoro. En su viaje, aprende sobre el amor, la sabiduría y la importancia de seguir los sueños propios.",
        "genre": "Ficción Filosófica"
    },
    {
        "title": "El Diario de Ana Frank",
        "author": "Ana Frank",
        "description": "El diario personal de una joven judía que documenta sus experiencias mientras se escondía con su familia durante la ocupación nazi de los Países Bajos. Un testimonio conmovedor sobre la guerra y la resistencia del espíritu humano.",
        "genre": "Biografía"
    },
    {
        "title": "Orgullo y Prejuicio",
        "author": "Jane Austen",
        "description": "Una novela que sigue a Elizabeth Bennet mientras navega por las complejidades del matrimonio, la moralidad y la sociedad en la Inglaterra del siglo XIX. Su relación con el orgulloso Sr. Darcy forma el centro de esta satírica exploración social.",
        "genre": "Romance Clásico"
    },
    {
        "title": "El Hobbit",
        "author": "J.R.R. Tolkien",
        "description": "La aventura de Bilbo Bolsón, un hobbit que es reclutado por el mago Gandalf para acompañar a un grupo de enanos en su misión de reclamar su reino y tesoro, custodiados por el temible dragón Smaug.",
        "genre": "Fantasía"
    },
    {
        "title": "Crónica de una Muerte Anunciada",
        "author": "Gabriel García Márquez",
        "description": "La historia de un asesinato en un pequeño pueblo, narrada a través de múltiples perspectivas y tiempos. A pesar de que todos conocían el plan del crimen, nadie pudo evitarlo, creando una tensión única en esta obra maestra del periodismo narrativo.",
        "genre": "Ficción Literaria"
    },
    {
        "title": "El Perfume",
        "author": "Patrick Süskind",
        "description": "La historia de Jean-Baptiste Grenouille, un asesino obsesionado con capturar el aroma perfecto. Nacido sin olor corporal pero con un sentido del olfato extraordinario, su búsqueda lo lleva a cometer terribles crímenes.",
        "genre": "Novela Histórica"
    },
    {
        "title": "Los Juegos del Hambre",
        "author": "Suzanne Collins",
        "description": "En un futuro distópico, Katniss Everdeen se ofrece voluntaria para los Juegos del Hambre en lugar de su hermana menor. En estos juegos televisados, 24 jóvenes deben luchar a muerte hasta que solo quede un superviviente.",
        "genre": "Ciencia Ficción Juvenil"
    },
    {
        "title": "El Gran Gatsby",
        "author": "F. Scott Fitzgerald",
        "description": "Un retrato de la era del jazz en los años 20, la historia sigue al misterioso millonario Jay Gatsby y su obsesión por Daisy Buchanan. Una crítica al sueño americano y una exploración del amor, la riqueza y la decadencia.",
        "genre": "Ficción Literaria"
    },
    {
        "title": "Rayuela",
        "author": "Julio Cortázar",
        "description": "Una novela experimental que puede leerse de múltiples maneras. Sigue la historia de Horacio Oliveira entre París y Buenos Aires, explorando el amor, el arte y la búsqueda existencial a través de una narrativa no lineal.",
        "genre": "Ficción Experimental"
    },
    {
        "title": "Los Pilares de la Tierra",
        "author": "Ken Follett",
        "description": "Una épica historia ambientada en la Inglaterra medieval que sigue la construcción de una catedral gótica. Entrelaza las vidas de monjes, nobles y plebeyos en una narrativa que abarca décadas de historia, amor y conflicto.",
        "genre": "Novela Histórica"
    },
    {
        "title": "Matar a un Ruiseñor",
        "author": "Harper Lee",
        "description": "A través de los ojos de Scout Finch, una niña de Alabama, se narra la historia de su padre, el abogado Atticus Finch, mientras defiende a un hombre negro falsamente acusado de violación en el sur de Estados Unidos de los años 30.",
        "genre": "Ficción Literaria"
    },
    {
        "title": "La Sombra del Viento",
        "author": "Carlos Ruiz Zafón",
        "description": "En la Barcelona de posguerra, un joven Daniel Sempere descubre un libro misterioso que lo lleva a una intrigante búsqueda sobre su autor. Una historia que mezcla misterio, romance y el amor por los libros.",
        "genre": "Misterio"
    },
    {
        "title": "Los Miserables",
        "author": "Victor Hugo",
        "description": "La épica historia de Jean Valjean, un ex convicto que busca la redención en la Francia del siglo XIX. A través de su vida y la de otros personajes, la novela explora temas de justicia, moral y amor en medio de la turbulenta historia francesa.",
        "genre": "Novela Clásica"
    }
]

# Nombres de usuarios reales
REAL_USERS = [
    {
        "username": "martin_lopez",
        "email": "martinlopez@gmail.com",
        "name": "Martín López",
        "profile_photo": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=500"
    },
    {
        "username": "laura_garcia",
        "email": "lauragarcia@gmail.com",
        "name": "Laura García",
        "profile_photo": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=500"
    },
    {
        "username": "carlos_rodriguez",
        "email": "carlosrodriguez@gmail.com",
        "name": "Carlos Rodríguez",
        "profile_photo": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=500"
    },
    {
        "username": "ana_martinez",
        "email": "anamartinez@gmail.com",
        "name": "Ana Martínez",
        "profile_photo": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=500"
    },
    {
        "username": "diego_sanchez",
        "email": "diegosanchez@gmail.com",
        "name": "Diego Sánchez",
        "profile_photo": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500"
    },
    {
        "username": "valeria_torres",
        "email": "valeriat@gmail.com",
        "name": "Valeria Torres",
        "profile_photo": "https://images.unsplash.com/photo-1524250502761-1ac6f2e30d43?w=500"
    },
    {
        "username": "pablo_fernandez",
        "email": "pablofernandez@gmail.com",
        "name": "Pablo Fernández",
        "profile_photo": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=500"
    },
    {
        "username": "lucia_romero",
        "email": "luciaromero@gmail.com",
        "name": "Lucía Romero",
        "profile_photo": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=500"
    },
    {
        "username": "juan_perez",
        "email": "juanperez@gmail.com",
        "name": "Juan Pérez",
        "profile_photo": "https://images.unsplash.com/photo-1463453091185-61582044d556?w=500"
    },
    {
        "username": "sofia_gomez",
        "email": "sofiagomez@gmail.com",
        "name": "Sofía Gómez",
        "profile_photo": "https://images.unsplash.com/photo-1521252659862-eec69941b071?w=500"
    }
]

# Comentarios reales sobre usuarios
REAL_COMMENTS = [
    "Excelente experiencia intercambiando libros con este usuario. Muy puntual y los libros estaban en perfecto estado.",
    "Increíble selección de libros y muy buena predisposición para el intercambio. Totalmente recomendable.",
    "Una persona muy agradable y confiable. El intercambio fue rápido y sin problemas.",
    "Gran experiencia. Los libros estaban muy bien cuidados y la comunicación fue excelente.",
    "Muy responsable con los tiempos de entrega y el estado de los libros era tal cual lo describió.",
    "Fantástico trato y muy buena comunicación. Sin duda volvería a intercambiar libros con este usuario.",
    "Usuario muy confiable y con una colección impresionante. Totalmente recomendado para intercambios."
]

from faker import Faker
import mysql.connector
from random import uniform, choice, randint
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_DATABASE")
}

fake = Faker('es_ES')  # Configuramos Faker para español

def insert_test_data():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Insertar usuarios reales
        user_ids = []
        for user in REAL_USERS:
            latitude = uniform(-34.6690, -34.5390)  # Coordenadas de Buenos Aires
            longitude = uniform(-58.5317, -58.3539)
            
            cursor.execute(
                """INSERT INTO Users 
                (username, email, password, profile_photo, latitude, longitude, created_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (user['username'], user['email'], "password123", user['profile_photo'], 
                 latitude, longitude, fake.date_time_between(start_date='-1y', end_date='now'))
            )
            user_ids.append(cursor.lastrowid)

        # Insertar libros reales
        book_ids = []
        for book in REAL_BOOKS:
            owner_id = choice(user_ids)
            availability_status = True
            book['photo'] = f"https://picsum.photos/200/300?random={randint(1, 1000)}"
            
            cursor.execute(
                """INSERT INTO Books 
                (name, author, photo, description, availability_status, genre, owner_id, average_rating, created_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (book['title'], book['author'], book['photo'], book['description'], 
                 availability_status, book['genre'], owner_id, 0.00,
                 fake.date_time_between(start_date='-6m', end_date='now'))
            )
            book_ids.append(cursor.lastrowid)

        # Insertar comentarios reales de forma aleatoria
        for comment in REAL_COMMENTS:
            commenter_id = choice(user_ids)
            # Asegurarse de que el receptor sea diferente al comentador
            possible_receivers = [u for u in user_ids if u != commenter_id]
            receiver_id = choice(possible_receivers)
            
            cursor.execute(
                """INSERT INTO UserComments 
                (commenter_id, receiver_id, comment, created_at) 
                VALUES (%s, %s, %s, %s)""",
                (commenter_id, receiver_id, comment, 
                 fake.date_time_between(start_date='-3m', end_date='now'))
            )

        # Insertar calificaciones de libros
        for book_id in book_ids:
            num_ratings = randint(3, 8)
            for _ in range(num_ratings):
                rater_id = choice(user_ids)
                rating = randint(3, 5)  # Calificaciones altas para libros populares
                
                try:
                    cursor.execute(
                        """INSERT INTO BookRatings 
                        (book_id, rater_id, rating, created_at) 
                        VALUES (%s, %s, %s, %s)""",
                        (book_id, rater_id, rating, 
                         fake.date_time_between(start_date='-3m', end_date='now'))
                    )
                except mysql.connector.Error:
                    continue

        # Insertar intercambios de libros
        for _ in range(15):
            book_id = choice(book_ids)
            cursor.execute("SELECT owner_id FROM Books WHERE id = %s", (book_id,))
            owner_id = cursor.fetchone()[0]
            possible_requesters = [u for u in user_ids if u != owner_id]
            
            if possible_requesters:
                requester_id = choice(possible_requesters)
                created_at = fake.date_time_between(start_date='-2m', end_date='now')
                
                cursor.execute(
                    """INSERT INTO BookExchanges 
                    (book_id, requester_id, owner_id, status, created_at, updated_at) 
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                    (book_id, requester_id, owner_id, 'completed', created_at, 
                     created_at + timedelta(days=randint(1, 14)))
                )
        
        # Insertar calificaciones de usuario
        for user_id in user_ids:
            # Cada usuario recibe entre 2 y 5 calificaciones
            num_ratings = randint(2, 5)
            for _ in range(num_ratings):
                # Seleccionar un evaluador diferente al usuario actual
                possible_raters = [u for u in user_ids if u != user_id]
                rater_id = choice(possible_raters)
                rating = randint(3, 5)  # Calificaciones altas ya que son usuarios confiables
                
                try:
                    cursor.execute(
                        """INSERT INTO UserRatings 
                        (rater_id, rated_user_id, rating, created_at) 
                        VALUES (%s, %s, %s, %s)""",
                        (rater_id, user_id, rating, 
                        fake.date_time_between(start_date='-3m', end_date='now'))
                    )
                except mysql.connector.Error:
                    continue  # Ignorar si ya existe la calificación

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
