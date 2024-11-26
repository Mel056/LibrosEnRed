// Función para cargar los libros
async function cargarLibros() {
    try {
        const response = await fetch('http://localhost:5001/books');
        const libros = await response.json();
        const carouselContainer = document.getElementById('carousel-libros');

        carouselContainer.innerHTML = '';

        // Generar HTML para cada libro
        libros.forEach(libro => {
            const libroHTML = `
           <div class="libros">
                <div class="contenedor-flip">
                    <div class="flip-libro">
                        <div class="libro-frente">
                            <img src="${libro.photo}" alt="${libro.name_book}">
                        </div>
                        <div class="libro-atras">
                            <h3>${libro.name_book}</h3>
                            <p>Autor: ${libro.author}</p>
                            <p>Género: ${libro.genre}</p>
                            <p>Estado: ${libro.status}</p>
                            <button class="button">
                                <a href="/detalle/${libro.id_books}">Ver más</a>
                            </button>
                        </div>
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

// Función para inicializar el carousel
function inicializarCarousel() {
    const flechaIzquierda = document.getElementById('flecha-izquierda-libros');
    const flechaDerecha = document.getElementById('flecha-derecha-libros');
    const carousel = document.querySelector('.carousel-libros');

    flechaDerecha.addEventListener('click', () => {
        carousel.scrollLeft += carousel.offsetWidth;
    });

    flechaIzquierda.addEventListener('click', () => {
        carousel.scrollLeft -= carousel.offsetWidth;
    });
}

document.addEventListener('DOMContentLoaded', cargarLibros);
