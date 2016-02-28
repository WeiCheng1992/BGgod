import random
from Werewolf import Werewolf

ROOMS = dict()
USERS = dict()
MAX_PEOPLE = 15


def get_channel(room_id, user_id):
    if user_id is None:
        return room_id * (MAX_PEOPLE + 1)
    else:
        return room_id * (MAX_PEOPLE + 1) + user_id +1


def create_room(people, wolf, villager, cupid, prophet, guard, hunter, witch):
    werewolf = Werewolf(people, wolf, villager, cupid, prophet, guard, hunter, witch)

    num = random.randint(0, 9999)
    while num in ROOMS.keys():
        num = random.randint(0, 9999)

    ROOMS[num] = werewolf

    return num


def enter_room(room_id, uid):
    if uid in USERS:
        return -2, None

    if room_id not in ROOMS.keys():
        return None, None

    play_id = ROOMS[room_id].add_user(uid)

    if play_id is None:
        return -1, None
    else:
        USERS[uid] = dict()
        USERS[uid]['room_id'] = room_id
        USERS[uid]['play_id'] = play_id
        USERS[uid]['role'] = ROOMS[room_id].get_role(play_id)
        return play_id, ROOMS[room_id].get_role(play_id)


def get_role(room_id, user_id):
    return ROOMS[room_id].get_role(user_id)


def get_userinfo(uid):
    return USERS.get(uid, None)