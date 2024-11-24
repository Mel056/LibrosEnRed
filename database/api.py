from flask import Flask, request, jsonify
from flask_cors import CORS

import mysql.connector

app = Flask(__name__)
CORS(app)  # Esto habilita CORS para todas las rutas

DB_CONFIG = {
    'host': 'localhost',
    'user': 'nacho',
    'password': '123',
    'database': 'LibrosEnRed'
}

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

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    query = """
        INSERT INTO Users (username, email, password, profile_photo) 
        VALUES (%s, %s, %s, %s)
    """
    result = execute_query(query, (data['username'], data['email'], data['password'], data['profile_photo']))
    if "error" in result:
        return jsonify(result), 400
    return jsonify({"message": "User created successfully"}), 201

@app.route('/users', methods=['GET'])
def get_users():
    user_id = request.args.get('id')
    username = request.args.get('username')
    email = request.args.get('email')

    filters = []
    params = []
    if user_id:
        filters.append("id_users = %s")
        params.append(user_id)
    if username:
        filters.append("username LIKE %s")
        params.append(f"%{username}%")
    if email:
        filters.append("email LIKE %s")
        params.append(f"%{email}%")

    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
    query = f"SELECT * FROM Users {where_clause}"

    result = execute_query(query, params)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result), 200

@app.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided to update"}), 400

    updates = []
    params = {'user_id': user_id}
    for key, value in data.items():
        updates.append(f"{key} = %({key})s")
        params[key] = value

    set_clause = ", ".join(updates)
    query = f"UPDATE Users SET {set_clause} WHERE id_users = %(user_id)s"

    result = execute_query(query, params)
    if "error" in result:
        return jsonify(result), 500

    return jsonify({"message": "User updated successfully"}), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    query = "DELETE FROM Users WHERE id_users = %s"
    result = execute_query(query, (user_id,))
    if "error" in result:
        return jsonify(result), 400
    return jsonify({"message": "User deleted successfully"}), 200

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    query = """
        INSERT INTO Books (name_book, author, photo, descripcion, status, genre) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    result = execute_query(query, (data['name_book'], data['author'], data['photo'], data['descripcion'], data['status'], data['genre']))
    if "error" in result:
        return jsonify(result), 400
    return jsonify({"message": "Book created successfully"}), 201

@app.route('/books', methods=['GET'])
def get_books():
    book_id = request.args.get('id')
    genre = request.args.get('genre')
    author = request.args.get('author')
    status = request.args.get('status')
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)

    filters = []
    params = []
    if book_id:
        filters.append("id_books = %s")
        params.append(book_id)
    if genre:
        filters.append("genre LIKE %s")
        params.append(f"%{genre}%")
    if author:
        filters.append("author LIKE %s")
        params.append(f"%{author}%")
    if status:
        filters.append("status = %s")
        params.append(status)

    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
    query = f"SELECT * FROM Books {where_clause} LIMIT %s OFFSET %s"
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

    updates = []
    params = {'book_id': book_id}
    for key, value in data.items():
        updates.append(f"{key} = %({key})s")
        params[key] = value

    set_clause = ", ".join(updates)
    query = f"UPDATE Books SET {set_clause} WHERE id_books = %(book_id)s"

    result = execute_query(query, params)
    if "error" in result:
        return jsonify(result), 500

    return jsonify({"message": "Book updated successfully"}), 200

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    query = "DELETE FROM Books WHERE id_books = %s"
    result = execute_query(query, (book_id,))
    if "error" in result:
        return jsonify(result), 400
    return jsonify({"message": "Book deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
