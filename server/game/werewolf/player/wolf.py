from server.utils.socket_utils import notice
from server.game.werewolf.player.character import Character

_STAGE = 'WOLF_KILL'


class Wolf(Character):
    def __init__(self):
        Character.__init__(self, _STAGE)

    def take_action(self, context, cv, room_id=None, play_id=None):

        notice('Please kill one person discussing with your teammate!(-1 for don\'t kill anyone)', room_id, play_id)

        ans = []

        stage = self.get_stage() + ":" + str(play_id)

        cv.acquire()
        while True:
            if stage not in context:
                cv.wait()
            else:
                ans = context[stage][0:1]
                del context[stage]
                break

        cv.release()

        return ans
