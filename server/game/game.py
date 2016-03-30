import threading

from flask import copy_current_request_context

from server.utils.socket_utils import alert


class Game:
    """
    _list : a list of game character
    _room_id : an unique int of room
    _cv : a conditional variable
    _context : a buffer map for user to input
    _stage : a string indicating which stage is
    _userlist = a list of user's uid
    """
    _list = []
    _room_id = 0
    _cv = None
    _context = dict()
    _stage = None
    _userlist = []

    def __init__(self, room_id):
        self._cv = threading.Condition(threading.Lock())
        self._room_id = room_id

    def get_role(self, play_id):
        """

        :param play_id: a index in int
        :return: a string of player's role like "wolf"
        """
        return ''

    def get_peoplenum(self):
        """

        :return: the total number of
                 people can play in this room
        """
        return len(self._list)

    def get_usernum(self):
        """

        :return: the number of people who have already enrolled
        """
        return len(self._userlist)

    def add_user(self, uid):
        """

        :param uid: user's uid
        :return: None if this room is full
                 their play_id in this room
        """
        if len(self._userlist) >= len(self._list):
            return None
        else:
            self._userlist.append(uid)
            return len(self._userlist) - 1

    def get_user(self, play_id):
        """

        :param play_id:
        :return: the uid of the player
        """
        return self._userlist[play_id]

    def set_info(self, info, play_id):
        """

        :param info: the player's input string
                     * only the numbers split by space are accepted
        :param play_id:
        :return: None
        """
        if self._stage is None:
            return

        try:
            info = list(map(int, info.split()))
        except ValueError:
            alert("input is invalid!", self._room_id, play_id)
            return

        self._cv.acquire()

        stage = self._stage + ':' + str(play_id)
        if stage not in self._context:
            self._context[stage] = []

        self._context[stage] += info
        self._cv.notify_all()
        self._cv.release()

    def start(self):
        """
        Do Some initialization of the game

        """
        pass

    def next_round(self):
        """

        Turn to the next round
        """
        pass

    def _vote_helper(self, funcs, play_ids, weights, stage=None):
        """
        :param funcs: a list players' vote functions
        :param play_ids: a list of players' id
        :param weights: a list of the voting weight of each player
        :param stage: string. which voting stage
        :return: list of tuple of vote (value, times).
        """
        ans = dict()
        threads = []

        @copy_current_request_context
        def __vote_wrapper(context, cv, func, play_id, result, stage):

            if stage is None:
                result[play_id] = func(context, cv, self._room_id, play_id)[0]
            else:
                result[play_id] = func(stage, context, cv, self._room_id, play_id)

        for i in range(len(funcs)):
            threads.append(
                threading.Thread(target=__vote_wrapper,
                                 args=(self._context, self._cv, funcs[i], play_ids[i], ans, stage)))

            threads[-1].start()

        for thread in threads:
            thread.join()

        votes = []
        for i in range(len(funcs)):
            votes += [ans[play_ids[i]] for _ in range(weights[i])]

        result = dict()

        for vote in votes:
            result[vote] = result.get(vote, 0) + 1

        return sorted(result.items(), key=lambda x: x[1], reverse=True)
