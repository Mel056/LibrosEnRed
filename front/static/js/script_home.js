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