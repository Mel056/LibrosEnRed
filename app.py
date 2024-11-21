from flask import Flask, render_template, url_for, request, redirect


def main():
    app = Flask(__name__)

    @app.route('/')
    def Home():
        generos = {"Acción", "Arte", "Autoayuda", "Aventuras", "Biografías", "Cocina",
                   "Contemporáneo", "Cs. Ficción", "Distopía", "Divulgativos", "Drama",
                   "Fantasía", "Historia", "Infantil", "Manuales", "Memorias", "Paranormal",
                   "Poesía", "Romance", "Salud", "Suspenso", "Terror"}
        return render_template('home.html', generos=generos)

    @app.route('/Login')
    def Login():
        return render_template('login.html')

    @app.route('/Home/<genero>')
    def Genero(genero):
        return render_template('home.html')

    @app.route('/Detalle/<idLibro>')
    def Detalle(idLibro):
        return render_template('detalle.html')

    @app.route('/CargarLibro')
    def Cargar():
        return render_template('cargar_libro.html')

    @app.route('/Perfil')
    def Perfil():
        return render_template('profile.html')

    app.run(debug=True)


if "__main__" == __name__:
    main()