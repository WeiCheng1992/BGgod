class Character:
    __is_alive = False
    __STAGE = None

    def __init__(self,stage):
        self.__is_alive = True
        self.__STAGE = stage

    def dead(self):
        self.__is_alive = False

    def is_alive(self):
        return self.__is_alive

    def dead_function(self):
        return []

    def take_action(self, context, cv, room_id = None, play_id = None):
        return []

    def is_active(self, turn):
        return False

    def get_stage(self):
        return self.__STAGE

