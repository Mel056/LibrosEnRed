document.getElementById('search-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const name = document.getElementById('name').value.trim();

    if (!name) {
        alert("Por favor, ingresa el nombre de un libro para buscar.");
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
                    <button class="detalle-libro">
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

document.getElementById('searchButton').addEventListener('click', function () {
    const resultados = document.getElementById('results');
    resultados.style.visibility = 'visible';
});