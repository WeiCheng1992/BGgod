
from flask import render_template, session, request
from server import app


@app.route('/login', methods = ['GET'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return session['username']
    else :
        if 'username' in session:
            return "hello " + session['username']
        else:
            return render_template("login.html")