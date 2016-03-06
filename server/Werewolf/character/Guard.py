from server.werewolf.character import Character
from server.controller.roomIO import notice
import threading


class Wolf(Character):
    def __init__(self):
        super('Guard Round')
        self.__guard = None

    def take_action(self, context, cv, room_id = None, play_id = None):
        notice("Please choose the person you want to guard!",room_id,play_id)

        stage = self.get_stage() + str(play_id)

        cv.acquire()
        while True:
            if stage not in context:
                cv.wait()
            else:
                if self.__guard == context[stage][0]:
                    notice("You can't guard one person in consecutive 2 rounds",room_id,play_id)
                    del context[stage]
                    cv.wait()
                else:
                    self.__guard = context[stage][0]
                    del context[stage]
                break

        cv.release()

        return [self.__guard]

    def get_guardee(self):
        return self.__guard

