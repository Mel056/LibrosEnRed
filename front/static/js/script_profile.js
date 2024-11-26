document.addEventListener('DOMContentLoaded', () => {
    const mainSection = document.querySelector('.main');

    mainSection.addEventListener('wheel', (event) => {
        event.preventDefault();
        mainSection.scrollTop += event.deltaY * 0.5;
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const mainSection = document.querySelector('#comments');

    mainSection.addEventListener('wheel', (event) => {
        event.preventDefault();
        mainSection.scrollTop += event.deltaY * 0.5;
    });
});

async function cargarPerfil(userId) {
    try {
        // Validar que se proporcione un ID de usuario
        if (!userId) {
            throw new Error('Se requiere un ID de usuario');
        }

        const response = await fetch(`http://localhost:5001/users?id=${userId}`);

        if (!response.ok) {
            throw new Error('Error al obtener datos del perfil');
        }

        const usuarios = await response.json();

        if (usuarios.length > 0) {
            const usuario = usuarios[0];

            const nombrePerfil = document.getElementById('Name_profile');
            nombrePerfil.textContent = usuario.username || 'Nombre de Usuario';

            const profileImg = document.getElementById('Profile');
            profileImg.src = usuario.profile_photo || "{{ url_for('static', filename='images/Perfil.jpg') }}";
        }
    } catch (error) {
        console.error('Error al cargar el perfil:', error);
    }
}

