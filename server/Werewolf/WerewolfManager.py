import random
from Werewolf import Werewolf
from server.controller.roomIO import alert, broadcast

ROOMS = dict()
USERS = dict()


def create_room(people, wolf, villager, cupid, prophet, guard, hunter, witch):

    room_id = random.randint(0, 9999)
    while room_id in ROOMS.keys():
        room_id = random.randint(0, 9999)

    werewolf = Werewolf(room_id,people, wolf, villager, cupid, prophet, guard, hunter, witch)
    ROOMS[room_id] = werewolf

    return room_id


def enter_room(room_id, uid, username):
    if uid in USERS:
        return -2, None

    if room_id not in ROOMS.keys():
        return None, None

    play_id = ROOMS[room_id].add_user(uid)

    if play_id is None:
        return -1, None
    else:
        USERS[uid] = dict()
        USERS[uid]['room_id'] = int(room_id)
        USERS[uid]['play_id'] = int(play_id)
        USERS[uid]['role'] = ROOMS[room_id].get_role(play_id)
        USERS[uid]['username'] = username
        return play_id, ROOMS[room_id].get_role(play_id)


def get_role(room_id, user_id):
    return ROOMS[room_id].get_role(user_id)


def get_userinfo(uid):
    return USERS.get(uid, None)


def game_begin(room_id):

    if ROOMS[room_id].get_usernum() != ROOMS[room_id].get_peoplenum():
        alert('someone doesn\'t enter', room_id, 0)
        return

    broadcast('game start!\n',room_id)

    for i in range((ROOMS[room_id].get_usernum())):
        user = USERS[ROOMS[room_id].get_user(i)]
        broadcast("username: " + user['username'] + " id: " + i, room_id)

    ROOMS[room_id].start()





