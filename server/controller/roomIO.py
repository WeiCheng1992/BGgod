import threading

from flask import session, redirect, url_for
from flask_socketio import join_room, leave_room
from flask import copy_current_request_context

from server import socketio
from server.game.werewolf.werewolf_manager import game_begin, start_night, start_day
from server.game.werewolf.werewolf_manager import get_userinfo, set_info
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
def leave_chatroom():
    if 'uid' not in session:
        return redirect(url_for('login'))

    userinfo = get_userinfo(session['uid'])
    # big room
    leave_room(get_channel(userinfo['room_id'], None))
    # personal room
    leave_room(get_channel(userinfo['room_id'], userinfo['play_id']))


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


@socketio.on('night')
def night(room_id):

    @copy_current_request_context
    def night_wrapper(room_id):
        start_night(room_id)

    t = threading.Thread(target=night_wrapper, args=(int(room_id), ))
    t.start()


@socketio.on('day')
def day(room_id):

    @copy_current_request_context
    def day_wrapper(room_id):
        start_day(room_id)

    t = threading.Thread(target=day_wrapper, args=(int(room_id), ))
    t.start()
