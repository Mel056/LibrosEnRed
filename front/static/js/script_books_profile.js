async function cargarLibros() {
    const user_id = document.body.getAttribute('data-user-id');
    console.log("User ID:", user_id);

    if (!user_id) {
        console.error('No se encontró el ID de usuario');
        return;
    }

    try {
        const response = await fetch(`http://localhost:5001/books?owner_id=${user_id}`);
        console.log(response)
        const libros = await response.json();
        console.log(libros)

        const carouselContainer = document.getElementById('carousel-libros');
        carouselContainer.innerHTML = '';

        if (libros.length === 0) {
            carouselContainer.innerHTML = '<p>No hay libros registrados aún.</p>';
            return;
        }


        libros.forEach(libro => {
            const photoUrl = libro.photo
                ? (libro.photo.startsWith('http')
                    ? libro.photo
                    : `http://localhost:5001/uploads/${libro.photo}`)
                : '/path/to/default/image.jpg';

            const libroHTML = `
                <div class="contenedor-flip">
                    <div class="flip-libro">
                        <div class="libro-frente">
                            <img src="${photoUrl}" alt="${libro.name}" onerror="this.onerror=null; this.src='/path/to/default/image.jpg';">
                        </div>
                        <div class="libro-atras">
                            <h3>${libro.name}</h3>
                            <p>Autor: ${libro.author}</p>
                            <p>Género: ${libro.genre}</p>
                            <p>Estado: ${libro.availability_status ? 'Disponible' : 'No disponible'}</p>
                            <button class="button">
                                <a href="/detalle/${libro.id}">Ver más</a>
                            </button>
                        </div>
                    </div>
                </div>
            `;
            carouselContainer.innerHTML += libroHTML;
        });
        inicializarCarousel();

    } catch (error) {
        console.error('Error al cargar los libros:', error);
    }
}

document.addEventListener('DOMContentLoaded', cargarLibros);