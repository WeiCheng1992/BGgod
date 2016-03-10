import random

from server.utils.socket_utils import alert, broadcast
from server.game.werewolf.wereworf_game import Werewolf

_ROOMS = dict()
_USERS = dict()


def create_room(people, wolf, villager, cupid, prophet, guard, hunter, witch):

    global _ROOMS, _USERS

    room_id = random.randint(0, 9999)
    while room_id in _ROOMS.keys():
        room_id = random.randint(0, 9999)

    werewolf = Werewolf(room_id, people, wolf, villager, cupid, prophet, guard, hunter, witch)
    _ROOMS[room_id] = werewolf

    return room_id


def enter_room(room_id, uid, username):

    global _ROOMS, _USERS

    if uid in _USERS:
        return -2, None

    if room_id not in _ROOMS.keys():
        return None, None

    play_id = _ROOMS[room_id].add_user(uid)

    if play_id is None:
        return -1, None
    else:
        _USERS[uid] = dict()
        _USERS[uid]['room_id'] = int(room_id)
        _USERS[uid]['play_id'] = int(play_id)
        _USERS[uid]['role'] = _ROOMS[room_id].get_role(play_id)
        _USERS[uid]['username'] = username
        return play_id, _ROOMS[room_id].get_role(play_id)


def get_role(room_id, user_id):

    global _ROOMS

    return _ROOMS[room_id].get_role(user_id)


def get_userinfo(uid):

    global _USERS

    return _USERS.get(uid, None)


def game_begin(room_id):

    global _ROOMS, _USERS

    if _ROOMS[room_id].get_usernum() != _ROOMS[room_id].get_peoplenum():
        alert('someone doesn\'t enter', room_id, 0)
        return

    broadcast('game start!\n', room_id)

    for i in range((_ROOMS[room_id].get_usernum())):
        user = _USERS[_ROOMS[room_id].get_user(i)]
        broadcast("username: " + user['username'] + " id: " + str(i), room_id)

    _ROOMS[room_id].start()


def start_night(room_id):

    global _ROOMS

    _ROOMS[room_id].night()