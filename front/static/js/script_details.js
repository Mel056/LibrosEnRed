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
