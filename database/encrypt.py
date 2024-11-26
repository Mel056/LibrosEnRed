from cryptography.fernet import Fernet


def encrypt_password(password, fernet_key):
    """
    Encripta una contraseña usando una clave Fernet.

    Args:
        password (str): La contraseña en texto plano.
        fernet_key (bytes): La clave Fernet para encriptar.

    Returns:
        str: La contraseña encriptada.
    """
    fernet = Fernet(fernet_key)
    return fernet.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password, fernet_key):
    """
    Desencripta una contraseña encriptada usando una clave Fernet.

    Args:
        encrypted_password (str): La contraseña encriptada.
        fernet_key (bytes): La clave Fernet para desencriptar.

    Returns:
        str: La contraseña desencriptada en texto plano.
    """
    fernet = Fernet(fernet_key)
    return fernet.decrypt(encrypted_password.encode()).decode()
