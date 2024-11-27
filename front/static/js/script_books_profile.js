// Función para cargar los libros
async function cargarLibros() {
    try {
        const response = await fetch('http://localhost:5001/books');
        const libros = await response.json();
        const carouselContainer = document.getElementById('carousel-libros');

        carouselContainer.innerHTML = '';

        // Generar HTML para cada libro
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
                            <img src="${libro.photo}" alt="${libro.name}" onerror="this.onerror=null; this.src='/path/to/default/image.jpg';">
                        </div>
                        <div class="libro-atras">
                            <h3>${libro.name}</h3>
                            <p>Autor: ${libro.author}</p>
                            <p>Género: ${libro.genre}</p>
                            <p>Estado: ${libro.availability_status ? 'Disponible' : 'No disponible'}</p>
                            <p>Propietario: ${libro.owner_username}</p>
                            <button class="button">
                                <a href="/Detalle/${libro.id}">Ver más</a>
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