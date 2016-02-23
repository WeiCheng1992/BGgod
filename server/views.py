from flask import render_template, session, request
from server import app


@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
def index():
    return render_template("index.html",
        title = 'Home',
        user = user)





def launch():
    app.run(debug=True, port=12138)

