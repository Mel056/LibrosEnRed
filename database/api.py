from flask import Flask, request, jsonify
from flask_cors import CORS

import mysql.connector
from encrypt import encrypt_password, decrypt_password

from dotenv import load_dotenv
import os
import boto3
from werkzeug.utils import secure_filename


load_dotenv()

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_REGION = os.getenv("S3_REGION")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")


DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")



app = Flask(__name__)
CORS(app)  # Esto habilita CORS para todas las rutas


DB_CONFIG = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_DATABASE
}



s3_client = boto3.client(
    's3',
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    region_name=S3_REGION
)



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def execute_query(query, params=None, fetch_one=False):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        if query.strip().upper().startswith("SELECT"):
            return cursor.fetchone() if fetch_one else cursor.fetchall()
        connection.commit()
        return {"message": "Success"}
    except mysql.connector.Error as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/upload/profile-photo/<int:user_id>', methods=['POST'])
def upload_profile_photo(user_id):
    # Verificar si el usuario existe
    user = execute_query("SELECT id FROM Users WHERE id = %s", (user_id,), fetch_one=True)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Verificar si hay archivo en la solicitud
    if 'file' not in request.files:
        return jsonify({
            "error": "No file provided",
            "detail": "Make sure to use 'file' as the key name in form-data",
            "received_keys": list(request.files.keys())
        }), 400

    file = request.files['file']

    # Validar formato del archivo
    if file.filename == '':
        return jsonify({
            "error": "No selected file",
            "detail": "Filename is empty"
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": "Invalid file type",
            "detail": f"Allowed extensions are: {ALLOWED_EXTENSIONS}",
            "received_file": file.filename
        }), 400

    # Asegurar el nombre del archivo
    filename = secure_filename(file.filename)

    # Subir a S3
    try:
        s3_client.upload_fileobj(
            file,
            S3_BUCKET_NAME,
            filename,
            ExtraArgs={"ContentType": file.content_type}
        )

    except Exception as e:
        return jsonify({
            "error": "Failed to upload to S3",
            "detail": str(e)
        }), 500

    # Obtener la URL pública
    file_url = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{filename}"

    # Guardar URL en el perfil del usuario
    query = "UPDATE Users SET profile_photo = %s WHERE id = %s"
    result = execute_query(query, (file_url, user_id))
    
    if "error" in result:
        return jsonify({
            "error": "Failed to update user profile",
            "detail": result["error"]
        }), 500

    return jsonify({
        "message": "Profile photo uploaded successfully",
        "file_url": file_url
    }), 200



@app.route('/upload/book-photo/<int:book_id>', methods=['POST'])
def upload_book_photo(book_id):
    # Verificar si el libro existe
    book = execute_query("SELECT id FROM Books WHERE id = %s", (book_id,), fetch_one=True)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    # Verificar si hay archivo en la solicitud
    if 'file' not in request.files:
        return jsonify({
            "error": "No file provided",
            "detail": "Make sure to use 'file' as the key name in form-data",
            "received_keys": list(request.files.keys())
        }), 400

    file = request.files['file']

    # Validar formato del archivo
    if file.filename == '':
        return jsonify({
            "error": "No selected file",
            "detail": "Filename is empty"
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": "Invalid file type",
            "detail": f"Allowed extensions are: {ALLOWED_EXTENSIONS}",
            "received_file": file.filename
        }), 400

    # Asegurar el nombre del archivo
    filename = secure_filename(file.filename)

    # Subir a S3
    try:
        s3_client.upload_fileobj(
            file,
            S3_BUCKET_NAME,
            filename,
            ExtraArgs={"ContentType": file.content_type}
        )

    except Exception as e:
        return jsonify({
            "error": "Failed to upload to S3",
            "detail": str(e)
        }), 500

    # Obtener la URL pública
    file_url = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{filename}"

    # Guardar URL en la foto del libro
    query = "UPDATE Books SET photo = %s WHERE id = %s"
    result = execute_query(query, (file_url, book_id))
    
    if "error" in result:
        return jsonify({
            "error": "Failed to update book photo",
            "detail": result["error"]
        }), 500

    return jsonify({
        "message": "Book photo uploaded successfully",
        "file_url": file_url
    }), 200



@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    
    # Verificar campos requeridos
    required_fields = ['username', 'email', 'password', 'latitude', 'longitude']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Verificar si el username o email ya existen (optimizado en una sola consulta)
    check_user_query = "SELECT username, email FROM Users WHERE username = %s OR email = %s"
    user_result = execute_query(check_user_query, (data['username'], data['email']))
    
    if user_result:
        for user in user_result:
            if user['username'] == data['username']:
                return jsonify({"error": "El nombre de usuario ya está registrado"}), 409
            if user['email'] == data['email']:
                return jsonify({"error": "El correo electrónico ya está registrado"}), 409

    # Encriptar la contraseña
    encrypted_password = encrypt_password(data['password'])

    # Registrar al usuario
    query = """
        INSERT INTO Users (
            username, 
            email, 
            password, 
            latitude, 
            longitude, 
            profile_photo,
            average_rating
        ) VALUES (%s, %s, %s, %s, %s, NULL, 0.00)
    """
    result = execute_query(query, (
        data['username'], 
        data['email'], 
        encrypted_password, 
        data['latitude'], 
        data['longitude']
    ))
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify({"message": "User registered successfully"}), 201



@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    
    required_fields = ['username', 'password']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Actualizamos el nombre del campo id y obtenemos datos adicionales útiles
    query = """
        SELECT 
            id,
            username, 
            password,
            email,
            profile_photo,
            average_rating
        FROM Users 
        WHERE username = %s
    """
    user = execute_query(query, (data['username'],), fetch_one=True)
    
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    # Desencriptar y comparar contraseñas
    try:
        decrypted_password = decrypt_password(user['password'])
        if decrypted_password != data['password']:
            return jsonify({"error": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"error": "Password decryption failed"}), 500

    # Devolvemos información adicional útil para la sesión del usuario
    return jsonify({
        "message": "Login successful",
        "user_id": user['id'],
        "username": user['username'],
        "email": user['email'],
        "profile_photo": user['profile_photo'],
        "average_rating": float(user['average_rating']) if user['average_rating'] else 0.00
    }), 200



@app.route('/users', methods=['GET'])
def get_users():
    # Obtener parámetros de búsqueda
    user_id = request.args.get('id')
    username = request.args.get('username')
    email = request.args.get('email')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    profile_photo = request.args.get('profile_photo')

    # Construir filtros
    filters = []
    params = []
    if user_id:
        filters.append("u.id = %s")
        params.append(user_id)
    if username:
        filters.append("u.username LIKE %s")
        params.append(f"%{username}%")
    if email:
        filters.append("u.email LIKE %s")
        params.append(f"%{email}%")
    if latitude:
        filters.append("u.latitude = %s")
        params.append(latitude)
    if longitude:
        filters.append("u.longitude = %s")
        params.append(longitude)
    if profile_photo is not None:
        filters.append("u.profile_photo IS NOT NULL" if profile_photo == 'true' else "u.profile_photo IS NULL")
    
    # Construir la consulta principal con subconsultas optimizadas
    query = """
    SELECT 
        u.id,
        u.username,
        u.email,
        u.profile_photo,
        u.latitude,
        u.longitude,
        u.created_at,
        u.average_rating,
        (
            SELECT JSON_ARRAYAGG(
                JSON_OBJECT(
                    'comment_id', c.id,
                    'commenter_username', cu.username,
                    'comment', c.comment,
                    'created_at', c.created_at
                )
            )
            FROM UserComments c
            JOIN Users cu ON cu.id = c.commenter_id
            WHERE c.receiver_id = u.id
        ) as received_comments,
        (
            SELECT COUNT(*)
            FROM Books b
            WHERE b.owner_id = u.id
        ) as total_books
    FROM Users u
    """

    # Agregar filtros si existen
    if filters:
        query += " WHERE " + " AND ".join(filters)

    # Agregar ordenamiento
    query += " ORDER BY u.username ASC"

    # Ejecutar la consulta
    result = execute_query(query, params)
    if "error" in result:
        return jsonify(result), 400

    # Procesar los resultados para manejar valores NULL en JSON_ARRAYAGG
    for user in result:
        if user['received_comments'] is None:
            user['received_comments'] = []
            
    return jsonify(result), 200



@app.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided to update"}), 400

    # Campos permitidos para actualización
    allowed_fields = {
        'username', 'email', 'password', 'profile_photo', 
        'latitude', 'longitude'
    }

    # Filtrar campos no permitidos
    invalid_fields = set(data.keys()) - allowed_fields
    if invalid_fields:
        return jsonify({
            "error": f"Invalid fields: {', '.join(invalid_fields)}"
        }), 400

    # Si se actualiza username o email, verificar que no existan
    if 'username' in data or 'email' in data:
        check_query = "SELECT username, email FROM Users WHERE id != %s AND (username = %s OR email = %s)"
        check_params = (
            user_id,
            data.get('username', ''),
            data.get('email', '')
        )
        existing = execute_query(check_query, check_params)
        
        if existing:
            for user in existing:
                if 'username' in data and user['username'] == data['username']:
                    return jsonify({"error": "Username already exists"}), 409
                if 'email' in data and user['email'] == data['email']:
                    return jsonify({"error": "Email already exists"}), 409

    # Construir la consulta de actualización
    updates = []
    params = {'user_id': user_id}
    
    for key, value in data.items():
        if key == 'password':
            value = encrypt_password(value)
        updates.append(f"{key} = %({key})s")
        params[key] = value

    set_clause = ", ".join(updates)
    query = f"UPDATE Users SET {set_clause} WHERE id = %(user_id)s"

    result = execute_query(query, params)
    if "error" in result:
        return jsonify(result), 500

    return jsonify({
        "message": "User updated successfully",
        "updated_fields": list(data.keys())
    }), 200



@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Verificar que el usuario existe antes de eliminarlo
    check_query = "SELECT id FROM Users WHERE id = %s"
    user = execute_query(check_query, (user_id,), fetch_one=True)
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Gracias a las restricciones ON DELETE CASCADE, 
    # esto eliminará automáticamente los registros relacionados
    query = "DELETE FROM Users WHERE id = %s"
    result = execute_query(query, (user_id,))
    
    if "error" in result:
        return jsonify(result), 400
        
    return jsonify({"message": "User deleted successfully"}), 200



@app.route('/books', methods=['POST'])
def create_book():
    # Verificar si hay archivo en la solicitud
    if 'photo' in request.files:
        file = request.files['photo']
        # Validar formato del archivo
        if file.filename != '' and allowed_file(file.filename):
            # Asegurar el nombre del archivo
            filename = secure_filename(file.filename)
            try:
                # Subir a S3
                s3_client.upload_fileobj(
                    file,
                    S3_BUCKET_NAME,
                    filename,
                    ExtraArgs={"ContentType": file.content_type}
                )
                # Generar URL de la foto
                photo_url = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{filename}"
            except Exception as e:
                return jsonify({
                    "error": "Failed to upload photo to S3",
                    "detail": str(e)
                }), 500
        else:
            photo_url = None
    else:
        photo_url = None

    # Obtener datos del formulario
    try:
        name = request.form.get('name')
        author = request.form.get('author')
        owner_id = int(request.form.get('owner_id'))
        genre = request.form.get('genre')
        description = request.form.get('description')
    except Exception as e:
        return jsonify({
            "error": "Failed to parse form data",
            "detail": str(e)
        }), 400

    # Verificar campos requeridos
    if not all([name, author, owner_id, genre]):
        return jsonify({
            "error": "Missing required fields",
            "detail": "name, author, owner_id, and genre are required"
        }), 400

    # Verificar que el owner_id es un número
    try:
        owner_id = int(owner_id)
    except ValueError:
        return jsonify({
            "error": "Invalid owner_id",
            "detail": "owner_id must be a number"
        }), 400
        
    # Verificar que el propietario existe
    check_owner = "SELECT id FROM Users WHERE id = %s"
    owner = execute_query(check_owner, (owner_id,), fetch_one=True)
    if not owner:
        return jsonify({"error": "Owner not found"}), 404

    # Crear el libro
    query = """
        INSERT INTO Books (
            name,
            author, 
            photo, 
            description, 
            availability_status,
            genre,
            owner_id,
            average_rating,
            created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
    """
    
    result = execute_query(query, (
        name,
        author,
        photo_url,
        description,
        True,  # availability_status siempre será True
        genre,
        owner_id,
        0.00
    ))
    
    if "error" in result:
        return jsonify(result), 400
        
    return jsonify({
        "message": "Book created successfully",
        "book_id": result.get('last_id'),
        "photo_url": photo_url
    }), 201


@app.route('/books', methods=['GET'])
def get_books():
   book_id = request.args.get('id')
   genre = request.args.get('genre')
   author = request.args.get('author') 
   availability_status = request.args.get('availability_status')
   owner_id = request.args.get('owner_id')
   name = request.args.get('name')
   limit = request.args.get('limit', 100, type=int)
   offset = request.args.get('offset', 0, type=int)

   # Construir filtros
   filters = []
   params = []
   if book_id:
       filters.append("b.id = %s")
       params.append(book_id)
   if genre:
       filters.append("b.genre LIKE %s")
       params.append(f"%{genre}%")
   if author:
       filters.append("b.author LIKE %s")
       params.append(f"%{author}%")
   if availability_status is not None:
       filters.append("b.availability_status = %s")
       params.append(availability_status.lower() == 'true')
   if owner_id:
       filters.append("b.owner_id = %s")
       params.append(owner_id)
   if name:
       filters.append("b.name = %s")
       params.append(name)

   # Construir consulta con información adicional
   query = """
       SELECT 
           b.id,
           b.name,
           b.author,
           b.photo,
           b.description,
           b.availability_status,
           b.genre,
           b.created_at,
           b.average_rating,
           b.owner_id,
           u.username as owner_username,
           u.average_rating as owner_rating,
           (
               SELECT COUNT(*) 
               FROM BookRatings br 
               WHERE br.book_id = b.id
           ) as total_ratings
       FROM Books b
       JOIN Users u ON u.id = b.owner_id
   """

   # Agregar filtros si existen
   if filters:
       query += " WHERE " + " AND ".join(filters)

   # Agregar ordenamiento y paginación
   query += " ORDER BY b.created_at DESC LIMIT %s OFFSET %s"
   params.extend([limit, offset])

   result = execute_query(query, params)
   if "error" in result:
       return jsonify(result), 400

   return jsonify(result), 200



@app.route('/books/<int:book_id>', methods=['PATCH'])
def update_book(book_id):
   data = request.get_json()

   if not data:
       return jsonify({"error": "No data provided to update"}), 400

   # Verificar que el libro existe
   check_query = "SELECT id, owner_id FROM Books WHERE id = %s"
   book = execute_query(check_query, (book_id,), fetch_one=True)
   
   if not book:
       return jsonify({"error": "Book not found"}), 404

   # Definir campos permitidos
   allowed_fields = {
       'name', 'author', 'photo', 'description', 
       'availability_status', 'genre'
   }

   # Filtrar campos no permitidos
   invalid_fields = set(data.keys()) - allowed_fields
   if invalid_fields:
       return jsonify({
           "error": f"Invalid fields: {', '.join(invalid_fields)}"
       }), 400

   # Construir la consulta
   updates = []
   params = {'book_id': book_id}
   
   for key, value in data.items():
       updates.append(f"{key} = %({key})s")
       params[key] = value

   set_clause = ", ".join(updates)
   query = f"UPDATE Books SET {set_clause} WHERE id = %(book_id)s"

   result = execute_query(query, params)
   if "error" in result:
       return jsonify(result), 500

   return jsonify({
       "message": "Book updated successfully",
       "updated_fields": list(data.keys())
   }), 200



@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
   # Verificar que el libro existe
   check_query = "SELECT id FROM Books WHERE id = %s"
   book = execute_query(check_query, (book_id,), fetch_one=True)
   
   if not book:
       return jsonify({"error": "Book not found"}), 404

   # Eliminar el libro (los ratings se eliminarán automáticamente por el ON DELETE CASCADE)
   query = "DELETE FROM Books WHERE id = %s"
   result = execute_query(query, (book_id,))
   
   if "error" in result:
       return jsonify(result), 400
       
   return jsonify({"message": "Book deleted successfully"}), 200



@app.route('/rating/books', methods=['POST'])
def rate_book():
   data = request.get_json()
   
   # Verificar campos requeridos
   required_fields = ['book_id', 'rater_id', 'rating']
   missing_fields = [field for field in required_fields if field not in data]
   if missing_fields:
       return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400
       
   # Verificar que el rating esté entre 1 y 5
   if not 1 <= data['rating'] <= 5:
       return jsonify({"error": "Rating must be between 1 and 5"}), 400

   # Verificar que el libro existe
   book_query = "SELECT id FROM Books WHERE id = %s"
   book = execute_query(book_query, (data['book_id'],), fetch_one=True)
   if not book:
       return jsonify({"error": "Book not found"}), 404

   # Verificar que el usuario existe
   user_query = "SELECT id FROM Users WHERE id = %s"
   user = execute_query(user_query, (data['rater_id'],), fetch_one=True)
   if not user:
       return jsonify({"error": "User not found"}), 404

   # Verificar si ya existe un rating para este usuario y libro
   check_query = """
       SELECT id FROM BookRatings 
       WHERE book_id = %s AND rater_id = %s
   """
   existing_rating = execute_query(check_query, (data['book_id'], data['rater_id']), fetch_one=True)

   if existing_rating:
       # Actualizar el rating existente
       update_query = """
           UPDATE BookRatings 
           SET rating = %s 
           WHERE book_id = %s AND rater_id = %s
       """
       result = execute_query(update_query, (
           data['rating'], 
           data['book_id'], 
           data['rater_id']
       ))
   else:
       # Crear nuevo rating
       insert_query = """
           INSERT INTO BookRatings (book_id, rater_id, rating, created_at)
           VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
       """
       result = execute_query(insert_query, (
           data['book_id'], 
           data['rater_id'], 
           data['rating']
       ))

   if "error" in result:
       return jsonify(result), 400

   # El promedio se actualiza automáticamente por el trigger

   return jsonify({
       "message": "Rating saved successfully",
       "book_id": data['book_id'],
       "rating": data['rating']
   }), 200



@app.route('/books/<int:book_id>/rating', methods=['GET'])
def get_book_rating(book_id):
   # Verificar que el libro existe
   book_query = "SELECT id FROM Books WHERE id = %s"
   book = execute_query(book_query, (book_id,), fetch_one=True)
   
   if not book:
       return jsonify({"error": "Book not found"}), 404

   # Obtener estadísticas de rating
   query = """
       SELECT 
           b.id,
           b.name,
           b.average_rating,
           COUNT(br.id) as total_ratings,
           JSON_ARRAYAGG(
               JSON_OBJECT(
                   'rating', br.rating,
                   'rater_id', br.rater_id,
                   'rater_name', u.username,
                   'created_at', br.created_at
               )
           ) as ratings_detail
       FROM Books b
       LEFT JOIN BookRatings br ON b.id = br.book_id
       LEFT JOIN Users u ON br.rater_id = u.id
       WHERE b.id = %s
       GROUP BY b.id
   """
   
   result = execute_query(query, (book_id,), fetch_one=True)

   # Procesar el resultado
   if result['ratings_detail'] is None:
       result['ratings_detail'] = []

   return jsonify({
       "book_id": book_id,
       "book_name": result['name'],
       "average_rating": float(result['average_rating']) if result['average_rating'] else 0,
       "total_ratings": result['total_ratings'],
       "ratings_detail": result['ratings_detail']
   }), 200



@app.route('/exchange/request', methods=['POST'])
def request_exchange():
    data = request.get_json()
    
    # Verificar campos requeridos
    required_fields = ['book_id', 'requesting_user_id']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Verificar que el libro exista y obtener la información del dueño
    book_query = """
        SELECT 
            b.id,
            b.owner_id,
            b.availability_status,
            b.name as book_name,
            u.username as owner_username
        FROM Books b
        JOIN Users u ON b.owner_id = u.id
        WHERE b.id = %s
    """
    book_result = execute_query(book_query, (data['book_id'],), fetch_one=True)
    
    if not book_result:
        return jsonify({"error": "Book not found"}), 404
        
    if not book_result['availability_status']:
        return jsonify({"error": "Book is not available for exchange"}), 400

    # Verificar que el solicitante exista
    requester_query = "SELECT id, username FROM Users WHERE id = %s"
    requester = execute_query(requester_query, (data['requesting_user_id'],), fetch_one=True)
    
    if not requester:
        return jsonify({"error": "Requesting user not found"}), 404

    # Verificar que el solicitante no sea el mismo dueño
    if data['requesting_user_id'] == book_result['owner_id']:
        return jsonify({"error": "Cannot request exchange with yourself"}), 400

    # Verificar si ya existe una solicitud pendiente
    check_existing_query = """
        SELECT id FROM BookExchanges 
        WHERE book_id = %s 
        AND requester_id = %s 
        AND status = 'completed'
    """
    existing_request = execute_query(
        check_existing_query, 
        (data['book_id'], data['requesting_user_id']),
        fetch_one=True
    )
    
    if existing_request:
        return jsonify({"error": "An exchange request already exists for this book"}), 409

    # Crear el intercambio como completado directamente
    exchange_query = """
        INSERT INTO BookExchanges (
            book_id,
            requester_id,
            owner_id,
            status
        ) VALUES (%s, %s, %s, 'completed')
    """
    result = execute_query(exchange_query, (
        data['book_id'],
        data['requesting_user_id'],
        book_result['owner_id']
    ))
    
    if "error" in result:
        return jsonify(result), 400

    # Actualizar el owner_id y estado del libro
    update_book_query = """
        UPDATE Books 
        SET availability_status = TRUE, 
            owner_id = %s
        WHERE id = %s
    """
    execute_query(update_book_query, (data['requesting_user_id'], data['book_id']))

    return jsonify({
        "message": "Exchange completed successfully",
        "exchange_details": {
            "exchange_id": result.get('last_id'),
            "book": {
                "id": book_result['id'],
                "name": book_result['book_name']
            },
            "owner": {
                "id": book_result['owner_id'],
                "username": book_result['owner_username']
            },
            "requester": {
                "id": requester['id'],
                "username": requester['username']
            },
            "status": "completed"
        }
    }), 201



@app.route('/users/comments', methods=['POST'])
def add_user_comment():
    data = request.get_json()
    
    # Verificar campos requeridos
    required_fields = ['receiver_id', 'commenter_id', 'comment']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Verificar que el usuario que recibirá el comentario existe
    receiver_query = "SELECT id FROM Users WHERE id = %s"
    receiver = execute_query(receiver_query, (data['receiver_id'],), fetch_one=True)
    if not receiver:
        return jsonify({"error": "Receiver user not found"}), 404

    # Verificar que el usuario que comenta existe
    commenter_query = "SELECT id, username FROM Users WHERE id = %s"
    commenter = execute_query(commenter_query, (data['commenter_id'],), fetch_one=True)
    if not commenter:
        return jsonify({"error": "Commenter user not found"}), 404

    # Verificar que el usuario no se comente a sí mismo
    if data['receiver_id'] == data['commenter_id']:
        return jsonify({"error": "Users cannot comment on their own profile"}), 400

    # Insertar el comentario
    insert_query = """
        INSERT INTO UserComments (
            receiver_id,
            commenter_id,
            comment,
            created_at
        ) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
    """
    
    result = execute_query(insert_query, (
        data['receiver_id'],
        data['commenter_id'],
        data['comment']
    ))
    
    if "error" in result:
        return jsonify(result), 400

    return jsonify({
        "message": "Comment added successfully",
        "comment_details": {
            "comment_id": result.get('last_id'),
            "receiver_id": data['receiver_id'],
            "commenter": {
                "id": commenter['id'],
                "username": commenter['username']
            },
            "comment": data['comment'],
            "created_at": "now"  # La base de datos maneja el timestamp real
        }
    }), 201



if __name__ == '__main__':
    app.run(debug=True, port=5001)
