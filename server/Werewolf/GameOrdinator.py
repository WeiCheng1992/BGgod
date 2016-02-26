import random
from Werewolf import Werewolf

ROOMS = dict()
SIO = dict()
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


def enter_room(room_id,name):
    if room_id not in ROOMS.keys():
        return None, None
    elif ROOMS[room_id].get_people() <= SIO.get(room_id, 0):
        return -1, None
    else:
        #print ROOMS[room_id].get_people() , SIO.get(room_id, 0)
        ID = SIO.get(room_id, 0)
        SIO[room_id] = SIO.get(room_id, 0) + 1

        return ID, ROOMS[room_id].get_role(ID)