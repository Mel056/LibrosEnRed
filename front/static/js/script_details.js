const pathname = window.location.pathname;
const bookId = pathname.split('/')[2];

if (bookId) {
    cargarDetallesLibro(bookId);
} else {
    console.error("No se encontró el id del libro en la URL");
}

async function cargarDetallesLibro(bookId) {
    try {
        const response = await fetch(`http://localhost:5001/books?id=${bookId}`);
        if (!response.ok) {
            throw new Error('Error en la carga de datos');
        }
        const libroJSON = await response.json();
        const libro = libroJSON[0]
        console.log(libro);

        const container = document.getElementById('book-details-container');
        container.innerHTML = ''; 

        const bookDetailsHTML = `
        <main>
            <div class="book-container">
                <div class="book-cover">
                    <img id="photo" src="${libro['photo'] || 'placeholder.jpg'}" alt="Portada del libro">
                </div>
                <div class="book-details">
                    <h1 id="name_book">${libro['title'] || 'Título no disponible'}</h1>
                    <h2 id="author">${libro['author'] || 'Autor desconocido'}</h2>
                    
                    <div class="book-genres">
                        <span id="genre">${libro['genre'] || 'Género no especificado'}</span>
                    </div>
                    
                    <div class="book-description">
                        <p id="description">${libro['description'] || 'Sin descripción disponible'}</p>
                    </div>
                    
                    ${libro['status'] === 'Disponible' ? `
                    <button id="reserve-btn" class="exchange-button">Reservar</button>
                    ` : `
                    <p class="unavailable"><strong>Estado:</strong> No disponible</p>
                    `}
                </div>
            </div>
        </main>
        `;

        container.innerHTML = bookDetailsHTML;
    
    } catch (error) {
        console.error('Error al cargar los detalles del libro:', error);

        const container = document.getElementById('book-details-container');
        container.innerHTML = `
            <div class="error-message">
                <p>No se pudieron cargar los detalles del libro. Por favor, intente nuevamente más tarde.</p>
                <button onclick="window.location.reload()">Reintentar</button>
            </div>
        `;
    }
}
