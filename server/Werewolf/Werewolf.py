
from random import shuffle
from server.werewolf.character import Cupid,Guard,Hunter,Prophet,Witch,Wolf,Villager
from server.controller.roomIO import notice
import threading


COPVOTE = 0.5


class Werewolf:
    __list = []
    __cop = 0
    __couple = []
    __userlist = []
    __turn = 0
    __stage = None
    __Day_or_night = None
    __has_cupid = False
    __has_prophet = False
    __has_guard = False
    __has_hunter = False
    __has_witch = False
    __cv = None
    __context = dict()
    __room_id = 0

    def __init__(self,room_id, people, wolf, villager, cupid, prophet, guard, hunter, witch):

        if people != wolf + villager + cupid + prophet + guard + hunter + witch:
            raise Exception('Bad parameter')

        self.__list += [Wolf() for __ in range(wolf)]
        self.__list += [Villager() for __ in range(villager)]
        self.__list += [Cupid() for __ in range(cupid)]
        self.__list += [Prophet() for __ in range(prophet)]
        self.__list += [Guard() for __ in range(guard)]
        self.__list += [Hunter() for __ in range(hunter)]
        self.__list += [Witch() for __ in range(witch)]
        shuffle(self.__list)
        self.__cv = threading.Condition(threading.Lock())
        self.__room_id = room_id

    def get_role(self, index):
        return type(self.__list[index])

    def get_peoplenum(self):
        return len(self.__list)

    def get_usernum(self):
        return len(self.__userlist)

    def add_user(self, uid):
        if len(self.__userlist) >= len(self.__list):
            return None
        else:
            self.__userlist.append(uid)
            return len(self.__userlist) - 1

    def get_user(self,index):
        return self.__userlist[index]

    def set_info(self, info):
        if self.__stage is None:
            return

        info = info.split()
        self.__cv.require()

        if self.__stage not in self.__context:
            self.__context[self.__stage] = []

        self.__context[self.__stage] += info

        self.__cv.notify_all()

        self.__cv.release()

    def start(self):
        self.__turn = 0

        cu = list(filter(lambda x : isinstance(x, Cupid), self.__list))
        if len(cu) == 0:
            return

        else:
            self.__couple = cu[0].take_action(self.__context, self.__cv,self.__room_id, self.__list.indexOf(cu[0]))
            self.__stage = None

    def next_night(self):
        pass
