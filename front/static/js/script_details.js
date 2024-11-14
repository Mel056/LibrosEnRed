function openMaps() {
    document.getElementById("map-container").style.display = "block";
    document.getElementById("map-overlay").style.display = "block";

    const map = document.getElementById("map");
    const query = encodeURIComponent("Buenos Aires"); 
    map.src = `https://www.google.com/maps?q=${query}&output=embed`;
}

function closeMaps() {
    document.getElementById("map-container").style.display = "none";
    document.getElementById("map-overlay").style.display = "none";
    document.getElementById("map").src = "";
}
