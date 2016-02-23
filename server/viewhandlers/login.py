
from flask import render_template, session, request ,redirect , url_for
from server import app


@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
def index():
    return render_template("index.html",
        title = 'Home')


@app.route('/login', methods = ['GET'])
def login():
    if 'username' in session and 'password' in session:
        return render_template("loginalready.html",name = session['username'])
    else :
        return render_template("login.html" )


@app.route('/signup', methods = ['POST'])
def signup():
    if 'username' in request.form and 'password' in request.form:
        session['username'] = request.form['username']
        session['password'] = request.form['password']

    return redirect(url_for('login'))


@app.route('/logout', methods = ['POST'])
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('login'))
