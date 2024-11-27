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

        // Asignar los datos a los elementos del HTML
        const portada = document.getElementById('photo');
        portada.src = libro.photo || 'placeholder.jpg';

        document.getElementById('name_book').textContent = libro.title || 'Título no disponible';
        document.getElementById('author').textContent = libro.author || 'Autor desconocido';
        document.getElementById('genre').textContent = libro.genre || 'Género no especificado';
        document.getElementById('availability_status').textContent = libro.status || 'Estado no disponible';
        document.getElementById('description').textContent = libro.description || 'Sin descripción disponible';
    } catch (error) {
        console.error('Error al cargar los detalles del libro:', error);
    }
}

