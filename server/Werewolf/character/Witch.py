from server.werewolf.character import Character
from server.controller.roomIO import notice
import threading


class Witch(Character):
    def __init__(self):
        super('Witch Round')
        self.__antidote = True
        self.__poison = True

    def take_action(self, context, cv, room_id = None, play_id = None):

        if not self.is_alive():
            return None

        ans = []
        dead = context['to be dead']

        notice("No. " + str(dead) + " dead tonight.",room_id,play_id)
        stage = self.get_stage() + str(play_id)

        cv.acquire()
        del context['to be dead']
        if self.__antidote:
            notice("Do you want save his life(0 for no,1 for yes)",room_id,play_id)
            while True:
                if stage not in context:
                    cv.wait()
                else:
                    if context[stage][0] == 1:
                        self.__antidote = False
                        ans.append[1]
                        del context[stage]
                        break
                    elif context[stage][0] == 0:
                        ans.append(0)
                        del context[stage]
                        break
                    else:
                        notice('(0 for no,1 for yes)' , room_id, play_id)
                        del context[stage]

        if self.__poison:
            notice("You have a poison,Do you want to kill someone? ( -1 for nobody)")
            while True:
                if stage not in context:
                    cv.wait()
                else:
                    if context[stage][0] == -1:
                        ans.append[-1]
                        del context[stage]
                        break
                    else:
                        ans.append(context[stage][0])
                        self.__poison = False
                        del context[stage]
                        break

        cv.release()

        return ans

