from server.utils.socket_utils import notice


class Character:
    __is_alive = False
    __STAGE = None

    def __init__(self, stage=None):
        self.__is_alive = True
        self.__STAGE = stage

    def dead(self):
        self.__is_alive = False

    def is_alive(self):
        return self.__is_alive

    def dead_action(self, context, cv, room_id=None, play_id=None):
        return []

    def take_action(self, context, cv, room_id=None, play_id=None):
        return []

    def fate_action(self, room_id):
        pass

    def get_stage(self):
        return self.__STAGE

    def vote(self, stage, context, cv, room_id=None, play_id=None):

        notice('Please vote for ' + stage, room_id, play_id)

        ans = None
        stage += ":" + str(play_id)

        cv.acquire()
        while True:
            if stage not in context:
                cv.wait()
            else:
                ans = context[stage][0]
                del context[stage]
                break

        cv.release()

        return ans
