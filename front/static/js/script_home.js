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

document.getElementById('search-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const name = document.getElementById('name').value.trim();

    if (!name) {
        alert("Por favor, ingresa un nombre de libro para buscar.");
        return;
    }

    const url = `http://localhost:5001/books?name=${encodeURIComponent(name)}`;

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

        const data = await response.json();

        const resultsContainer = document.getElementById('results');
        if (data.length === 0) {
            resultsContainer.innerHTML = "<p>No se encontraron libros con ese nombre.</p>";
        } else {
            resultsContainer.innerHTML = data.map(book => `
                <form action="detalle/${book.id}">
                    <button class="button-genero">
                        <img src="${book.photo}">
                        <h3>${book.name}</h3>
                        <p><strong>Autor:</strong> ${book.author}</p>
                        <p><strong>Género:</strong> ${book.genre}</p>
                        <p><strong>Disponible:</strong> ${book.availability_status ? 'Sí' : 'No'}</p>
                        <p><strong>Propietario:</strong> ${book.owner_username}</p>
                    </button>
                </form>
                    
            `).join('');
        }
    } catch (err) {
        alert(`Hubo un error: ${err.message}`);
    }
});