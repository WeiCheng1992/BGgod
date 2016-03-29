from server import MAX_PEOPLE
from flask_socketio import emit


def get_channel(room_id, user_id=None):
    if user_id is None:
        return int(room_id) * (MAX_PEOPLE + 1)
    else:
        return int(room_id) * (MAX_PEOPLE + 1) + int(user_id) + 1


def alert(msg, room_id, play_id=None):
    emit('alert', {'msg': msg}, room=get_channel(room_id, play_id))


def notice(msg, room_id, play_id=None):
    emit('notice', {'msg': msg}, room=get_channel(room_id, play_id))


def deadnote(id, room_id, play_id=None):
    emit('deadnote', {'id': id}, room=get_channel(room_id, play_id))


def end(room_id):
    emit('end', room=get_channel(room_id))
