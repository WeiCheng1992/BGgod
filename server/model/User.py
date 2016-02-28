
class User:
    __uid = -1
    __username = ""
    __password = ""

    def __init__(self, uid,username, password):
        self.__username = username
        self.__password = password
        self.__uid = uid

    def get_uid(self):
        return self.__uid

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password


