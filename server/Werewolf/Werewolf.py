
from random import shuffle
from server.werewolf.character import Cupid,Guard,Hunter,Prophet,Witch,Wolf,Villager
from server.controller.roomIO import notice,deadnote
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

    def __get_characters(self, role):
        ans = []
        for i in range(len(self.__list)):
            if isinstance(self.__list[i], role):
                ans.append((self.__list[i], i))

        return ans

    def __handle_dead(self,deads):
        for dead in deads:
            if dead in self.__couple:
                deads += self.couple

        deads = list(set(deads))

        for dead in deads:
            deadnote(str(dead), self.__room_id, dead)

        n = []
        for dead in deads:
            if isinstance(self.__list[dead],Hunter):
                self.__stage = self.__list[dead].get_stage()
                n += self.__list[dead].dead_action(self.__context,self.__cv,self.__room_id,dead)

        if len(n) == 1:
            if n[0] in self.__couple:
                if n[0] == self.__couple[0]:
                    n += self.__couple[1]
                else:
                    n += self.__couple[0]

        for dead in n:
            deadnote(str(dead), self.__room_id, dead)

        deads += n
        for dead in deads:
            self.__list[dead].dead()

    def start(self):
        self.__turn = 0

        cupid = self.__get_characters(Cupid)
        if len(cupid) == 0:
            return

        else:
            self.__stage = cupid[0][0].get_stage()
            self.__couple = cupid[0][0].take_action(self.__context, self.__cv, self.__room_id, cupid[0][1])
            self.__stage = None

    def next_night(self):

        # wolf killing
        wolves = self.__get_characters(Wolf)
        ans = []
        self.__stage = wolves[0][0].get_stage()
        while True:
            for wolf in wolves:
                if wolf[0].is_alive():
                    ans.append(wolf[0].take_action(self.__context, self.__cv, self.__room_id, wolf[1]))

            if len(set(ans)) != 1:
                for wolf in wolves:
                    if wolf[0].is_alive():
                        notice("please kill One person!",self.__room_id, wolf[1])
            else:
                ans = list(set(ans))
                break

        dead = ans[0]

        # guard round
        guard = self.__get_characters(Guard)
        if len(guard) == 1:
            self.__stage = guard[0][0].get_stage()
            guard[0][0].take_action(self.__context, self.__cv,self.__room_id,guard[0][1])

        # prophet round
        prophet = self.__get_characters(Prophet)
        if len(prophet) == 1:
            self.__stage = prophet[0][0].get_stage()
            ans = prophet[0][0].take_action(self.__context, self.__cv,self.__room_id,prophet[0][1])
            if ans is not None:
                if isinstance(self.__list[ans[0]], Wolf):
                    notice("He is a bad man!", self.__room_id, prophet[0][1])
                else:
                    notice("He is a good man!", self.__room_id, prophet[0][1])

        # witch round
        witch = self.__get_characters(Witch)
        if len(witch) == 1:
            self.__stage = witch[0][0].get_stage()
            self.__context['to be dead'] = dead
            ans = witch[0][0].take_action(self.__context,self.__cv,self.__room_id,witch[0][1])

        #final calculate
        if (guard[0][0].get_guardee() == dead or ans[0] == 1) and ans[1] == -1:
            pass
        elif guard[0][0].get_guardee() == dead or ans[0] == 1 :
            self.__handle_dead([ans[1]])
        elif ans[1] != -1:
            self.__handle_dead([dead, ans[1]])
        else:
            self.__handle_dead([dead])

        self.__context.clear()


