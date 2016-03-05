import sqlite3
from User import User
from server import app
from flask import g


def connect_to_database():
    return sqlite3.connect("./server/model/BGgod.sqlite")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def get_user(username, password):
    cu = get_db().cursor()
    cu.execute("select * from user where username = ? and password = ?", [username, password])
    l = cu.fetchall()
    cu.close()
    if len(l) == 0:
        return None
    else:
        return User(l[0][0], l[0][1], l[0][2])


def add_user(username, password):
    db = get_db()
    cu = db.cursor()
    cu.execute("insert into user(username, password) values(?,?)", [username, password])
    db.commit()
    cu.close()
    return get_user(username, password)