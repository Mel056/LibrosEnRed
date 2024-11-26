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

