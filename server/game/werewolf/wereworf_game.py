import threading
from random import shuffle

from flask import copy_current_request_context

from server.utils.socket_utils import notice, broadcast, deadnote
from server.game.werewolf.player.cupid import Cupid
from server.game.werewolf.player.guard import Guard
from server.game.werewolf.player.hunter import Hunter
from server.game.werewolf.player.prophet import Prophet
from server.game.werewolf.player.villager import Villager
from server.game.werewolf.player.witch import Witch
from server.game.werewolf.player.wolf import Wolf


class Werewolf:
    __list = []
    __cop = None
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

    def __init__(self, room_id, people, wolf, villager, cupid, prophet, guard, hunter, witch):

        if people != wolf + villager + cupid + prophet + guard + hunter + witch:
            raise Exception('Bad parameter')

        self.__list += [Wolf() for _ in range(wolf)]
        self.__list += [Villager() for _ in range(villager)]
        self.__list += [Cupid() for _ in range(cupid)]
        self.__list += [Prophet() for _ in range(prophet)]
        self.__list += [Guard() for _ in range(guard)]
        self.__list += [Hunter() for _ in range(hunter)]
        self.__list += [Witch() for _ in range(witch)]
        shuffle(self.__list)
        self.__cv = threading.Condition(threading.Lock())
        self.__room_id = room_id

    def get_role(self, index):
        return str(self.__list[index].__class__).split('.')[-1]

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

    def get_user(self, index):
        return self.__userlist[index]

    def set_info(self, info, play_id):
        if self.__stage is None:
            return

        info = info.split()
        self.__cv.require()

        if self.__stage not in self.__context:
            self.__context[self.__stage + str(play_id)] = []

        self.__context[self.__stage + str(play_id)] += info

        self.__cv.notify_all()

        self.__cv.release()

    def __get_characters(self, role):
        ans = []
        for i in range(len(self.__list)):
            if isinstance(self.__list[i], role):
                ans.append((self.__list[i], i))

        return ans

    def __handle_dead(self, deads):
        for dead in deads:
            if self.__couple is not None and dead in self.__couple:
                deads += self.__couple
                self.__couple = None

        deads = list(set(deads))

        for dead in deads:
            deadnote(str(dead), self.__room_id, dead)

        n = []
        for dead in deads:
            if isinstance(self.__list[dead], Hunter):
                self.__stage = self.__list[dead].get_stage()
                n += self.__list[dead].dead_action(self.__context, self.__cv, self.__room_id, dead)

        if len(n) == 1:
            if self.__couple is not None and n[0] in self.__couple:
                if n[0] == self.__couple[0]:
                    n += self.__couple[1]
                else:
                    n += self.__couple[0]
            self.__couple = None

        for dead in n:
            deadnote(str(dead), self.__room_id, dead)

        deads += n
        for dead in deads:
            notice('No.' + str(dead) + ' dead.', self.__room_id)
            self.__list[dead].dead()

        win = self.__is_win()
        if win is None:
            broadcast('Game ends. ' + str(win) + ' win!', self.__room_id)
        else:
            if self.__cop in deads:
                broadcast('cop dead. Must set a new cop', self.__room_id)
                self.__stage = 'setting cop'
                self.__cop = self.__list[self.__cop].vote(self.__stage, self.__context, self.__cv, self.__room_id,
                                                          self.__cop)
                broadcast('new cop is No.' + str(self.__cop), self.__room_id)

    def __is_win(self):
        ans = []
        for i in range(len(self.__list)):
            if self.__list[i].is_alive():
                ans.append(i)

        if len(self.__get_characters(Wolf)) == 0:
            return ans

        if len(ans) == 2 and self.__couple is not None:
            if ans[0] * ans[1] == self.__couple[0] * self.__couple[1] and sum(ans) == sum(self.__couple):
                return ans

        for alive in filter(lambda x: x.is_alive(), self.__list):
            if not isinstance(alive, Wolf):
                return None

        return ans

    def __vote_helper(self, funcs, selfs, play_ids, weights, isone, stage=None):
        ans = dict()
        threads = []

        @copy_current_request_context
        def __vote_wrapper(self, func, sself, play_id, ans, stage=None):

            if stage is None:
                ans[play_id] = func(sself, self.__context, self.__cv, self.__room_id, play_id)[0]
            else:
                ans[play_id] = func(sself, stage, self.__context, self.__cv, self.__room_id, play_id)

        for i in range(len(funcs)):
            threads.append(
                threading.Thread(target=self.__vote_wrapper, args=(self, funcs[i], selfs[i], play_ids[i], ans, stage)))

            threads[-1].start()

        for thread in threads:
            thread.join()

        if isone and len(set(ans.values())) != 1:
            return None

        votes = []
        for i in range(len(funcs)):
            votes += [ans[play_ids[i]] for _ in range(weights[i])]

        result = dict()

        for vote in votes:
            result[vote] = result.get(vote, 0) + 1

        if len(result) == 1:
            return result.keys()[0]

        tmp = sorted(result.items(), key=lambda x: x[1])

        ans = [tmp[0][0]]
        for i in range(len(tmp) - 1):
            if tmp[i][1] == tmp[i + 1][1]:
                ans.append(tmp[i + 1][1])
            else:
                break

        return ans

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
        dead = None
        ans = []
        self.__stage = wolves[0][0].get_stage()
        play_ids = []
        selfs = []

        for wolf in wolves:
            if wolf[0].is_alive():
                play_ids.append(wolf[1])
                selfs.append(wolf[0])

        while True:
            dead = self.__vote_helper([x.take_action for x in selfs],
                                      selfs,
                                      play_ids,
                                      [1 for _ in len(selfs)],
                                      True)

            if dead is None:
                for wolf in wolves:
                    if wolf[0].is_alive():
                        notice('please kill One person!', self.__room_id, wolf[1])
            else:
                break

        # guard round
        guard = self.__get_characters(Guard)
        if len(guard) == 1:
            self.__stage = guard[0][0].get_stage()
            guard[0][0].take_action(self.__context, self.__cv, self.__room_id, guard[0][1])

        # prophet round
        prophet = self.__get_characters(Prophet)
        if len(prophet) == 1:
            self.__stage = prophet[0][0].get_stage()
            ans = prophet[0][0].take_action(self.__context, self.__cv, self.__room_id, prophet[0][1])
            if ans is not None:
                if isinstance(self.__list[ans[0]], Wolf):
                    notice('He is a bad man!', self.__room_id, prophet[0][1])
                else:
                    notice('He is a good man!', self.__room_id, prophet[0][1])

        # witch round
        witch = self.__get_characters(Witch)
        if len(witch) == 1:
            self.__stage = witch[0][0].get_stage()
            self.__context['to be dead'] = dead
            ans = witch[0][0].take_action(self.__context, self.__cv, self.__room_id, witch[0][1])

        # final calculate
        if (guard[0][0].get_guardee() == dead or ans[0] == 1) and ans[1] == -1:
            pass
        elif guard[0][0].get_guardee() == dead or ans[0] == 1:
            self.__handle_dead([ans[1]])
        elif ans[1] != -1:
            self.__handle_dead([dead, ans[1]])
        else:
            self.__handle_dead([dead])

        self.__context.clear()

    def next_day(self):

        # vote for cop
        if self.__turn == 1:
            self.__stage = 'cop'
            play_ids = []
            selfs = []
            for i in range(len(self.__list)):
                if self.__list[i].is_alive():
                    play_ids.append(i)
                    selfs.append(self.__list[i])

                    while True:

                        ans = self.__vote_helper([x.vote for x in selfs],
                                                 selfs,
                                                 play_ids,
                                                 [1 for _ in range(len(selfs))],
                                                 False,
                                                 self.__stage
                                                 )

                        if len(ans) != 1:
                            for play_id in play_ids:
                                notice('Tie for' + str(ans) + ' . Please revote', self.__room_id, play_id)
                        else:
                            self.__cop = ans[0]

                            for play_id in play_ids:
                                notice('Cop is No.' + str(self.__cop), self.__room_id, play_id)
                            break

        self.__stage = 'dead'
        play_ids = []
        selfs = []
        weights = []
        for i in range(len(self.__list)):
            if self.__list[i].is_alive():
                play_ids.append(i)
                selfs.append(self.__list[i])
                if i == self.__cop:
                    weights.append(3)
                else:
                    weights.append(2)

        while True:
            ans = self.__vote_helper([x.vote for x in selfs],
                                     selfs,
                                     play_ids,
                                     weights,
                                     False,
                                     self.__stage
                                     )

            if len(ans) != 1:
                for play_id in play_ids:
                    notice('Tie for' + str(ans) + ' . Please revote', self.__room_id, play_id)
            else:
                self.__handle_dead(ans)
                break
