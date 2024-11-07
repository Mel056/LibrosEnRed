from flask import Flask, render_template, url_for, request, redirect


def main():
    app = Flask(__name__)

    @app.route('/')
    def Home():
        return render_template('home.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    app.run(debug=True)


if "__main__" == __name__:
    main()
