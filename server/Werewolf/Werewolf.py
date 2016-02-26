from enum import Enum
from random import shuffle

Role = Enum('Role', ('WOLF', 'VILLAGER', 'CUPID', 'PROPHET', 'GUARD', 'HUNTER', 'WITCH', 'DEAD'))

COPVOTE = 0.5


class Werewolf:
    __list = []
    __cop = 0
    __couple = []

    def __init__(self, people, wolf, villager, cupid, prophet, guard, hunter, witch):

        if people != wolf + villager + cupid + prophet + guard + hunter + witch:
            raise Exception('Bad parameter')

        self.__list += [Role.WOLF for __ in range(wolf)]
        self.__list += [Role.VILLAGER for __ in range(villager)]
        self.__list += [Role.CUPID for __ in range(cupid)]
        self.__list += [Role.PROPHET for __ in range(prophet)]
        self.__list += [Role.GUARD for __ in range(guard)]
        self.__list += [Role.HUNTER for __ in range(hunter)]
        self.__list += [Role.WITCH for __ in range(witch)]

        shuffle(self.__list)

    def get_role(self, index):
        return self.__list[index]

    def set_couple(self, couple):
        self.__couple = couple

    def __vote(self, votes):
        l = [(id, vote) for id, vote in votes.items()]

        l.sort(key = lambda x : x[1])

        if len(l) == 1:
            return l[0][0]

        if l[0][1] == l[1][1]:
            return -1

        return l[0][0]

    def vote_cop(self, votes):
        assert len(votes) == len(self.__list)

        d = dict()

        for vote in votes:
            d[vote] = d.get(vote, 0) + 1

        __cop = self.__vote(d)

        return __cop

    def set_cop(self, index):
        self.__cop = index

    def vote_dead(self, votes):
        len(filter(lambda x : x != Role.DEAD, self.__list)) == len(votes)
        d = dict()

        for vote in votes:
            if vote != -1:
                d[vote] = d.get(vote, 0) + 1

        d[votes[self.__cop]] = d.get(votes[self.__cop], 0) + COPVOTE

        return self.__vote(d)

    def set_dead(self, index):
        self.__list[index] = Role.DEAD

    def get_people(self):
        return len(self.__list)



