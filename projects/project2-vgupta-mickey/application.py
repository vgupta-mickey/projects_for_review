import os
import requests
import datetime

from flask import Flask, jsonify, render_template, request, session
from flask_socketio import SocketIO, emit
from flask_socketio import join_room, leave_room
from flask_session import Session


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False 
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app, manage_session=False)

#This is a socket class. Every time a user opens a new socket, a socket object is created. The socket object keeps which username and channel is associated withe the socket.

class sock():
 def __init__(self, sid):
      self.sid = sid
      self.username = None 
      self.channel = None
 def setChannel(self, channel):
      self.channel = channel
 def setUsername(self, username):
      self.username = username
 def getChannel(self):
      return self.channel
 def getUsername(self):
      return self.username

#This is a user class. Every time a user creates username for first time, a user object is created. The user object keeps how many sockets are associated with this user (multiple browser tabs)  and which channel is being used.

class user():
  def __init__(self, username):
     self.username = username
     self.socket_list = set() 
     self.channel = None

  def addChannel(self, channel):
      self.channel = channel

  def deleteChannel(self, channel):
      self.channel = None

  def addSocket(self, sid):
     if sid not in self.socket_list:
        self.socket_list.add(sid)
     else:
        print(f"{sid} exist in {self.username}")

  def deleteSocket(self, sid):
     if sid in self.socket_list:
        self.socket_list.remove(sid)
     else:
        print(f"{sid} does not exist in {self.username}")

  def totalSockets(self):
       return len(self.socket_list)

#This is a channel class. Every time a user creates join a channel, a channel object is created. The channel object keeps how many users are in channel, and it manages the history of messages upto 100.

class channel():
  def __init__(self, channel):
     self.channel = channel
     self.user_list = set()
     self.message_history = [] 

  def addUser (self, user):
     self.user_list.add(user)

  def removeUser(self, user):
     if user in self.user_list:
       self.user_list.remove(user)
     else: 
       print(f"{user} is not in {self.channel}") 

  def addMessage (self, username, cur_time, message):
     if (len(self.message_history) < 100):
        self.message_history.append({"username":username, "time":cur_time, "message":message})
     else:
        del self.message_history[0]
        self.message_history.append({"username":username, "time":cur_time, "message":message})
  def isUserExist(self, username):
     if username in self.user_list:
       return True
     else:
       return False
  def totalUsers(self):
       return len(self.user_list)
    

#socket map - it manages, the list of open sockets.
socket_map = {}

#user map - it manages list of unique users currenly being active 
user_map = {}

#channel_map - it manages the list of chanells currenly being active
channel_map = {}

# initial route when user enters 120.0.0.1:5000

@app.route("/")
def index():
    return render_template("index.html")

# when client connects web socket - a socket object is created.

@socketio.on('connect')
def client_connect():
    socket_map[request.sid] = sock(request.sid)
    emit("client connected")

# when a client disconnects  - kill browser Tab or close the browser.
# user will be removed from user_map if all of the its open sockets are closed
#if user is removed from user map, we declare that user is leaving the channel/chatroom

@socketio.on('disconnect')
def client_disconnect():
    print('Client disconnected')

    sock_obj = socket_map[request.sid]
    
    username = sock_obj.getUsername()
    channel_name = sock_obj.getChannel()
    del socket_map[request.sid]
    if username in user_map:
       user_map[username].deleteSocket(request.sid)
       if (user_map[username].totalSockets() == 0):
          del user_map[username]
          leave_room(username)
          on_leave({"username":username, "channel":channel_name})
       else:
          print("user still has few more sockets open")
    else:
       print("problem - no user associated to socket")

      
# when a client enters user name for first time . A user object is created.
# we will add the socket in user_obj. This will send the list of current channels available for user to enter.

@socketio.on("new user")
def user_connected(data):
    print("user is connected")
    username = data["username"]
    
    if username in user_map:
      emit("login failed")
    else:
      user_map[username] = user(username)
      user_map[username].addSocket(request.sid)
      if request.sid in socket_map:
        socket_map[request.sid].setUsername(username)
      else:
        print("sid not in socket_map")

      emit("I logged-in", list(channel_map.keys()))
      emit("new user connected", {"username": username}, broadcast=True)

# when a client enters user name and channel or if a user enters 127.0.0.1:5000 in new Tab and browser remembers the username and channel info.
# This will take user into chat room.

@socketio.on('join')
def on_join(data):
    username = data['username']
    channel_name = data['channel']
    if request.sid in socket_map:
       socket_map[request.sid].setUsername(username)
       socket_map[request.sid].setChannel(channel_name)
    else:
       print("error socket sid not in socket_map")

    if username not in user_map:
      user_map[username] = user(username)
    user_map[username].addSocket(request.sid)
    user_map[username].addChannel(channel_name)

    user_already_in_room = False
    if channel_name in channel_map:
      if channel_map[channel_name].isUserExist(username) == True:
        user_already_in_room = True
      else:
        channel_map[channel_name].addUser(username)
    else:
      channel_map[channel_name] = channel(channel_name)
      channel_map[channel_name].addUser(username)
      

    cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    join_room(channel_name)
    join_room(username)
    emit("I join chat room",{"message_history":channel_map[channel_name].message_history, "users_list":list(channel_map[channel_name].user_list)})
    if (user_already_in_room == False):
      emit("user join chat room", {"username":username,"time":cur_time}, include_self=False, room=channel_name)


# this will invoke when a user sends message. The message is broadcast to the chatroom/channel. Also, the message is saved under channle object.

@socketio.on('message')
def on_message(data):
    username = data['username']
    channel_name = data['channel'] 
    message = data['message']
    cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if channel_name in channel_map:
        channel_map[channel_name].addMessage(username, cur_time, message)
    else:
      print("error no channel in channel map")

    emit("user message", {"username":username,"time":cur_time, "message":message}, room=channel_name)

# this will invoke when a user sends private message. The message is broadcast to the all the open sockets of the target user.

@socketio.on('priv-message')
def on_privmessage(data):
    username = data['username']
    message = data['message']
    remoteusername = data['priv-user']
    cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    emit("user priv message", {"username":username,"time":cur_time, "message":message}, room=remoteusername)
    emit("sent priv message", {"username":remoteusername,"time":cur_time, "message":message})

# this will invoke when a user leave the chat room.
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    channel_name = data['channel']
    if channel_name in channel_map:
      channel_map[channel_name].removeUser(username)
      if channel_map[channel_name].totalUsers() == 0:
        del channel_map[channel_name]
    else:
      print("no channel error")

    cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    leave_room(channel_name)

    emit("user left", {"username":username,"time":cur_time}, include_self=False, room=channel_name)


if __name__ == '__main__':
   socketio.run(app, debug = True)

