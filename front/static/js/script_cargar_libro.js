document.getElementById('bookForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this); // Esto incluye automáticamente el archivo

    // No es necesario crear un objeto data, ya que FormData maneja todo
    fetch('http://127.0.0.1:5001/books', {
        method: 'POST',
        body: formData  // Enviar el FormData directamente
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Completado:', data);
        alert('Carga de libro exitosa');
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Error al cargar el libro. Verifique los datos cargados');
    });
});