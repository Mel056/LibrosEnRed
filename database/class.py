from cryptography.fernet import Fernet
import mysql.connector

def generate_fernet_key():
    return Fernet.generate_key()

def store_fernet_key(user_id, fernet_key):
    conn = mysql.connector.connect(
        host='localhost',          
        user='leo',               
        password='123',  
        database='LibrosEnRed'     
    )
    cursor = conn.cursor()

    
    cursor.execute(""" INSERT INTO Users_keys (users_id, fernet_key) VALUES (%s, %s)
    """, (user_id, fernet_key))

    conn.commit()
    conn.close()


user_id = 1  
new_fernet_key = generate_fernet_key()


store_fernet_key(user_id, new_fernet_key)

print(f"Clave de Fernet almacenada para el usuario {user_id}.")
