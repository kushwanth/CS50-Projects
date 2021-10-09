import os
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect, session
from flask_socketio import *
from collections import deque
import eventlet
eventlet.monkey_patch()
app = Flask(__name__)
app.config["SECRET_KEY"] = 'cs50project2bykushwanth'
socketio = SocketIO(app, async_mode='eventlet')

rooms = ["default"]
userlogged = ["default"]
roomchat = dict()
securerooms = dict()
secureusers = []
limitusers = dict()

#loging in users, creating rooms

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
       session['user'] = request.form.get("user")
       session['room'] = request.form.get("cname")
       if session['user'] in userlogged:
          return "username exits"
       userlogged.append(session['user'])
       if session['room']  not in rooms:
          rooms.append(session['room'])
       if session['room'] not in roomchat.keys():
          roomchat.update({session['room']: deque()})
       return render_template("channel.html", room=session['room'], user=session['user'], msgs=roomchat[session['room']])
    if request.method == "GET":
       if session.get('user') != None and session.get('room') != None:
          return render_template("channel.html", room=session['room'], user=session['user'], msgs=roomchat[session['room']])
       return render_template("home.html", room=rooms)

#private chat login
@app.route("/private", methods=["GET", "POST"])
def private():
    if request.method == "POST":
       user = request.form.get("user")
       room = request.form.get("cname")
       pwd =  request.form.get("pwd")
       if room not in securerooms:
           securerooms.update({room: pwd})
       if pwd != securerooms[room]:
           return "wrong password"
       if user  in secureusers:
          return "username exists"
       secureusers.append(user)
       limitusers.update({room: secureusers})
       if len(limitusers[room]) >2:
          return "Its an 1 to 1 chatroom, and its full"
       return render_template("pchat.html", room=room, user=user)
    return render_template("private.html")

#sending msg to users

@socketio.on('message')
def message(data):
    uname = session.get('user')
    cname = session.get('room')
    msg = data["msg"]
    time = datetime.now()
    timestamp = time.strftime("%Y-%m-%d %H:%M")
    roomchat[cname].append([uname,msg,timestamp])
    if len(roomchat[cname]) > 100:
       roomchat[cname].popleft()
    join_room(cname)
    emit('roommsg', {'user': uname, 'time':timestamp, 'msg':msg}, room=cname)

@socketio.on('pmessage')
def pmessage(data):
    uname = data["user"]
    cname = data["room"]
    msg = data["msg"]
    time = datetime.now()
    timestamp = time.strftime("%Y-%m-%d %H:%M")
    join_room(cname)
    emit('securemsg', {'user': uname, 'time':timestamp, 'msg':msg}, room=cname)

#logging out users

@app.route("/logout", methods=['GET'])
def logout():
    try:
        userlogged.remove(session['user'])
    except ValueError:
        pass
    session.clear()
    return redirect("/")

@app.route("/plogout", methods=['GET', 'POST'])
def plogout():
    if request.method == "POST":
       puser = request.form.get("puser")
       proom = request.form.get("proom")
    try:
        secureusers.remove(puser)
    except ValueError:
        pass
    if len(securerooms[proom]) == 0:
        securerooms.pop(proom)
    return redirect("/")


if __name__ == '__main__':
    socketio.run(app, debug=True)
