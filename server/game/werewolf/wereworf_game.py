import threading
from random import shuffle

from server.game.werewolf.player.cupid import Cupid
from server.game.werewolf.player.guard import Guard
from server.game.werewolf.player.hunter import Hunter
from server.game.werewolf.player.prophet import Prophet
from server.game.werewolf.player.villager import Villager
from server.game.werewolf.player.witch import Witch
from server.game.werewolf.player.wolf import Wolf
from server.utils.socket_utils import notice, deadnote
from server.game.game import Game


class Werewolf(Game):
    """
    __cop : the play_id of cop
    __couple : the play_ids of couple
    """
    __cop = None
    __couple = None
    __turn = 0
    __is_day = None

    def __init__(self, room_id, people, wolf, villager, cupid, prophet, guard, hunter, witch):

        if people != wolf + villager + cupid + prophet + guard + hunter + witch:
            raise Exception('Bad parameter!\n')

        self._list += [Wolf() for _ in range(wolf)]
        self._list += [Villager() for _ in range(villager)]
        self._list += [Cupid() for _ in range(cupid)]
        self._list += [Prophet() for _ in range(prophet)]
        self._list += [Guard() for _ in range(guard)]
        self._list += [Hunter() for _ in range(hunter)]
        self._list += [Witch() for _ in range(witch)]
        shuffle(self._list)
        Game.__init__(self, room_id)

    def get_role(self, play_id):
        return str(self._list[play_id].__class__).split('.')[-1]

    def start(self):
        self.__turn = 0
        self.__is_day = True

        cupid = self.__get_characters(Cupid)
        if len(cupid) == 0:
            return

        else:
            self._stage = cupid[0][0].get_stage()
            self.__couple = list(
                map(int, cupid[0][0].take_action(self._context, self._cv, self._room_id, cupid[0][1])))
            self._stage = None

    def next_round(self):
        if self.__is_day:
            self.__is_day = False
            return self.next_night()
        else:
            self.__turn += 1
            self.__is_day = True
            return self.next_day()

    def __get_characters(self, role):
        """
        :param role: type of characters EG: Prophet
        :return: the list of tuple (character, play_id)
        """
        ans = []
        for i in range(len(self._list)):
            if isinstance(self._list[i], role):
                ans.append((self._list[i], i))

        return ans

    def __handle_dead(self, deads):
        deads = list(map(int, deads))

        for dead in deads:
            if self.__couple is not None and dead in self.__couple:
                deads += self.__couple
                self.__couple = None

        deads = list(set(deads))

        for dead in deads:
            deadnote(dead, self._room_id, dead)
            self._list[dead].dead()

        iswin, win = self.__is_win()
        if iswin:
            notice('Game ends. ' + str(win) + ' win!', self._room_id)
            return True

        n = []
        for dead in deads:
            if isinstance(self._list[dead], Hunter):
                self._stage = self._list[dead].get_stage()
                n += self._list[dead].dead_action(self._context, self._cv, self._room_id, dead)

        if len(n) == 1:
            if self.__couple is not None and n[0] in self.__couple:
                if n[0] == self.__couple[0]:
                    n += self.__couple[1]
                else:
                    n += self.__couple[0]
            self.__couple = None

        for dead in n:
            deadnote(dead, self._room_id, dead)
            self._list[dead].dead()

        deads += n

        iswin, win = self.__is_win()
        if iswin:
            notice('Game ends. ' + str(win) + ' win!', self._room_id)
            return True

        else:
            if self.__cop in deads:
                notice('cop dead. Must set a new cop', self._room_id)
                self._stage = 'setting cop'
                self.__cop = self._list[self.__cop].vote(self._stage, self._context, self._cv, self._room_id,
                                                         self.__cop)
                notice('new cop is No.' + str(self.__cop), self._room_id)

        return False

    def __is_win(self):
        """
        :return: a tuple (iswin,winlist)
             iswin : boolean
                    False for game not end
                    True for game end
             winlist : list of winning players
                    None when iswin is False
        """
        ans = []
        for i in range(len(self._list)):
            if self._list[i].is_alive():
                ans.append(i)

        # good man win
        if len(filter(lambda x: x.is_alive(), list(map(lambda x: x[0], self.__get_characters(Wolf))))) == 0:
            return True, ans

        # couple win
        if len(ans) == 2 and self.__couple is not None:
            if ans[0] * ans[1] == self.__couple[0] * self.__couple[1] and sum(ans) == sum(self.__couple):
                return True, ans

        # not win
        for alive in filter(lambda x: x.is_alive(), self._list):
            if not isinstance(alive, Wolf):
                return False, None

        # wolf win
        return True, ans

    def __vote(self, funcs, play_ids, weights, isone, stage=None):
        """
        :param funcs: a list players' vote functions
        :param play_ids: a list of players' id
        :param weights: a list of the voting weight of each player
        :param isone: boolean whether all the people need to have same vote
        :param stage: string. which voting stage
        :return: list of targeting people. empty list for vote failure.
        """

        tmp = self._vote_helper(funcs, play_ids, weights,stage)

        if isone and len(tmp) != 1:
            return []

        ans = [tmp[0][0]]

        for i in range(len(tmp) - 1):
            if tmp[i][1] == tmp[i + 1][1]:
                ans.append(int(tmp[i + 1][0]))
            else:
                break

        return ans

    def next_night(self):

        # wolf killing
        wolves = self.__get_characters(Wolf)
        self._stage = wolves[0][0].get_stage()
        play_ids = []
        selfs = []
        dead = None

        for wolf in wolves:
            if wolf[0].is_alive():
                play_ids.append(wolf[1])
                selfs.append(wolf[0])

        deads = self.__vote([x.take_action for x in selfs],
                            play_ids,
                            [1 for _ in range(len(selfs))],
                            True)

        if len(deads) == 0 or deads[0] == -1:
            for wolf in wolves:
                if wolf[0].is_alive():
                    notice('No one dead tonight', self._room_id, wolf[1])
        else:
            dead = deads[0]

        # guard round
        guard = self.__get_characters(Guard)
        if len(guard) == 1:
            if guard[0][0].is_alive():
                self._stage = guard[0][0].get_stage()
                guard[0][0].take_action(self._context, self._cv, self._room_id, guard[0][1])
            else:
                guard[0][0].fate_action(self._room_id)

        # prophet round
        prophet = self.__get_characters(Prophet)
        if len(prophet) == 1:
            if prophet[0][0].is_alive():
                self._stage = prophet[0][0].get_stage()
                ans = prophet[0][0].take_action(self._context, self._cv, self._room_id, prophet[0][1])
                if ans is not None:
                    if isinstance(self._list[ans[0]], Wolf):
                        notice('He is a bad man!', self._room_id, prophet[0][1])
                    else:
                        notice('He is a good man!', self._room_id, prophet[0][1])
            else:
                prophet[0][0].fate_action(self._room_id)

        # witch round
        witch = self.__get_characters(Witch)
        if len(witch) == 1:
            if witch[0][0].is_alive():
                self._stage = witch[0][0].get_stage()
                self._context['to be dead'] = dead
                ans = witch[0][0].take_action(self._context, self._cv, self._room_id, witch[0][1])
            else:
                witch[0][0].fate_action(self._room_id)
                ans = [0, -1]
        else:
            ans = [0, -1]

        #  final calculate
        g = guard[0][0].get_guardee() if len(guard) == 1 else -1

        self._context.clear()

        if (dead is None or g == dead or ans[0] == 1) and ans[1] == -1:
            notice("No one die tonight!", self._room_id)
            return False
        elif g == dead or ans[0] == 1:
            return self.__handle_dead([ans[1]])
        elif ans[1] != -1:
            return self.__handle_dead([dead, ans[1]])
        else:
            return self.__handle_dead([dead])

    def next_day(self):

        # vote for cop
        if self.__turn == 1:
            self._stage = 'cop'
            play_ids = []
            selfs = []
            for i in range(len(self._list)):
                if self._list[i].is_alive():
                    play_ids.append(i)
                    selfs.append(self._list[i])

            while True:

                ans = self.__vote([x.vote for x in selfs],
                                  play_ids,
                                  [1 for _ in range(len(selfs))],
                                  False,
                                  self._stage
                                  )

                if len(ans) != 1:
                    for play_id in play_ids:
                        notice('Tie for' + str(ans) + ' . Please revote', self._room_id, play_id)
                else:
                    self.__cop = ans[0]

                    for play_id in play_ids:
                        notice('Cop is No.' + str(self.__cop), self._room_id, play_id)
                    break

        self._stage = 'dead'
        play_ids = []
        selfs = []
        weights = []
        for i in range(len(self._list)):
            if self._list[i].is_alive():
                play_ids.append(i)
                selfs.append(self._list[i])
                if i == self.__cop:
                    weights.append(3)
                else:
                    weights.append(2)

        while True:
            ans = self.__vote([x.vote for x in selfs],
                              play_ids,
                              weights,
                              False,
                              self._stage
                              )

            if len(ans) != 1:
                for play_id in play_ids:
                    notice('Tie for' + str(ans) + ' . Please revote', self._room_id, play_id)
            else:
                return self.__handle_dead(ans)

        return False
