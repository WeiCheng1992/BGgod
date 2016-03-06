from server.werewolf.character import Character
from server.controller.roomIO import notice
import threading


class Cupid(Character):
    def __init__(self):
        super('SET_COUPLE')

    def take_action(self, context, cv, room_id = None, play_id = None):
        notice("Please choose 2 player to be couples.\n(type 2 numbers splited by space)",room_id, play_id)

        ans = []
        stage = self.get_stage()
        cv.acquire()
        while True:
            if stage not in context:
                cv.wait()
            else:
                if len(context[stage]) < 2:
                    notice('Please choose 2 players', room_id, play_id)
                    cv.wait()
                elif context[stage][0] == context[stage][1]:
                    notice('Please choose 2 different player', room_id, play_id)
                    cv.wait()
                else:
                    ans = context[stage][0:2]
                    del context[stage]
                    break

        notice('You are couple. The other is No. '+ str(ans[1]),room_id,ans[0])
        notice('You are couple. The other is No. '+ str(ans[0]),room_id,ans[1])

        cv.release()

        return ans


