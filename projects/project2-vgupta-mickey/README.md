# Project 2

Web Programming with Python and JavaScript

The overall idea of the project is to load the HTML page one time and change/update the content of page using java script and socketio. I have used displayname/username/nickname  for user identify and chatroom/channel for channel identity interchangeably.


The way I designed is that I have HTML page with all the informations needed for user to enter displayname/username, channel/chatroom info and sending and receiving messages. However, I keep the HTML page info hide initially and will unhide based on the what is available in the localStorage. The HTML page will have main 3 peice of the information - getting user's displayname, getting user's channel info, and main chat window to exchaing the messages. Each peice will be unide based on what is available into the localStorage.

So, if user opens browser and type 127.0.0.1:5000 first time, it will be prompted for entering its displayname/username.This happens because javascript will look if localStorage has username present, if it is not, it will unhide certain piece of HTML page.  If localStorage has displayname remembered, it will skip this step and will look for channel/chatroom if the browser remembered the channel info. If not, it will prompt the user to either enter all together new channel (create new one) or will be asked to enter one of the existing channels/chatroom. If browser remembers, it will take the user into the last joined chatroom. 
    - The screen will show upto 100 messages exchanged in the chatroom.
    - Total users in the chatroom
    - The list of the users
    - The total user, list of users will update lively if a user leave/join the chatroom.

The user will also be provided with separate private chat room window where user can send/receive private messages from other users in the chatroom. [private messaging implementation - personal touch]

Another point I would like to highight is that if a user opens new browser tab and types 127.0.0.1:5000, it will take him to chatroom directly. Effectively, user opened multiple sockets to the server. If user closes all the Tab, the server eventually closes all the sockets and chatroom will be notified that user has left the chatroom. Everytime, user enters into the chatroom, chatroom will be notified.

I could have implemented where user can allow user to change the chatroom but it increses the scope of the project, so I din't as it is not needed for the project. 


The following artifacts are generated:

1)static/js/index.js - Javascript code. 
The file is self explanatory and have lots of comments.
Idea is that when page is loaded and websocket is connected, localStorage is checked for username and channel info. 
  "new user" event is generated if user enters "displayname" or localStorage has userinfo but no channel info.
  "join" even is generated if localStorage has userinfo and channel info. or user is prompted to enter channel info.
 "message" event is generated if user send message in chat room.
 "priv-message" event is generated if user send private message to a specific user.


  The folloiwng events are received by client :
   1. "I logged-in" event is triggered when the server gets user's display name and would like the user to enter channel info. The user will be provided with the list of channels available. 
   1. "I join the chat room" event is triggered at javascript when the server has username and channel info for the user and server wants to take the user into the chatroom with message-history and list of users.
   2. "user join the chat room" event is triggered when a new user eneters into the chatroom. A

   3. "user left" event is triggered when a user leave the chat room.
   
   4. "user message" event is triggered when a user sends message to chatroom.
   5. "priv user message" is triggered when a user sends a private message to that user
   6. "sent priv message" is triggered when the client sends a private mesage to other user and wants to display the message exchange on its own screen.
   8. "loggin failed" event is triggered when user enters a displayname which is already taken by someone"



2 )static/css/style.css

  This is for styling.

3)template/index.html

  HTML page with main three pieces of the information wrapped with ID=nickWrap for enetring displayname, ID=channelWrap for entering channel info and ID=contentWrap for chatroom.

4)application.py

The is server side Flask code. Flask socketip uses join_room/leave_room features of socketio.

The way code is managed is that I created 2 class objects - socket, user and channel. Three dictionaries are maintained - socket_map, user_map and channel_map.

 scket_obj is created when a new socket is opened and it maintains which user/channel is associated with socket.
 user_obj is created when a new user is enters into the chatroom and it maintains which channel and how many sockets are opened for the user.
 channel_obj is created when a new channel is created by a user. It maintains the list of users who are in this channel and history of the messages for the channel.

