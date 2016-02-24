
from flask import render_template, session, request ,redirect , url_for ,flash
from server import app




@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
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
    else:
        flash('login fail')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    print request.method
    session.pop('username', None)
    session.pop('password', None)
    flash('logout succesfully')
    return redirect(url_for('login'))
