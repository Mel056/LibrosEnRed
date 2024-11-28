document.addEventListener('DOMContentLoaded', () => {
    const editProfileBtn = document.getElementById('Edit_profile');
    const editProfileModal = document.getElementById('editProfileModal');
    const closeModalBtn = document.querySelector('.close');
    const editProfileForm = document.getElementById('editProfileForm');

    // Función para obtener el userId desde el backend
    async function getUserId() {
        try {
            const response = await fetch('/get-current-user');
            const userData = await response.json();
            return userData.user_id;
        } catch (error) {
            console.error('Error obteniendo ID de usuario:', error);
            return null;
        }
    }

    // Abrir formulario
    editProfileBtn.addEventListener('click', async () => {
        const userId = await getUserId();

        if (!userId) {
            alert('No se pudo obtener el ID de usuario');
            return;
        }

        editProfileModal.style.display = 'block';
    });

    // Cerrar formulario en la X
    closeModalBtn.addEventListener('click', () => {
        editProfileModal.style.display = 'none';
    });

    // Cerrar formulario si se hace click fuera
    window.addEventListener('click', (event) => {
        if (event.target === editProfileModal) {
            editProfileModal.style.display = 'none';
        }
    });

    editProfileForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const userId = await getUserId();

        if (!userId) {
            alert('No se pudo obtener el ID de usuario');
            return;
        }

        const newUsername = document.getElementById('username').value;
        const newProfilePhoto = document.getElementById('googlePhotosLink').value;


        const updateData = {};

        if (newUsername.trim() !== '') {
            updateData.username = newUsername;
        }

        if (newProfilePhoto.trim() !== '') {
            updateData.profile_photo = newProfilePhoto;
        }

        if (Object.keys(updateData).length === 0) {
            alert('No se han realizado cambios');
            return;
        }

        try {
            const response = await fetch(`http://localhost:5001/users/${userId}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updateData)
            });

            const result = await response.json();

            if (response.ok) {
                // Actualiza unicamente lo que fue completado
                if (updateData.username) {
                    document.getElementById('Name_profile').textContent = updateData.username;
                }

                if (updateData.profile_photo) {
                    document.getElementById('Profile').src = updateData.profile_photo;
                }

                // Cierra el formulario
                editProfileModal.style.display = 'none';

                alert('Perfil actualizado exitosamente');
            } else {
                alert('Error al actualizar el perfil: ' + result.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Hubo un problema al actualizar el perfil');
        }
    });
});