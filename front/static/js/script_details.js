function obtenerIdLibro() {
    const path = window.location.pathname;
    const segments = path.split('/');
    const bookId = segments[segments.length - 1];

    if (bookId) {
        console.log('ID del libro:', bookId);
        return bookId;
    } else {
        console.error('No se proporcionó un ID de libro.');
        return null;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const mainSection = document.querySelector('.main');

    if (mainSection) {
        mainSection.addEventListener('wheel', (event) => {
            event.preventDefault();
            mainSection.scrollTop += event.deltaY * 0.5;
        });
    }

    const idLibro = obtenerIdLibro();
    if (idLibro) {
        cargarDetallesLibro(idLibro);
    }
});


async function cargarDetallesLibro(bookId) {
    try {
        const response = await fetch(`http://localhost:5001/books/${bookId}`); // Cambia esto para que apunte a tu API local
        if (!response.ok) {
            throw new Error('Error en la carga de datos');
        }
        const libro = await response.json();

        const portada = document.getElementById('photo')
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


function initMap(latitude, longitude) {
    const map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: latitude, lng: longitude },
        zoom: 12
    });


    new google.maps.Marker({
        position: { lat: latitude, lng: longitude },
        map: map,
        title: 'Ubicación'
    });
}

async function cargarUbicacion() {
    try {
        const response = await fetch('http://localhost:5001/users'); 
        const usuarios = await response.json();


        usuarios.forEach(usuario => {
            const latitude = parseFloat(usuario.latitude);  
            const longitude = parseFloat(usuario.longitude);  

            
            initMap(latitude, longitude);
        });
    } catch (error) {
        console.error('Error al cargar los usuarios:', error);
    }
}


cargarUbicacion();

function openMaps() {
    document.getElementById('map-container').style.display = 'block'; 
    cargarUbicacion(); 
}


function closeMaps() {
    document.getElementById('map-container').style.display = 'none'; 
}

