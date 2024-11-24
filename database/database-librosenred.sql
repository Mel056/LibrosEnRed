CREATE DATABASE LibrosEnREd;
USE LibrosEnREd;


CREATE TABLE Users (
    id_users INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    profile_photo VARCHAR(255) NOT NULL
);

CREATE TABLE Books (
    id_books INT AUTO_INCREMENT PRIMARY KEY,
    name_book VARCHAR(150) NOT NULL,
    author VARCHAR(100) NOT NULL,
    owner INT NOT NULL,  
    photo VARCHAR(255),
    description TEXT,
    status VARCHAR(250),
    genre VARCHAR(250),
    FOREIGN KEY (owner) REFERENCES Users(id_users)  
);


CREATE TABLE Book_Exchange (
    id_exchange INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    user_1 INT NOT NULL,
    user_2 INT NOT NULL,
    exchange_status BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (book_id) REFERENCES Books(id_books),
    FOREIGN KEY (user_1) REFERENCES Users(id_users),
    FOREIGN KEY (user_2) REFERENCES Users(id_users)
);

CREATE TABLE Maps (
    id_map INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    street VARCHAR(255) NOT NULL,
    height VARCHAR(50) NOT NULL,
    locality VARCHAR(100) NOT NULL,
    province VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id_users) ON DELETE CASCADE
)

CREATE TABLE Users_keys (
    users_id INT AUTO_INCREMENT PRIMARY KEY,
    fernet_key BLOB NOT NULL,
    FOREIGN KEY (users_id) REFERENCES Users(id_users)
)


CREATE TABLE Comments(
    id_comments INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    comments TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(id_users)   
)

INSERT INTO Users (username, name, email, profile_photo)
VALUES 
('user1', 'Name1', 'mail1@gmail.com', 'https://images.unsplash.com/photo-1599488879763-bc34d1796448?q=80&w=1469&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
('user2', 'Name2', 'mail2@gmail.com', 'https://images.unsplash.com/photo-1651570095137-500ac393a2d9?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
('user3', 'Name3', 'mail3@gmail.com', 'https://images.unsplash.com/photo-1602924097911-a78ca1af38c6?q=80&w=1433&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
('user4', 'Name4', 'mail4@gmail.com', 'https://images.unsplash.com/photo-1554579306-94e345617dbc?q=80&w=1331&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
('user5', 'Name5', 'mail5@gmail.com', 'https://images.unsplash.com/photo-1606494554797-279096d01a9a?q=80&w=1335&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
('user6', 'Name6', 'mail6@gmail.com', 'https://plus.unsplash.com/premium_photo-1667873584049-d9f7b3aa73d4?q=80&w=1471&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
('user7', 'Name7', 'mail7@gmail.com', 'https://images.unsplash.com/photo-1535930891776-0c2dfb7fda1a?q=80&w=1374&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
('user8', 'Name8', 'mail8@gmail.com', 'https://images.unsplash.com/photo-1549488799-496ecb87b5b3?q=80&w=1374&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
('user9', 'Name9', 'mail9@gmail.com', 'https://images.unsplash.com/photo-1651017414745-96819e87e452?q=80&w=1332&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
('user10', 'Name10', 'mail10@gmail.com', 'https://images.unsplash.com/photo-1453227588063-bb302b62f50b?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
('user11', 'Name11', 'mail11@gmail.com', 'https://images.unsplash.com/photo-1477868433719-7c5f2731b310?q=80&w=1474&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
('user12', 'Name12', 'mail12@gmail.com', 'https://images.unsplash.com/photo-1607473129014-0afb7ed09c3a?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
('user13', 'Name13', 'mail13@gmail.com', 'https://images.unsplash.com/photo-1544822688-c5f41d2c1972?q=80&w=1419&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'),
('user14', 'Name14', 'mail14@gmail.com', 'https://images.unsplash.com/photo-1523920290228-4f321a939b4c?q=80&w=1476&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');



INSERT INTO Books (name_book, owner, photo, description, status, genre)
VALUES ('After', 'Anna Todd', 1, 'https://m.media-amazon.com/images/I/81h1OJdLBsL._SL1500_.jpg', 'La historia gira en torno a la complicada relación amorosa entre Tessa Young, una chica estudiosa y educada, y Hardin Scott, el chico malo de la universidad.', 'Disponible', 'Romance'),
('Hoy no es siempre', 'Sabrina Critzmann', 2, 'https://m.media-amazon.com/images/I/71vSigvp4zL._SL1500_.jpg', 'Guía práctica para una crianza respetuosa', 'Disponible', 'Maternidad y Crianza'),
('Hush, Hush', 'Becca Fitzpatrick', 3, 'https://m.media-amazon.com/images/I/71nPdCKx15L._SL1500_.jpg', ' La saga Hush, Hush habla del amor que se desarrolla entre Nora Grey y Patch Cipriano','Disponible', 'Literatura fantástica'),
('La Felicidad', 'Gabriel Rolón', 4, 'https://m.media-amazon.com/images/I/61Ed9FZzUpL._SL1500_.jpg', 'El reconocido psicoanalista y psicoterapeuta argentino, Gabriel Rolón, nos propone un nuevo ensayo en el que se cuestiona los discursos contemporáneos sobre la felicidad.', 'Disponible', 'Psicologia'),
('Harry Potter', 'J. K. Rowling', 5, 'https://m.media-amazon.com/images/I/91R1AixEiLL._SL1500_.jpg', 'Harry Potter y la piedra filosofal es el primer libro de la heptalogía acerca del joven mago Harry Potter, escrita por J.K. Rowling', 'Disponible', 'Literatura Fantástica' ),
('Las mujeres que aman demasiado', 'Robin Norwood', 6, 'https://m.media-amazon.com/images/I/71B8AWw6Z+L._SL1500_.jpg', 'En este libro la autora ofrece un camino para que todas aquellas mujeres que aman demasiado puedan amarse a sí mismas y establezcan una relación de pareja sana, feliz y duradera.', 'Disponible', 'Autoayuda'),
('La chica del tren', 'Paula Hawkings', 7, 'https://m.media-amazon.com/images/I/616nzgP+DgL._SL1500_.jpg', 'La chica del tren es una novela de intriga y misterio de la autora británica Paula Hawkins', 'Disponible', 'Suspenso'),
('Caos', 'Magalí Tajes', 8, 'https://m.media-amazon.com/images/I/71donXmsVgL._SL1500_.jpg', '¿Cuántos muros se tienen que saltar para llegar a un puente? ¿Cuántos universos hay que dejar morir para que nazca el propio? Caos. Una fiesta, varias habitaciones, tres tiempos: pasado errático, presente mágico, futuro incierto. Puertas que abren mundos y cierran miedos. Cinco colores jugando a adivinar de qué color pintás la vida. Historias dentro de historias. Disfraces desnudos. La risa como revolución. Miradas que buscan ojos en los que reconocerse. Espejos y corazones rotos. Caos. Mucho caos. Todas las personas que habitan en mí sacando a bailar a las que habitan en vos.
¡Qué empiece la fiesta!', 'Disponible', 'Literatura y Ficción' ),
('Algo tan sensillo como tuitear te quiero', 'Blue Jeans', 9, 'https://m.media-amazon.com/images/I/81LWh4L5WNL._SL1500_.jpg', 'Algo tan sencillo como tuitear te quiero es la nueva y esperada novela de Blue Jeans, el autor de la serie más vendida de literatura juvenil romántica. En esta novela, conoceremos a un grupo de chicos y chicas que afrontan por primera vez la experiencia de vivir y estudiar lejos de la casa familiar. Madrid se convertirá en su ciudad de acogida y la residencia, en su nuevo hogar. Todos ellos tendrán sus propios problemas y deberán enfrentarse a las novatadas, la soledad, las nuevas relaciones que puedan surgir, las tentaciones poco recomendables… A pesar de todo, y por encima de todo, triunfará el amor, la amistad y la lealtad al grupo.', 'Disponible', 'Ficción'),
('Bridgerton', 'Julia Quinn', 10, 'https://m.media-amazon.com/images/I/81PomFbUKTL._SL1500_.jpg', 'Bridgerton es una serie de ocho novelas románticas ambientadas en la época de Regencia escritas por Julia Quinn. Publicada entre 2000 y 2006, sigue a los ocho hermanos y hermanas de la noble familia Bridgerton mientras se adentran en la alta sociedad londinense en busca de amor, aventuras y felicidad.', 'Disponible', 'Ficción')
('El señor de los anillos', 'J. R. R. Tolkien', 11, 'https://m.media-amazon.com/images/I/71oVTrHAylL._SL1178_.jpg', 'El Señor de los Anillos es una novela de fantasía épica escrita por el filólogo y escritor británico J. R. R. Tolkien.', 'Disponible', 'Literatura Fantástica'),
('Pulsaciones', 'Francesc Miralles y Javier Ruescas', 12, 'https://m.media-amazon.com/images/I/61RMr3aL6iL._SL1002_.jpg', 'Elia se acaba de despertar de un coma y está un poco perdida. Lo último que recuerda es un concierto y una frase: "No puedo devolverte la canción, pero puedo mostrarte cómo danzan los peces". Ahora que sus padres le han comprado un Smartphone, Elia por fin tiene acceso al Heartbits (un programa en la línea del WhatsApp) y los lectores somos testigos de todas sus conversaciones. Con la ayuda de su mejor amiga, Sue, Elia intentará recuperar los tres días que ha olvidado y, mientras tanto, conocerá a Tommy, un estadounidense que viene de intercambio a España; a Marion, una chica con media cara quemada que asiste a su terapia de grupo, y a Phoenix, un desconocido al que le encantan los aforismos.', 'Dispoinible', 'Ficción'),
('El ABC de la pasteleria', 'Osvaldo Gross', 13, 'https://m.media-amazon.com/images/I/71Rgt8fhOUL._SL1500_.jpg', '"Con el auge creciente de la gastronomía en escuelas, en la televisión, en revistas y demás medios de divulgación, he visto tantas definiciones erróneas e imprecisiones que, casi rebelándome, me dije a mí mismo: '"Tengo que poner luz y verdad en la materia"'. Por eso decidí revisar, actualizar y agregar algunos conceptos y recetas que estaban en mi libro Pastelería base y concebir este nuevo El ABC de la pastelería." Y así surgió este libro. Un manual en el que se abordan los aspectos básicos de la pastelería de la mano de quien es, sin duda, una de las figuras con más experiencia y reconocimiento en el tema: Osvaldo Gross. Una obra de iniciación y de consulta permanente para estudiantes, fanáticos y, por qué no, algún que otro indeciso.', 'Disponible', 'Cocina'),
('No sonrias que me enamoro', 'Blue Jeans', 14, 'https://m.media-amazon.com/images/I/71Wzzj4LS0L._SL1500_.jpg', 'Hasta hace unos meses formaban El Club de los Incomprendidos. Cada uno con su personalidad y su carácter, eran los mejores amigos del mundo. Pero ahora, superados los viejos problemas, otros nuevos han separado sus caminos. Con ayuda de nuevas amistades ¿conseguirán recuperar la confianza perdida y volver a la normalidad?', 'Disponible', 'Ficción'),
('Una influencer muerta en Paris', 'Blue Jeans', 15, 'https://m.media-amazon.com/images/I/71aRW-UGSqL._SL1500_.jpg', '

El nuevo thriller juvenil de Blue Jeans, brutalmente impactante y actual

París, 2023. Una famosa marca francesa de perfumes y cosméticos convoca el Premio al Mejor Influencer del Momento de habla hispana para así hacerse un hueco en el mercado español. El galardón se entregará en la capital francesa, pero esta fiesta repleta de lujo, influencers y lentejuelas acabará de una forma trágica: Henar Berasategui, una de las candidatas al premio y la instagrammer más popular de los últimos tiempos, aparece muerta en uno de los baños del teatro donde se celebra la gala. Junto al cadáver encuentran, con las manos llenas de sangre, a Ana Leyton (Ley), una tiktoker de diecinueve años que está arrasando y que es la mayor rival de Henar.

El mundo de los influencers, sus representantes, las marcas, la rivalidad entre creadores de contenido, la juventud con la que adquieren la fama, los haters, la presión que soportan, las cuestiones relacionadas con la salud mental, los fans que se obsesionan con sus ídolos, los intereses y el dinero que mueven serán las claves de esta nueva novela de Blue Jeans, vertiginosa, intrigante y de rabiosa actualidad, en la que el amor, la incomprensión y la muerte también estarán muy presentes.

Cinco influencers candidatos a un premio. ¿Se esconde un asesino tras uno de ellos? TODO VALE POR UN LIKE.
', 'Disponible', 'Suspenso')

INSERT INTO Book_Exchange (book_id, user_1, user_2, exchange_status)
VALUES (1, 1, 2, TRUE);

INSERT INTO Maps (user_id, street, height, locality, province, country)
VALUES ('1', 'street1', 'height2', 'locality1', 'province1', 'country1'),
('2', 'street2', 'height2', 'locality2', 'province2', 'country2'),
('3', 'street3', 'height3', 'locality3', 'province3', 'country3'),
('4', 'street4', 'height4', 'locality4', 'province4', 'country4'),
('5', 'street5', 'height5', 'locality5', 'province5', 'country5'),
('6', 'street6', 'height6', 'locality6', 'province6', 'country6'),
('7', 'street7', 'height7', 'locality7', 'province7', 'country7'),
('8', 'street8', 'height8', 'locality8', 'province8', 'country8'),
('9', 'street9', 'height9', 'locality9', 'province9', 'country9'),
('10', 'street10', 'height10', 'locality10', 'province10', 'country10'),
('11', 'street11', 'height11', 'locality11', 'province11', 'country11'),
('12', 'street12', 'height12', 'locality12', 'province12', 'country12'),
('13', 'street13', 'height13', 'locality13', 'province13', 'country13'),
('14', 'street14', 'height14', 'locality14', 'province14', 'country14')