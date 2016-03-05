
from flask import render_template, session, request ,redirect , url_for ,flash
from server import app
from server.Werewolf.GameOrdinator import USERS
from server.model import SqliteDB


@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
@app.route('/login', methods = ['GET'])
def login():
    if 'uid' in session :
        if session['uid'] in USERS:
            return redirect(url_for("room", room_id = USERS[session['uid']]['room_id']))
        else:
            return render_template("loginalready.html",name = session['username'])
    else:
        return render_template("login.html")


@app.route('/signon', methods = ['POST'])
def signon():
    user = SqliteDB.get_user(request.form.get("username",""), request.form.get("password",""))

    if user is None:
        flash('username or password is wrong!')
    else:
        session['uid'] = user.get_uid()
        session['username'] = user.get_username()
        session['password'] = user.get_password()

    return redirect(url_for('login'))


@app.route('/signup', methods = ['GET'])
def register():
    return render_template("register.html")


@app.route('/signup', methods = ['POST'])
def signup():
    if len(request.form.get("username","")) < 3:
        flash("username cannot shorter than 3!")
        return redirect(url_for("signup"))

    if len(request.form.get("password","")) < 3:
        flash("password cannot shorter than 3!")
        return redirect(url_for("signup"))

    if request.form.get("password","") != request.form.get("again",""):
        flash("passwords are different!")
        return redirect(url_for("signup"))

    user = SqliteDB.add_user(request.form['username'], request.form['password'])
    if user is None:
        flash('something is wrong!')
        return redirect(url_for("signup"))
    else:
        session['uid'] = user.get_uid()
        session['username'] = user.get_username()
        session['password'] = user.get_password()

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if 'uid' in session:
        session.pop("uid")
    if 'password' in session:
        session.pop("password")
    flash('logout successfully')
    return redirect(url_for('login'))

