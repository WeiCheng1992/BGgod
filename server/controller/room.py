from flask import render_template, session, request, redirect, url_for, flash

from server import app
from server.game.game_manager import create_room as manager_create, get_userinfo, enter_room as manager_enter


@app.route('/open_room', methods=['GET'])
def open_room():
    if 'uid' not in session:
        return redirect(url_for('login'))

    return render_template('openroom.html')


@app.route('/create_room', methods=['POST', 'GET'])
def create_room():
    if 'uid' not in session:
        return redirect(url_for('login'))

    people = int(request.form.get('people', 0))
    wolf = int(request.form.get('wolf', 0))
    villager = int(request.form.get('villager', 0))

    cupid = 0 if request.form.get('cupid', 0) == 0 else 1
    prophet = 0 if request.form.get('prophet', 0) == 0 else 1
    guard = 0 if request.form.get('guard', 0) == 0 else 1
    hunter = 0 if request.form.get('hunter', 0) == 0 else 1
    witch = 0 if request.form.get('witch', 0) == 0 else 1

    try:
        room_id = manager_create(people, wolf, villager, cupid, prophet, guard, hunter, witch)
    except Exception as e:
        flash(e.message)
        return redirect(url_for('open_room'))
    else:
        return redirect(url_for('enter_room', room_id=room_id))


@app.route('/enter_room', methods=['POST'])
def go_room():
    if len(request.form.get('room_id', '')) > 0:
        return redirect(url_for('enter_room', room_id=request.form.get('room_id', '')))

    flash("invalid room number!")
    return render_template("alreadylogin.html", name=session['username'])


@app.route('/enter_room/<int:room_id>')
def enter_room(room_id):
    if 'uid' not in session:
        return redirect(url_for('login'))

    userinfo = get_userinfo(session['uid'])

    if userinfo is not None:
        flash("your already have a game. Help you to indirect to it")
        return redirect(url_for('room', room_id=userinfo['room_id']))

    play_id, role = manager_enter(int(room_id), session['uid'], session['username'])

    if play_id is None:
        flash("no such room!")
        return redirect(url_for('open_room'))
    elif play_id == -1:
        flash("The room is full of people!")
        return redirect(url_for('open_room'))
    else:
        return redirect(url_for('room', room_id=room_id))


@app.route('/room/<int:room_id>')
def room(room_id):
    if 'uid' not in session:
        return redirect(url_for('login'))

    userinfo = get_userinfo(session['uid'])

    if userinfo is None:
        flash("You are not in the opening game!")
        return redirect(url_for('open_room'))
    else:
        if userinfo['room_id'] != room_id:
            flash("You have another ongoing game!,help you enter it!")
            return redirect(url_for('room', room_id=userinfo['room_id']))
        else:
            return render_template("room.html",
                                   play_id=userinfo['play_id'],
                                   role=userinfo['role'],
                                   room_id=room_id)
