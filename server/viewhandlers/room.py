from flask import render_template, session, request ,redirect , url_for ,flash
from server import app
from server import socketio
from server.Werewolf import GameOrdinator
from server.Werewolf.GameOrdinator import get_channel ,ROOMS
from flask_socketio import join_room, leave_room , send,emit

@app.route('/OpenRoom', methods = ['GET'])
def open_room():
    return render_template('OpenRoom.html')


@app.route('/createroom', methods = ['POST', 'GET'])
def create_room():
    people = int(request.form.get('people', 0))
    wolf = int(request.form.get('wolf', 0))
    villager = int(request.form.get('villager', 0))

    cupid = 0 if request.form.get('cupid', 0) == 0 else 1
    prophet = 0 if request.form.get('prophet', 0) == 0 else 1
    guard = 0 if request.form.get('guard', 0) == 0 else 1
    hunter = 0 if request.form.get('hunter', 0) == 0 else 1
    witch = 0 if request.form.get('witch', 0) == 0 else 1

    room_num = GameOrdinator.create_room(people, wolf, villager, cupid, prophet, guard, hunter, witch)

    return redirect("/room/" + str(room_num))


@app.route('/room/<room_id>')
def room(room_id):
    if 'user_id' not in session and ('room_id' not in session or session['room_id'] != room_id):
        ID, role = GameOrdinator.enter_room(int(room_id),session['username'])
    else:
        ID = session['user_id']
        role = ROOMS[session['room_id']].get_role(ID)

    if ID is None :
        return "no such room"
    elif ID == -1 :
        return "Room is full of people"
    else :
        session['room_id'] = int(room_id)
        session['user_id'] = int(ID)
        return render_template("room.html",
                               ID = ID,
                               role = role,
                               room_id = room_id)


@socketio.on('join_user')
def enter_room():
    # big room
    join_room(get_channel(session['room_id'], None))
    # personal room
    join_room(get_channel(session['room_id'], session['user_id']))
    send("hello all", room=get_channel(session['room_id'], None))
    send("hello you", room=get_channel(session['room_id'], session['user_id']))


