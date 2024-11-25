import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "leo",  # Cambiar si se usa un usuario diferente
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
            id_users INT AUTO_INCREMENT PRIMARY KEY,
            fernet_key BLOB NOT NULL,
            FOREIGN KEY (id_users) REFERENCES Users(id_users)
        )
        """
        cursor.execute(create_users_keys_table)
        

        
        create_comments_table = """
        CREATE TABLE IF NOT EXISTS Comments (
            id_comments INT AUTO_INCREMENT PRIMARY KEY,
            id_users INT NOT NULL,
            comments TEXT,
            FOREIGN KEY (id_users) REFERENCES Users(id_users)
        )
        """
        cursor.execute(create_comments_table)
        
        insert_users = """
        INSERT INTO Users (username, email, password, profile_photo)
        VALUES (%s, %s, %s, %s)
        """
        users_data = [
            ('user1', 'mail1@gmail.com', 'default password', 'https://images.unsplash.com/photo-1599488879763-bc34d1796448?q=80&w=1469&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user2', 'mail2@gmail.com', 'default password', 'https://images.unsplash.com/photo-1651570095137-500ac393a2d9?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user3', 'mail3@gmail.com', 'default password', 'https://images.unsplash.com/photo-1602924097911-a78ca1af38c6?q=80&w=1433&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user4', 'mail4@gmail.com', 'default password', 'https://images.unsplash.com/photo-1554579306-94e345617dbc?q=80&w=1331&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user5', 'mail5@gmail.com', 'default password', 'https://images.unsplash.com/photo-1606494554797-279096d01a9a?q=80&w=1335&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user6', 'mail6@gmail.com', 'default password', 'https://plus.unsplash.com/premium_photo-1667873584049-d9f7b3aa73d4?q=80&w=1471&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user7', 'mail7@gmail.com', 'default password', 'https://images.unsplash.com/photo-1535930891776-0c2dfb7fda1a?q=80&w=1374&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user8', 'mail8@gmail.com', 'default password', 'https://images.unsplash.com/photo-1549488799-496ecb87b5b3?q=80&w=1374&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user9', 'mail9@gmail.com', 'default password', 'https://images.unsplash.com/photo-1651017414745-96819e87e452?q=80&w=1332&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user10', 'mail10@gmail.com', 'default password', 'https://images.unsplash.com/photo-1453227588063-bb302b62f50b?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user11', 'mail11@gmail.com', 'default password', 'https://images.unsplash.com/photo-1477868433719-7c5f2731b310?q=80&w=1474&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user12', 'mail12@gmail.com', 'default password', 'https://images.unsplash.com/photo-1607473129014-0afb7ed09c3a?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user13',  'mail13@gmail.com', 'default password', 'https://images.unsplash.com/photo-1544822688-c5f41d2c1972?q=80&w=1419&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
            ('user14', 'mail14@gmail.com', 'default password', 'https://images.unsplash.com/photo-1523920290228-4f321a939b4c?q=80&w=1476&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')
        ] 
        cursor.executemany(insert_users, users_data)
        print("Base de datos y tablas creadas exitosamente.")
        
        insert_books = """
        INSERT INTO Books (name_book, author, photo, descripcion, status, genre)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        books_data = [
            ('After', 'Anna Todd', 'https://m.media-amazon.com/images/I/81h1OJdLBsL._SL1500_.jpg', 'La historia gira en torno a la complicada relación amorosa entre Tessa Young, una chica estudiosa y educada, y Hardin Scott, el chico malo de la universidad.', 'disponible', 'Romance'),
            ('Hoy no es siempre', 'Sabrina Critzmann', 'https://m.media-amazon.com/images/I/71vSigvp4zL._SL1500_.jpg', 'Guía práctica para una crianza respetuosa', 'disponible', 'Maternidad y Crianza'),
            ('Hush, Hush', 'Becca Fitzpatrick', 'https://m.media-amazon.com/images/I/71nPdCKx15L._SL1500_.jpg', 'La saga Hush, Hush habla del amor que se desarrolla entre Nora Grey y Patch Cipriano', 'disponible', 'Literatura fantástica'),
            ('La Felicidad', 'Gabriel Rolón', 'https://m.media-amazon.com/images/I/61Ed9FZzUpL._SL1500_.jpg', 'El reconocido psicoanalista y psicoterapeuta argentino, Gabriel Rolón, nos propone un nuevo ensayo en el que se cuestiona los discursos contemporáneos sobre la felicidad.', 'disponible', 'Psicologia'),
            ('Harry Potter', 'J. K. Rowling', 'https://m.media-amazon.com/images/I/91R1AixEiLL._SL1500_.jpg', 'Harry Potter y la piedra filosofal es el primer libro de la heptalogía acerca del joven mago Harry Potter, escrita por J.K. Rowling', 'disponible', 'Literatura Fantástica'),
            ('Las mujeres que aman demasiado', 'Robin Norwood', 'https://m.media-amazon.com/images/I/71B8AWw6Z+L._SL1500_.jpg', 'En este libro la autora ofrece un camino para que todas aquellas mujeres que aman demasiado puedan amarse a sí mismas y establezcan una relación de pareja sana, feliz y duradera.', 'disponible', 'Autoayuda'),
            ('La chica del tren', 'Paula Hawkings', 'https://m.media-amazon.com/images/I/616nzgP+DgL._SL1500_.jpg', 'La chica del tren es una novela de intriga y misterio de la autora británica Paula Hawkins', 'disponible', 'Suspenso'),
            ('Caos', 'Magalí Tajes', 'https://m.media-amazon.com/images/I/71donXmsVgL._SL1500_.jpg', '¿Cuántos muros se tienen que saltar para llegar a un puente?...', 'disponible', 'Literatura y Ficción'),
            ('Algo tan sensillo como tuitear te quiero', 'Blue Jeans', 'https://m.media-amazon.com/images/I/81LWh4L5WNL._SL1500_.jpg', 'Algo tan sencillo como tuitear te quiero es la nueva y esperada novela de Blue Jeans...', 'disponible', 'Ficción'),
            ('Bridgerton', 'Julia Quinn', 'https://m.media-amazon.com/images/I/81PomFbUKTL._SL1500_.jpg', 'Bridgerton es una serie de ocho novelas románticas...', 'disponible', 'Ficción'),
            ('El señor de los anillos', 'J. R. R. Tolkien', 'https://m.media-amazon.com/images/I/71oVTrHAylL._SL1178_.jpg', 'El Señor de los Anillos es una novela de fantasía épica...', 'disponible', 'Literatura Fantástica'),
            ('Pulsaciones', 'Francesc Miralles y Javier Ruescas', 'https://m.media-amazon.com/images/I/61RMr3aL6iL._SL1002_.jpg', 'Elia se acaba de despertar de un coma...', 'disponible', 'Ficción'),
            ('El ABC de la pasteleria', 'Osvaldo Gross', 'https://m.media-amazon.com/images/I/71Rgt8fhOUL._SL1500_.jpg', 'Con el auge creciente de la gastronomía en escuelas...', 'disponible', 'Cocina'),
            ('No sonrias que me enamoro', 'Blue Jeans', 'https://m.media-amazon.com/images/I/71Wzzj4LS0L._SL1500_.jpg', 'Hasta hace unos meses formaban El Club de los Incomprendidos...', 'disponible', 'Ficción'),
            ('Una influencer muerta en Paris', 'Blue Jeans', 'https://m.media-amazon.com/images/I/71aRW-UGSqL._SL1500_.jpg', 'El nuevo thriller juvenil de Blue Jeans...', 'disponible', 'Suspenso')
        ]
        cursor.executemany(insert_books, books_data)
        
        insert_exchange = """
        INSERT INTO Book_Exchange (book_id, user_1, user_2, exchange_status)
        VALUES (%s, %s, %s, %s)
        """
        exchange_data = [(1, 1, 2, True)]
        cursor.executemany(insert_exchange, exchange_data)
        




    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    create_database_and_tables()
