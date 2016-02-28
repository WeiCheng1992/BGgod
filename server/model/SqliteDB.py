import sqlite3
from User import User


def get_user(username, password):
    DB = sqlite3.connect("./server/model/BGgod.sqlite")
    cu = DB.cursor()
    cu.execute("select * from user where username = ? and password = ?", [username, password])
    l = cu.fetchall()
    cu.close()
    DB.close()
    if len(l) == 0:
        return None
    else:
        return User(l[0][0], l[0][1], l[0][2])
