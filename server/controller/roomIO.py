import threading

from flask import copy_current_request_context
from flask import session, redirect, url_for
from flask_socketio import join_room, leave_room

from server import socketio
from server.game.game_manager import game_begin, next_round
from server.game.game_manager import get_userinfo, set_info
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


@socketio.on('leave_user')
def leave_chatroom(room_id, player_id):

    # big room
    leave_room(get_channel(room_id, None))
    # personal room
    leave_room(get_channel(room_id, player_id))


@socketio.on('msg')
def receive(msg):
    set_info(msg['room_id'], msg['play_id'], msg['msg'])


@socketio.on('begin')
def begin(room_id):

    @copy_current_request_context
    def begin_wrapper(room_id):
        game_begin(room_id)

    t = threading.Thread(target=begin_wrapper, args=(int(room_id),))
    t.start()


@socketio.on('next')
def night(room_id):

    @copy_current_request_context
    def next_wrapper(room_id):
        next_round(room_id)

    t = threading.Thread(target=next_wrapper, args=(int(room_id), ))
    t.start()

