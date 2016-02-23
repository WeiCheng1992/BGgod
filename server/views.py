from flask import render_template
from server import app
from server.forms import LoginForm


@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
def index():
    user = {'nickname': 'Charles'}
    return render_template("index.html",
        title = 'Home',
        user = user)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html',
        title = 'Sign In',
        form = form)


def launch():
    app.run(debug=True, port=12138)

