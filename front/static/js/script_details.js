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

        const OWNER_ID = libro['owner_id'];

        const container = document.getElementById('book-details-container');
        container.innerHTML = '';

        const userResponse = await fetch(`http://localhost:5001/users?id=${OWNER_ID}`);
        if (!userResponse.ok) {
            throw new Error('Error al cargar los datos del usuario');
        }
        const usuarioJSON = await userResponse.json();
        const usuario = usuarioJSON[0];
        const bookDetailsHTML = `
        <main>
            <div class="book-container">
                <div class="book-cover">
                    <img id="photo" src="${libro['photo'] || 'placeholder.jpg'}" alt="Portada del libro">
                </div>
                
                <div class="book-details">
                    <h1 id="author">${libro['author'] || 'Autor desconocido'}</h1>

                    <h2 id="name_book">${libro['name'] || 'Título no disponible'}</h2>

                    <div class="availability-status">
                        <button class="status-button">${libro['availability_status'] === 1 ? 'Disponible' : 'No disponible'}</button>
                    </div>
                    
                    <div class="book-description">
                        <p id="description">${libro['description'] || 'Sin descripción disponible'}</p>
                    </div>

                    <div class="book-genres">
                        <span id="genre">${libro['genre'] || 'Género no especificado'}</span>
                    </div>
                    <div class="book-owner">
                        <p id="link_perfil">Publicado por: <a href="/visit/${usuario['id']}">${usuario['username'] || 'Usuario desconocido'}</a></p>
                    </div>
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
