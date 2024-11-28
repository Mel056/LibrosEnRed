console.log('Script login started loading');

function getLocation() {
    return new Promise((resolve, reject) => {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    resolve({
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude
                    });
                },
                (error) => {
                    console.warn(`Geolocation error: ${error.message}`);
                    resolve({ latitude: 0, longitude: 0 });
                }
            );
        } else {
            resolve({ latitude: 0, longitude: 0 });
        }
    });
}

function validateForm(type, data) {
    const errors = [];

    if (!data.username || data.username.length < 3) {
        errors.push("El nombre de usuario debe tener al menos 3 caracteres");
    }

    if (type === 'register') {
        if (!data.email || !data.email.includes('@')) {
            errors.push("Introduce un correo electrónico válido");
        }

        if (data.password !== data.confirmPassword) {
            errors.push("Las contraseñas no coinciden");
        }

        if (data.password.length < 6) {
            errors.push("La contraseña debe tener al menos 6 caracteres");
        }
    }

    return errors;
}

async function makeRequest(url, method, data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(url, options);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Error en la solicitud');
        }

        return await response.json();
    } catch (error) {
        console.error('Error en la solicitud:', error);
        throw error;
    }
}

function initializeForms() {
    console.log('Initializing forms...');

    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');
    const container = document.getElementById('container');

    console.log('Found elements:', {
        registerForm: !!registerForm,
        loginForm: !!loginForm,
        container: !!container
    });

    if (!container) {
        console.error('Container element not found');
        return;
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            console.log('Register form submitted');

            const username = document.getElementById('registerUsername').value;
            const email = document.getElementById('registerEmail').value;
            const password = document.getElementById('registerPassword').value;
            const confirmPassword = document.getElementById('confirmPassword').value;

            const formData = {
                username,
                email,
                password,
                confirmPassword
            };

            const validationErrors = validateForm('register', formData);
            if (validationErrors.length > 0) {
                alert(validationErrors.join('\n'));
                return;
            }

            try {
                const { latitude, longitude } = await getLocation();

                const response = await makeRequest('http://localhost:5001/register', 'POST', {
                    username,
                    email,
                    password,
                    latitude,
                    longitude
                });

                alert('Registro exitoso');
                container.classList.remove('sign-up');
                container.classList.add('sign-in');

            } catch (error) {
                alert(error.message || 'Error en registro. Intenta nuevamente.');
            }
        });
    } else {
        console.error('Register form not found');
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            console.log('Login form submitted');

            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;

            const formData = { username, password };
            const validationErrors = validateForm('login', formData);
            if (validationErrors.length > 0) {
                alert(validationErrors.join('\n'));
                return;
            }

            try {
                console.log('Sending login request...');
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username,
                        password
                    })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Error en inicio de sesión');
                }

                console.log('Login successful, redirecting...');
                window.location.href = '/home';

            } catch (error) {
                console.error('Login error:', error);
                alert(error.message || 'Error en inicio de sesión. Intenta nuevamente.');
            }
        });
    } else {
        console.error('Login form not found');
    }
}

// Esta función debe estar disponible globalmente para el onclick
window.toggle = function () {
    console.log('Toggle called');
    const container = document.getElementById('container');
    if (container) {
        container.classList.toggle('sign-in');
        container.classList.toggle('sign-up');
    } else {
        console.error('Container not found for toggle');
    }
};

// Asegurarse de que el DOM esté completamente cargado
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeForms);
} else {
    initializeForms();
}

// Log cuando el script termina de cargar
console.log('Script login finished loading');
