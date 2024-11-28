from flask import Flask, render_template, url_for, request, redirect, session, jsonify
from functools import wraps
import requests

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))  # Cambiado de 'Login' a 'login'
        return f(*args, **kwargs)
    return decorated_function

def main():
    app = Flask(__name__)
    
    app.secret_key = 'tu_clave_secreta_aqui'


    @app.route('/')
    def index():
        return redirect(url_for('login'))

    @app.route('/home')
    @login_required
    def home():  # Cambiado de Home a home
        generos = {"Fiction", "Non-Fiction", "Mystery", "Science Fiction", 
                  "Fantasy", "Romance", "Thriller", "Horror", "Biography",
                  "Historical Fiction", "Young Adult", "Children's"}
        try:
            response = requests.get(f'http://localhost:5001/books')
            if response.status_code == 200:
                libros = response.json()
                return render_template('home.html', libros=libros, generos=generos)
            else:
                return render_template('home.html', libros=None, generos=generos, error="Libros no encontrados")
        except Exception as e:
            return render_template('home.html', libros=None, error=str(e))

    @app.route('/login', methods=['GET', 'POST'])
    def login():  # Cambiado de Login a login
        if 'user_id' in session:
            return redirect(url_for('home'))  # Cambiado de Home a home
        
        if request.method == 'POST':
            try:
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')

                response = requests.post('http://localhost:5001/login', 
                    json={
                        'username': username,
                        'password': password
                    })
                
                if response.status_code == 200:
                    data = response.json()
                    session['user_id'] = data['user_id']
                    session['username'] = data['username']
                    session['email'] = data.get('email')
                    session['profile_photo'] = data.get('profile_photo')
                    return jsonify({'success': True}), 200
                else:
                    return jsonify({'error': 'Credenciales inválidas'}), 401
                    
            except Exception as e:
                return jsonify({'error': str(e)}), 500
                
        return render_template('login.html')

    @app.route('/register', methods=['GET'])
    def register():  # Cambiado de register_page a register
        return render_template('login.html')
    
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))  # Cambiado de Login a login

    @app.route('/home/<cat>')
    @login_required
    def genero(cat):  # Cambiado de Genero a genero
        try:
            response = requests.get(f'http://localhost:5001/books?genre={cat}')
            if response.status_code == 200:
                libros = response.json()
                return render_template('base.html', libros=libros)
            else:
                return render_template('base.html', libros=None , error="Libros no encontrados")
        except Exception as e:
            return render_template('base.html', libros=None, error=str(e))

    @app.route('/detalle/<int:idLibro>')
    @login_required
    def detalle(idLibro):  # Cambiado de Detalle a detalle
        try:
            print('id libro', idLibro)
            response = requests.get(f'http://localhost:5001/books?id={idLibro}')
            print(response.json())
            print(response.status_code)
            if response.status_code == 200:
                book_data = response.json()[0]  
                return render_template('detalle.html', libro=book_data)
            else:
                return render_template('detalle.html', libro=None, error="Libro no encontrado")
        except Exception as e:
            return render_template('detalle.html', libro=None, error=str(e))

    @app.route('/cargar_libro')
    @login_required
    def cargar():  # Cambiado de Cargar a cargar
        return render_template('cargar_libro.html')

    @app.route('/perfil')
    @login_required
    def perfil():
        try:
            user_id = session.get('user_id')
            response = requests.get(f'http://localhost:5001/books?owner_id={user_id}')
            user_response = requests.get(f'http://localhost:5001/users?id={user_id}')
            
            if user_response.status_code == 200:
                user_data = user_response.json()[0]
            else:
                user_data = None

            if response.status_code == 200:
                libros = response.json()
                return render_template('profile.html', user=user_data, libros=libros, user_id=user_id)
            else:
                return render_template('profile.html', user=user_data, libros=None, error="Libros no encontrados", user_id=user_id)
        except Exception as e:
            return render_template('profile.html', user=None, libros=None, error=str(e))

    @app.route('/get-current-user')
    @login_required
    def get_current_user():
        return jsonify({
            'user_id': session.get('user_id')
        })

    return app  # Retornamos la app en lugar de ejecutarla

if __name__ == "__main__":
    app = main()
    app.run(debug=True)
