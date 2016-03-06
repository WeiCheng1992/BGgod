from server.werewolf.WerewolfManager import  game_begin
from flask import  session, redirect, url_for
from flask_socketio import join_room, emit
from server import socketio
from server.werewolf import WerewolfManager
from server import MAX_PEOPLE
import threading

def get_channel(room_id, user_id = None):
    if user_id is None:
        return room_id * (MAX_PEOPLE + 1)
    else:
        return room_id * (MAX_PEOPLE + 1) + user_id +1


def alert(msg, room_id, play_id = None):
    emit('alert',{'msg': msg}, room=get_channel(room_id,play_id))


def notice(msg, room_id,play_id = None):
    emit('notice', {'msg': msg}, room=get_channel(room_id, play_id))


def broadcast(msg, room_id):
    emit('broadcast', {'msg': msg}, room=get_channel(room_id))


@socketio.on('join_user')
def join_chatroom():
    if 'uid' not in session:
        return redirect(url_for('login'))

    userinfo = WerewolfManager.get_userinfo(session['uid'])
    # big room
    join_room(get_channel(userinfo['room_id'], None))
    # personal room
    join_room(get_channel(userinfo['room_id'], userinfo['play_id']))


@socketio.on('begin')
def begin(room_id):
    t = threading.Thread(target=game_begin, args=(int(room_id), ))
    t.start()


