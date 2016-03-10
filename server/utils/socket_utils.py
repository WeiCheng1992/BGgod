from server import MAX_PEOPLE
from flask_socketio import emit


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


def deadnote(msg, room_id,play_id = None):
    emit('deadnote', {'msg': msg}, room=get_channel(room_id,play_id))