from flask import Flask, request, jsonify
from flask_SQLAlchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root@localhost:3308/LibrosEnREd"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

engine = create_engine("mysql+mysqlconnector://root@localhost:3308/LibrosEnREd")

def run_query(query, parameters=None):
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), parameters)
            conn.commit()
            return result
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users', methods=['POST'])
def new_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    profile_photo = data['profile_photo']
    
    query = """
    INSERT INTO Users (username, email, password, profile_photo)
    VALUES (:username, :email, :password, :profile_photo)
    """
    result = run_query(query, {'username': username, 'email': email, 'password': password, 'profile_photo': profile_photo})
    return jsonify({"message": "User created successfully"}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    query = "SELECT username, email FROM Users WHERE id_users = :user_id"
    result = run_query(query, {'user_id': user_id})
    return jsonify(result.fetchall()), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    query = "SELECT username, email FROM Users"
    result = run_query(query)
    return jsonify(result.fetchall()), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    profile_photo = data['profile_photo']
    
    query = """
    UPDATE Users SET username = :username, email = :email, password = :password, profile_photo = :profile_photo 
    WHERE id_users = :user_id
    """
    run_query(query, {'username': username, 'email': email, 'password': password, 'profile_photo': profile_photo, 'user_id': user_id})
    return jsonify({"message": "User updated successfully"}), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    query = "DELETE FROM Users WHERE id_users = :user_id"
    run_query(query, {'user_id': user_id})
    return jsonify({"message": "User deleted successfully"}), 200



@app.route('/books', methods=['POST'])
def new_book():
    data = request.get_json()
    name_book = data['name_book']
    author = data['author']
    photo = data['photo']
    descripcion = data['descripcion']
    status = data['status']
    genre = data['genre']
    
    query = """
    INSERT INTO Books (name_book, author, photo, descripcion, status, genre)
    VALUES (:name_book, :author, :photo, :descripcion, :status, :genre)
    """
    result = run_query(query, {'name_book': name_book, 'author': author, 'photo': photo, 'descripcion': descripcion, 'status': status, 'genre': genre})
    return jsonify({"message": "Book created successfully"}), 201

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    query = "SELECT name_book, author, photo, descripcion, status, genre FROM Books WHERE id_books = :book_id"
    result = run_query(query, {'book_id': book_id})
    return jsonify(result.fetchall()), 200

@app.route('/books', methods=['GET'])
def get_all_books():
    query = "SELECT name_book, author, photo, descripcion, status, genre FROM Books"
    result = run_query(query)
    return jsonify(result.fetchall()), 200

@app.route('/books/genre/<string:book_genre>', methods=['GET'])
def get_book_by_genre(book_genre):
    query = "SELECT name_book, author, photo, descripcion, status FROM Books WHERE genre = :book_genre"
    result = run_query(query, {'book_genre': book_genre})
    return jsonify(result.fetchall()), 200

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    name_book = data['name_book']
    author = data['author']
    photo = data['photo']
    descripcion = data['descripcion']
    status = data['status']
    genre = data['genre']
    
    query = """
    UPDATE Books SET name_book = :name_book, author = :author, photo = :photo, descripcion = :descripcion, 
    status = :status, genre = :genre WHERE id_books = :book_id
    """
    run_query(query, {'name_book': name_book, 'author': author, 'photo': photo, 'descripcion': descripcion, 'status': status, 'genre': genre, 'book_id': book_id})
    return jsonify({"message": "Book updated successfully"}), 200

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    query = "DELETE FROM Books WHERE id_books = :book_id"
    run_query(query, {'book_id': book_id})
    return jsonify({"message": "Book deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
