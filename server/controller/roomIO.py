import threading

from flask import session, redirect, url_for
from flask_socketio import join_room

from server import socketio
from server.game.werewolf.werewolf_manager import game_begin, start_night
from server.game.werewolf.werewolf_manager import get_userinfo
from server.utils.socket_utils import get_channel


@socketio.on('join_user')
def join_chatroom():
    if 'uid' not in session:
        return redirect(url_for('login'))

    userinfo = get_userinfo(session['uid'])
    # big room
    join_room(get_channel(userinfo['room_id'], None))
    # personal room
    join_room(get_channel(userinfo['room_id'], userinfo['play_id']))


@socketio.on('begin')
def begin(room_id):
    t = threading.Thread(target=game_begin, args=(int(room_id), ))
    t.start()


@socketio.on('night')
def night(room_id):
    t = threading.Thread(target=start_night, args=(int(room_id), ))
    t.start()
