from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

# Clave Fernet desde el archivo .env
FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY:
    raise ValueError("FERNET_KEY no encontrada en .env")


def encrypt_password(password):
    """
    Encripta una contraseña usando una clave Fernet.

    Args:
        password (str): La contraseña en texto plano.
        fernet_key (bytes): La clave Fernet para encriptar.

    Returns:
        str: La contraseña encriptada.
    """
    fernet = Fernet(FERNET_KEY)
    return fernet.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password):
    """
    Desencripta una contraseña encriptada usando una clave Fernet.

    Args:
        encrypted_password (str): La contraseña encriptada.
        fernet_key (bytes): La clave Fernet para desencriptar.

    Returns:
        str: La contraseña desencriptada en texto plano.
    """
    fernet = Fernet(FERNET_KEY)
    return fernet.decrypt(encrypted_password.encode()).decode()
