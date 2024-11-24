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
        
        create_users_keys_table = """
        CREATE TABLE IF NOT EXISTS Users_keys (
            users_id INT AUTO_INCREMENT PRIMARY KEY,
            fernet_key BLOB NOT NULL,
            FOREIGN KEY (users_id) REFERENCES Users(id_users)
        )
        """
        cursor.execute(create_users_keys_table)
        
        create_ratings_table = """
        CREATE TABLE IF NOT EXISTS User_Ratings (
            id_rating INT AUTO_INCREMENT PRIMARY KEY,
            rated_user_id INT NOT NULL,
            rater_user_id INT NOT NULL,
            rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
            comment TEXT,
            rating_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            exchange_id INT,
            FOREIGN KEY (rated_user_id) REFERENCES Users(id_users),
            FOREIGN KEY (rater_user_id) REFERENCES Users(id_users),
            FOREIGN KEY (exchange_id) REFERENCES Book_Exchange(id_exchange),
            UNIQUE KEY unique_rating (rated_user_id, rater_user_id, exchange_id)
        )
        """
        cursor.execute(create_ratings_table)
        
        create_comments_table = """
        CREATE TABLE IF NOT EXISTS Comments (
            id_comments INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            comments TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(id_users)
        )
        """
        cursor.execute(create_comments_table)
        
        create_user_locations_table = """
        CREATE TABLE IF NOT EXISTS User_Locations (
            id_location INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            latitude DECIMAL(10, 8) NOT NULL,
            longitude DECIMAL(11, 8) NOT NULL,
            city VARCHAR(50),
            country VARCHAR(50),
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(id_users)
             )
        """
        cursor.execute(create_user_locations_table)
        
        insert_users = """
        INSERT INTO Users (username, name, email, password, profile_photo)
        VALUES (%s, %s, %s, %s, %s)
        """
        users_data = [
            ('user1', 'Name1', 'mail1@gmail.com', 'default password', 'https://images.unsplash.com/photo-1599488879763-bc34d1796448?q=80&w=1469&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user2', 'Name2', 'mail2@gmail.com', 'default password', 'https://images.unsplash.com/photo-1651570095137-500ac393a2d9?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user3', 'Name3', 'mail3@gmail.com', 'default password', 'https://images.unsplash.com/photo-1602924097911-a78ca1af38c6?q=80&w=1433&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user4', 'Name4', 'mail4@gmail.com', 'default password', 'https://images.unsplash.com/photo-1554579306-94e345617dbc?q=80&w=1331&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user5', 'Name5', 'mail5@gmail.com', 'default password', 'https://images.unsplash.com/photo-1606494554797-279096d01a9a?q=80&w=1335&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user6', 'Name6', 'mail6@gmail.com', 'default password', 'https://plus.unsplash.com/premium_photo-1667873584049-d9f7b3aa73d4?q=80&w=1471&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user7', 'Name7', 'mail7@gmail.com', 'default password', 'https://images.unsplash.com/photo-1535930891776-0c2dfb7fda1a?q=80&w=1374&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user8', 'Name8', 'mail8@gmail.com', 'default password', 'https://images.unsplash.com/photo-1549488799-496ecb87b5b3?q=80&w=1374&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user9', 'Name9', 'mail9@gmail.com', 'default password', 'https://images.unsplash.com/photo-1651017414745-96819e87e452?q=80&w=1332&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user10', 'Name10', 'mail10@gmail.com', 'default password', 'https://images.unsplash.com/photo-1453227588063-bb302b62f50b?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user11', 'Name11', 'mail11@gmail.com', 'default password', 'https://images.unsplash.com/photo-1477868433719-7c5f2731b310?q=80&w=1474&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user12', 'Name12', 'mail12@gmail.com', 'default password', 'https://images.unsplash.com/photo-1607473129014-0afb7ed09c3a?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user13', 'Name13', 'mail13@gmail.com', 'default password', 'https://images.unsplash.com/photo-1544822688-c5f41d2c1972?q=80&w=1419&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user14', 'Name14', 'mail14@gmail.com', 'default password', 'https://images.unsplash.com/photo-1523920290228-4f321a939b4c?q=80&w=1476&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')
        ]   
        cursor.executemany(insert_users, users_data)
        print("Base de datos y tablas creadas exitosamente.")
        
        insert_books = """
        INSERT INTO Books (name_book, author, owner, photo, description, status, genre)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        books_data = [
            ('After', 'Anna Todd', 1, 'https://m.media-amazon.com/images/I/81h1OJdLBsL._SL1500_.jpg', 'La historia gira en torno a la complicada relación amorosa entre Tessa Young, una chica estudiosa y educada, y Hardin Scott, el chico malo de la universidad.', 'Disponible', 'Romance'),
            ('Hoy no es siempre', 'Sabrina Critzmann', 2, 'https://m.media-amazon.com/images/I/71vSigvp4zL._SL1500_.jpg', 'Guía práctica para una crianza respetuosa', 'Disponible', 'Maternidad y Crianza'),
            ('Hush, Hush', 'Becca Fitzpatrick', 3, 'https://m.media-amazon.com/images/I/71nPdCKx15L._SL1500_.jpg', ' La saga Hush, Hush habla del amor que se desarrolla entre Nora Grey y Patch Cipriano','Disponible', 'Literatura fantástica'),
            ('La Felicidad', 'Gabriel Rolón', 4, 'https://m.media-amazon.com/images/I/61Ed9FZzUpL._SL1500_.jpg', 'El reconocido psicoanalista y psicoterapeuta argentino, Gabriel Rolón, nos propone un nuevo ensayo en el que se cuestiona los discursos contemporáneos sobre la felicidad.', 'Disponible', 'Psicologia'),
            ('Harry Potter', 'J. K. Rowling', 5, 'https://m.media-amazon.com/images/I/91R1AixEiLL._SL1500_.jpg', 'Harry Potter y la piedra filosofal es el primer libro de la heptalogía acerca del joven mago Harry Potter, escrita por J.K. Rowling', 'Disponible', 'Literatura Fantástica' ),
            ('Las mujeres que aman demasiado', 'Robin Norwood', 6, 'https://m.media-amazon.com/images/I/71B8AWw6Z+L._SL1500_.jpg', 'En este libro la autora ofrece un camino para que todas aquellas mujeres que aman demasiado puedan amarse a sí mismas y establezcan una relación de pareja sana, feliz y duradera.', 'Disponible', 'Autoayuda'),
            ('La chica del tren', 'Paula Hawkings', 7, 'https://m.media-amazon.com/images/I/616nzgP+DgL._SL1500_.jpg', 'La chica del tren es una novela de intriga y misterio de la autora británica Paula Hawkins', 'Disponible', 'Suspenso'),
            ('Caos', 'Magalí Tajes', 8, 'https://m.media-amazon.com/images/I/71donXmsVgL._SL1500_.jpg', '¿Cuántos muros se tienen que saltar para llegar a un puente? ¿Cuántos universos hay que dejar morir para que nazca el propio? Caos. Una fiesta, varias habitaciones, tres tiempos: pasado errático, presente mágico, futuro incierto. Puertas que abren mundos y cierran miedos. Cinco colores jugando a adivinar de qué color pintás la vida. Historias dentro de historias. Disfraces desnudos. La risa como revolución. Miradas que buscan ojos en los que reconocerse. Espejos y corazones rotos. Caos. Mucho caos. Todas las personas que habitan en mí sacando a bailar a las que habitan en vos.¡Qué empiece la fiesta!', 'Disponible', 'Literatura y Ficción' ),
            ('Algo tan sensillo como tuitear te quiero', 'Blue Jeans', 9, 'https://m.media-amazon.com/images/I/81LWh4L5WNL._SL1500_.jpg', 'Algo tan sencillo como tuitear te quiero es la nueva y esperada novela de Blue Jeans, el autor de la serie más vendida de literatura juvenil romántica. En esta novela, conoceremos a un grupo de chicos y chicas que afrontan por primera vez la experiencia de vivir y estudiar lejos de la casa familiar. Madrid se convertirá en su ciudad de acogida y la residencia, en su nuevo hogar. Todos ellos tendrán sus propios problemas y deberán enfrentarse a las novatadas, la soledad, las nuevas relaciones que puedan surgir, las tentaciones poco recomendables… A pesar de todo, y por encima de todo, triunfará el amor, la amistad y la lealtad al grupo.', 'Disponible', 'Ficción'),
            ('Bridgerton', 'Julia Quinn', 10, 'https://m.media-amazon.com/images/I/81PomFbUKTL._SL1500_.jpg', 'Bridgerton es una serie de ocho novelas románticas ambientadas en la época de Regencia escritas por Julia Quinn. Publicada entre 2000 y 2006, sigue a los ocho hermanos y hermanas de la noble familia Bridgerton mientras se adentran en la alta sociedad londinense en busca de amor, aventuras y felicidad.', 'Disponible', 'Ficción')
            ('El señor de los anillos', 'J. R. R. Tolkien', 11, 'https://m.media-amazon.com/images/I/71oVTrHAylL._SL1178_.jpg', 'El Señor de los Anillos es una novela de fantasía épica escrita por el filólogo y escritor británico J. R. R. Tolkien.', 'Disponible', 'Literatura Fantástica'),
            ('Pulsaciones', 'Francesc Miralles y Javier Ruescas', 12, 'https://m.media-amazon.com/images/I/61RMr3aL6iL._SL1002_.jpg', 'Elia se acaba de despertar de un coma y está un poco perdida. Lo último que recuerda es un concierto y una frase: "No puedo devolverte la canción, pero puedo mostrarte cómo danzan los peces". Ahora que sus padres le han comprado un Smartphone, Elia por fin tiene acceso al Heartbits (un programa en la línea del WhatsApp) y los lectores somos testigos de todas sus conversaciones. Con la ayuda de su mejor amiga, Sue, Elia intentará recuperar los tres días que ha olvidado y, mientras tanto, conocerá a Tommy, un estadounidense que viene de intercambio a España; a Marion, una chica con media cara quemada que asiste a su terapia de grupo, y a Phoenix, un desconocido al que le encantan los aforismos.', 'Dispoinible', 'Ficción'),
            ('El ABC de la pasteleria', 'Osvaldo Gross', 13, 'https://m.media-amazon.com/images/I/71Rgt8fhOUL._SL1500_.jpg', '"Con el auge creciente de la gastronomía en escuelas, en la televisión, en revistas y demás medios de divulgación, he visto tantas definiciones erróneas e imprecisiones que, casi rebelándome, me dije a mí mismo: '"Tengo que poner luz y verdad en la materia"'. Por eso decidí revisar, actualizar y agregar algunos conceptos y recetas que estaban en mi libro Pastelería base y concebir este nuevo El ABC de la pastelería." Y así surgió este libro. Un manual en el que se abordan los aspectos básicos de la pastelería de la mano de quien es, sin duda, una de las figuras con más experiencia y reconocimiento en el tema: Osvaldo Gross. Una obra de iniciación y de consulta permanente para estudiantes, fanáticos y, por qué no, algún que otro indeciso.', 'Disponible', 'Cocina'),
            ('No sonrias que me enamoro', 'Blue Jeans', 14, 'https://m.media-amazon.com/images/I/71Wzzj4LS0L._SL1500_.jpg', 'Hasta hace unos meses formaban El Club de los Incomprendidos. Cada uno con su personalidad y su carácter, eran los mejores amigos del mundo. Pero ahora, superados los viejos problemas, otros nuevos han separado sus caminos. Con ayuda de nuevas amistades ¿conseguirán recuperar la confianza perdida y volver a la normalidad?', 'Disponible', 'Ficción'),
            ('Una influencer muerta en Paris', 'Blue Jeans', 15, 'https://m.media-amazon.com/images/I/71aRW-UGSqL._SL1500_.jpg', 'El nuevo thriller juvenil de Blue Jeans, brutalmente impactante y actual París, 2023. Una famosa marca francesa de perfumes y cosméticos convoca el Premio al Mejor Influencer del Momento de habla hispana para así hacerse un hueco en el mercado español. El galardón se entregará en la capital francesa, pero esta fiesta repleta de lujo, influencers y lentejuelas acabará de una forma trágica: Henar Berasategui, una de las candidatas al premio y la instagrammer más popular de los últimos tiempos, aparece muerta en uno de los baños del teatro donde se celebra la gala. Junto al cadáver encuentran, con las manos llenas de sangre, a Ana Leyton (Ley), una tiktoker de diecinueve años que está arrasando y que es la mayor rival de Henar. El mundo de los influencers, sus representantes, las marcas, la rivalidad entre creadores de contenido, la juventud con la que adquieren la fama, los haters, la presión que soportan, las cuestiones relacionadas con la salud mental, los fans que se obsesionan con sus ídolos, los intereses y el dinero que mueven serán las claves de esta nueva novela de Blue Jeans, vertiginosa, intrigante y de rabiosa actualidad, en la que el amor, la incomprensión y la muerte también estarán muy presentes. Cinco influencers candidatos a un premio. ¿Se esconde un asesino tras uno de ellos? TODO VALE POR UN LIKE.', 'Disponible', 'Suspenso')
        ]
        cursor.executemany(insert_books, books_data)
        
        insert_exchange = """
        INSERT INTO Book_Exchange (book_id, user_1, user_2, exchange_status)
        VALUES (%s, %s, %s, %s)
        """
        exchange_data = [(1, 1, 2, True)]
        cursor.executemany(insert_exchange, exchange_data)
        
        insert_ratings = """
        INSERT INTO User_Ratings 
            (rated_user_id, rater_user_id, rating, comment, exchange_id)
        VALUES 
            (%s, %s, %s, %s, %s)
        """
        ratings_data = [
            (1, 2, 1, "Puntuación 1", 1),
            (1, 3, 2, "Puntuación 2", 1),
            (2, 1, 3, "Puntuación 3", 1),
            (2, 4, 4, "Puntuación 4", 1),
            (3, 1, 5, "Puntuación 5", 1),
            (3, 2, 1, "Puntuación 6", 1),
            (4, 1, 2, "Puntuación 7", 1),
            (4, 3, 3, "Puntuación 8", 1),
            (5, 2, 4, "Puntuación 9", 1),
            (5, 4, 5, "Puntuación 10", 1),
            (6, 5, 1, "Puntuación 11", 1),
            (7, 6, 2, "Puntuación 12", 1),
            (8, 7, 3, "Puntuación 13", 1),
            (9, 8, 4, "Puntuación 14", 1),
            (10, 9, 5, "Puntuación 15", 1)
        ]
        cursor.executemany(insert_ratings, ratings_data)

        insert_locations = """
        INSERT INTO User_Locations (user_id, latitude, longitude, city, country)
        VALUES (%s, %s, %s, %s, %s)
        """
        location_data = [
            (1, -34.603722, -58.381592, 'City1', 'Country1'),
            (2, -34.921452, -57.954528, 'City2', 'Country2'),
            (3, -31.417229, -64.183319, 'City3', 'Country3'),
            (4, -32.944925, -60.651850, 'City4', 'Country4'),
            (5, -33.123456, -59.987654, 'City5', 'Country5'),
            (6, -35.234567, -58.876543, 'City6', 'Country6'),
            (7, -32.345678, -57.765432, 'City7', 'Country7'),
            (8, -31.456789, -56.654321, 'City8', 'Country8'),
            (9, -30.567890, -55.543210, 'City9', 'Country9'),
            (10, -29.678901, -54.432109, 'City10', 'Country10'),
            (11, -28.789012, -53.321098, 'City11', 'Country11'),
            (12, -27.890123, -52.210987, 'City12', 'Country12'),
            (13, -26.901234, -51.109876, 'City13', 'Country13'),
            (14, -25.012345, -50.098765, 'City14', 'Country14')
        ]
        cursor.executemany(insert_locations, location_data)

    except mysql.connector.Error as e:
        print(f"Error al crear la base de datos o tablas: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    create_database_and_tables()
