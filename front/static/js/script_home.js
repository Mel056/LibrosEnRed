document.getElementById('searchButton').addEventListener('click', function () {
    const searchInput = document.getElementById('searchInput');
    searchInput.classList.toggle('open');
    searchInput.focus();
});