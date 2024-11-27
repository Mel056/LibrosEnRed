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
        const libro = await response.json();
        console.log(libro);

        // Get the book-details-container
        const container = document.getElementById('book-details-container');

        // Clear any existing content
        container.innerHTML = '';

        // Create the book details HTML structure
        const bookDetailsHTML = `
            <div class="book-details">
                <div class="book-image">
                    <img id="photo" src="${libro.photo || 'placeholder.jpg'}" alt="Portada del libro" class="book-cover">
                </div>
                
                <div class="book-info">
                    <h1 id="name_book" class="book-title">${libro.title || 'Título no disponible'}</h1>
                    
                    <div class="book-metadata">
                        <p>
                            <strong>Autor:</strong> 
                            <span id="author">${libro.author || 'Autor desconocido'}</span>
                        </p>
                        <p>
                            <strong>Género:</strong> 
                            <span id="genre">${libro.genre || 'Género no especificado'}</span>
                        </p>
                        <p>
                            <strong>Disponibilidad:</strong> 
                            <span id="availability_status" 
                                  class="${libro.status === 'Disponible' ? 'available' : 'unavailable'}">
                                ${libro.status || 'Estado no disponible'}
                            </span>
                        </p>
                    </div>
                    
                    <div class="book-description">
                        <h2>Descripción</h2>
                        <p id="description">${libro.description || 'Sin descripción disponible'}</p>
                    </div>
                    
                    ${libro.status === 'Disponible' ? `
                    <div class="book-actions">
                        <button class="btn-reserve">Reservar</button>
                    </div>
                    ` : ''}
                </div>
            </div>
        `;

        // Insert the generated HTML into the container
        container.innerHTML = bookDetailsHTML;

    } catch (error) {
        console.error('Error al cargar los detalles del libro:', error);

        // Error handling HTML
        const container = document.getElementById('book-details-container');
        container.innerHTML = `
            <div class="error-message">
                <p>No se pudieron cargar los detalles del libro. Por favor, intente nuevamente más tarde.</p>
                <button onclick="window.location.reload()">Reintentar</button>
            </div>
        `;
    }
}