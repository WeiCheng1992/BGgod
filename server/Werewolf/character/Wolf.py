from server.werewolf.character import Character
from server.controller.roomIO import notice
import threading


class Wolf(Character):
    def __init__(self):
        super('WOLF_KILL')

    def take_action(self, context, cv, room_id = None, play_id = None):
        if not self.is_alive():
            return None

        notice("Please kill one person discussing with your teammate!",room_id,play_id)

        ans = []

        stage = self.get_stage() + str(play_id)

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

