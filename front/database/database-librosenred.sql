CREATE DATABASE LibrosEnREd;
USE LibrosEnREd;

CREATE TABLE Users (
    id_users INT AUTO_INCREMENT PRIMARY KEY,
    id_books INT,
    username VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    maps VARCHAR(200) NOT NULL,
    password VARCHAR(300) NOT NULL,
    profile_photo VARCHAR(255),
FOREIGN KEY (id_books) REFERENCES Books(id_books)
);

CREATE TABLE Books (
    id_books INT AUTO_INCREMENT PRIMARY KEY,
    name_book VARCHAR(150) NOT NULL,
    owner INT,
    photo VARCHAR(255),
    description TEXT,
    status VARCHAR(250),
    genre VARCHAR(250),
FOREIGN KEY (owner) REFERENCES Users(id_users)
);

INSERT INTO Books (name_book, owner, photo, description, status, genre)
VALUES ('After', 'Anna Todd', 1, 'https://images.app.goo.gl/FeLkpZxJ9atvxKvr7', 'La historia gira en torno a la complicada relación amorosa entre Tessa Young, una chica estudiosa y educada, y Hardin Scott, el chico malo de la universidad.', 'Disponible', 'Romance'),
('Hoy no es siempre', 'Sabrina Critzmann', 2, 'https://images.app.goo.gl/KZzSWaJWnZdJr4Au9', 'Guía práctica para una crianza respetuosa', 'Disponible', 'Maternidad y Crianza'),
('Hush, Hush', 'Becca Fitzpatrick', 3, 'https://images.app.goo.gl/yLNiV9AV8e76JJnb8', ' La saga Hush, Hush habla del amor que se desarrolla entre Nora Grey y Patch Cipriano','Disponible', 'Literatura fantástica'),
('La Felicidad', 'Gabriel Rolón', 4, 'https://images.app.goo.gl/BnUwA51sNV8HYPZb8', 'El reconocido psicoanalista y psicoterapeuta argentino, Gabriel Rolón, nos propone un nuevo ensayo en el que se cuestiona los discursos contemporáneos sobre la felicidad.', 'Disponible', 'Psicologia'),
('Harry Potter', 'J. K. Rowling', 5, 'https://images.app.goo.gl/f6i3AFT9BXqQaVTq6', 'Harry Potter y la piedra filosofal es el primer libro de la heptalogía acerca del joven mago Harry Potter, escrita por J.K. Rowling', 'Disponible', 'Literatura Fantástica' ),
('Las mujeres que aman demasiado', 'Robin Norwood', 6, 'https://images.app.goo.gl/cmNGTfnRgj5626ft6', 'En este libro la autora ofrece un camino para que todas aquellas mujeres que aman demasiado puedan amarse a sí mismas y establezcan una relación de pareja sana, feliz y duradera.', 'Disponible', 'Autoayuda'),
('La chica del tren', 'Paula Hawkings', 7, 'https://images.app.goo.gl/wVmvCZPtcueoRrvL6', 'La chica del tren es una novela de intriga y misterio de la autora británica Paula Hawkins', 'Disponible', 'Suspenso'),
('Caos', 'Magalí Tajes', 8, 'https://images.app.goo.gl/ktubEDXh6c1w5XBw5', '¿Cuántos muros se tienen que saltar para llegar a un puente? ¿Cuántos universos hay que dejar morir para que nazca el propio? Caos. Una fiesta, varias habitaciones, tres tiempos: pasado errático, presente mágico, futuro incierto. Puertas que abren mundos y cierran miedos. Cinco colores jugando a adivinar de qué color pintás la vida. Historias dentro de historias. Disfraces desnudos. La risa como revolución. Miradas que buscan ojos en los que reconocerse. Espejos y corazones rotos. Caos. Mucho caos. Todas las personas que habitan en mí sacando a bailar a las que habitan en vos.
¡Qué empiece la fiesta!', 'Disponible', 'Literatura y Ficción' ),
('Algo tan sensillo como tuitear te quiero', 'Blue Jeans', 9, 'https://images.app.goo.gl/dYESAKMgqf3VRKwc9', 'Algo tan sencillo como tuitear te quiero es la nueva y esperada novela de Blue Jeans, el autor de la serie más vendida de literatura juvenil romántica. En esta novela, conoceremos a un grupo de chicos y chicas que afrontan por primera vez la experiencia de vivir y estudiar lejos de la casa familiar. Madrid se convertirá en su ciudad de acogida y la residencia, en su nuevo hogar. Todos ellos tendrán sus propios problemas y deberán enfrentarse a las novatadas, la soledad, las nuevas relaciones que puedan surgir, las tentaciones poco recomendables… A pesar de todo, y por encima de todo, triunfará el amor, la amistad y la lealtad al grupo.', 'Disponible', 'Ficción'),
('Bridgerton', 'Julia Quinn', 10, 'https://images.app.goo.gl/i5duTRvwMC1Bo3Qh7', 'Bridgerton es una serie de ocho novelas románticas ambientadas en la época de Regencia escritas por Julia Quinn. Publicada entre 2000 y 2006, sigue a los ocho hermanos y hermanas de la noble familia Bridgerton mientras se adentran en la alta sociedad londinense en busca de amor, aventuras y felicidad.', 'Disponible', 'Ficción')
('El señor de los anillos', 'J. R. R. Tolkien', 11, 'https://images.app.goo.gl/5DJgn9oTUNbgBopN7', 'El Señor de los Anillos es una novela de fantasía épica escrita por el filólogo y escritor británico J. R. R. Tolkien.', 'Disponible', 'Literatura Fantástica'),
('Pulsaciones', 'Francesc Miralles y Javier Ruescas', 12, 'https://images.app.goo.gl/KZro5KiTz5o5Gxmy5', 'Elia se acaba de despertar de un coma y está un poco perdida. Lo último que recuerda es un concierto y una frase: "No puedo devolverte la canción, pero puedo mostrarte cómo danzan los peces". Ahora que sus padres le han comprado un Smartphone, Elia por fin tiene acceso al Heartbits (un programa en la línea del WhatsApp) y los lectores somos testigos de todas sus conversaciones. Con la ayuda de su mejor amiga, Sue, Elia intentará recuperar los tres días que ha olvidado y, mientras tanto, conocerá a Tommy, un estadounidense que viene de intercambio a España; a Marion, una chica con media cara quemada que asiste a su terapia de grupo, y a Phoenix, un desconocido al que le encantan los aforismos.', 'Dispoinibles', 'Ficción'),
