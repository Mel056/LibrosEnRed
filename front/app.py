from flask import Flask, render_template, url_for, request,redirect

def main():
    app = Flask(__name__)

    @app.route('/')
    def Home():
        generos = {"Acción", "Arte", "Autoayuda", "Aventuras", "Biografías", "Cocina",
                   "Contemporáneo", "Cs. Ficción", "Distopía", "Divulgativos", "Drama",
                   "Fantasía", "Historia", "Infantil", "Manuales", "Memorias", "Paranormal",
                   "Poesía", "Romance", "Salud", "Suspenso", "Terror"}
        return render_template('home.html', generos=generos)

    @app.route('/login', methods=['GET', 'POST'])
    def Login():
        return render_template('login.html')



    @app.route('/register', methods=['GET'])
    def register_page():
        return render_template('login.html')
    

    @app.route('/home/<genero>')
    def Genero(genero):
        return render_template('base.html')


    @app.route('/detalle/<int:idLibro>')
    def Detalle(idLibro):
        return render_template('detalle.html', idLibro=idLibro)

    @app.route('/cargar_libro')
    def Cargar():
        return render_template('cargar_libro.html')


    @app.route('/perfil')
    def Perfil():
        try:
            #Integrar autenticacion de sesion   
            user_id = 1  
            response = request.get(f'http://localhost:5001/users?id={user_id}')

            if response.status_code == 200:
                user_data = response.json()[0] 
                return render_template('profile.html', user=user_data)
            else:
                return render_template('profile.html', user=None, error="Usuario no encontrado")
        except Exception as e:
            return render_template('profile.html', user=None, error=str(e))



    app.run(debug=True)


if "__main__" == __name__:
    main()
