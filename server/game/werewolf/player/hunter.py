from server.utils.socket_utils import notice
from server.game.werewolf.player.character import Character

_STAGE = 'Hunter Round'


class Hunter(Character):
    def __init__(self):
        Character.__init__(self, _STAGE)

    def dead_action(self, context, cv, room_id=None, play_id=None):
        notice('Please choose one person to die (-1 for no one)!', room_id, play_id)

        stage = self.get_stage() + str(play_id)

        ans = []
        cv.acquire()
        while True:
            if stage not in context:
                cv.wait()
            else:
                if context[stage][0] != -1:
                    ans = context[stage][0:1]
                del context[stage]
                break

        cv.release()

        return ans
