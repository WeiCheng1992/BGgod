from flask import render_template, session, request ,redirect , url_for ,flash
from server import app


@app.route('/OpenRoom', methods = ['GET'])
def openroom():
    return render_template('OpenRoom.html')


@app.route('/createroom', methods = ['POST', 'GET'])
def createroom():
    people = int(request.form.get('people', 0))
    wolf = int(request.form.get('wolf', 0))
    villager = int(request.form.get('villager', 0))

    cupid = 0 if request.form.get('cupid', 0) == 0 else 1
    prophet = 0 if request.form.get('prophet', 0) == 0 else 1
    guard = 0 if request.form.get('guard', 0) == 0 else 1
    hunter = 0 if request.form.get('hunter', 0) == 0 else 1
    witch = 0 if request.form.get('witch', 0) == 0 else 1

    return 'a'




