document.getElementById('searchButton').addEventListener('click', function () {
    const searchInput = document.getElementById('searchInput');
    searchInput.classList.toggle('open');
    searchInput.focus();
});

const fila = document.querySelector('.contenedor-carousel');
const categorias = document.querySelector('.categoria');
const flechaIzquierda = document.getElementById('flecha-izquierda');
const flechaDerecha = document.getElementById('flecha-derecha');

flechaDerecha.addEventListener('click', () => {
    fila.scrollLeft += fila.offsetWidth;
});

flechaIzquierda.addEventListener('click', () => {
    fila.scrollLeft -= fila.offsetWidth;
});

const filaLibros = document.querySelector('.contenedor-carousel-libros');
const libros = document.querySelector('.libro');
const flechaIzquierdaLibros = document.getElementById('flecha-izquierda-libros');
const flechaDerechaLibros = document.getElementById('flecha-derecha-libros');

flechaDerechaLibros.addEventListener('click', () => {
    filaLibros.scrollLeft += filaLibros.offsetWidth;
});

flechaIzquierdaLibros.addEventListener('click', () => {
    filaLibros.scrollLeft -= filaLibros.offsetWidth;
});

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
                <div class="contenedor-flip">
                    <div class="flip-libro">
                        <div class="libro-frente">
                            <img src="${libro.photo}" alt="${libro.name_book}">
                        </div>
                        <div class="libro-atras">
                            <h3>${libro.name_book}</h3>
                            <p>${libro.author}</p>
                            <p>${libro.genre}</p>
                            <p>${libro.status}</p>
                            <button class="button">
                                <a href="/Detalle/${libro.id_books}">Ver más</a>
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