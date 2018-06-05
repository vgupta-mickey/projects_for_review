document.addEventListener('DOMContentLoaded', () => {

   // Connect to websocket
   var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

   //on connect
   socket.on('connect', () => {
           const username = localStorage.getItem("username");
           const channel = localStorage.getItem("channel");
           //if displayname and chatroom is remembered, supply username and chat room info to server so that server can take you ditectly into the chat room
           if (username != null && channel != null)
           {
             console.log('user name and channel info is available');
             socket.emit('join', {'username': username, 'channel': channel});
           }
           //if display name is available, but chat room is not remembered yet, supply username to the server so that it will prompt user to enter chat room
           else if (username != null)
           {
             socket.emit('new user', {'username': username});
           }
           //if display name is not available, ask user to enter it.
           // jusr unhide the part of HTML page to allow user to enter username
           else
           {
             document.querySelector('#nickWrap').style.display = "block";
             document.querySelector('#contentWrap').style.display = "none";
             document.querySelector('#channelWrap').style.display = "none";
           }
   });

   socket.on('client connected',() => {
   });

  // submit buttom to submit username/nickname is disabled by default
   document.querySelector('#nick-submit').disabled = true;

   // Enable button only if there is text in the username input field
   document.querySelector('#nickname').onkeyup = () => {
   if (document.querySelector('#nickname').value.length > 0)
      document.querySelector('#nick-submit').disabled = false;
   else
      document.querySelector('#nick-submit').disabled = true;
   };

   document.querySelector('#channel-submit').disabled = true;

   // Enable button only if there is text in the channel input field
   document.querySelector('#channel').onkeyup = () => {
   if (document.querySelector('#channel').value.length > 0)
      document.querySelector('#channel-submit').disabled = false;
   else
      document.querySelector('#channel-submit').disabled = true;
   };

   document.querySelector('#chatroom-submit').disabled = true;

   // Enable button only if there is text in the message input field
   document.querySelector('#message').onkeyup = () => {
   if (document.querySelector('#message').value.length > 0)
      document.querySelector('#chatroom-submit').disabled = false;
   else
      document.querySelector('#chatroom-submit').disabled = true;
   };

   document.querySelector('#priv-submit').disabled = true;

   // Enable button only if there is text in the private message input field
   document.querySelector('#priv-message').onkeyup = () => {
   if (document.querySelector('#priv-message').value.length > 0 &&
       document.querySelector('#priv-user').value.length > 0)
      document.querySelector('#priv-submit').disabled = false;
   else
      document.querySelector('#priv-submit').disabled = true;
   }

   // Enable button only if there is text in the private message input field
   document.querySelector('#priv-user').onkeyup = () => {
   if (document.querySelector('#priv-message').value.length > 0 &&
       document.querySelector('#priv-user').value.length > 0)
      document.querySelector('#priv-submit').disabled = false;
   else
      document.querySelector('#priv-submit').disabled = true;
   }

   //on submiting username, send username to server over socketio by emiting 'new user' event
   document.querySelector('#setNick').onsubmit = () =>
   {
       var username = document.querySelector('#nickname').value;
       localStorage.setItem("username", username);
       socket.emit('new user', {'username': username});
       document.querySelector('#nickname').value='';
       document.querySelector('#nick-submit').disabled=true;
       return false;
   }

   //on submiting channel info, send username and channel info to server over socketio by emiting 'join' event
   document.querySelector('#setChannel').onsubmit = () => 
   {
       const channel = document.querySelector('#channel').value;
       socket.emit('join', {'username':localStorage.getItem("username"), 'channel': channel});
       localStorage.setItem("channel", channel);
       document.querySelector('#channel').value='';
       document.querySelector('#channel-submit').disabled = true;
       return false;
   }

   //on submiting message, send username, channel and message info to server over socketio by emiting 'message' event
   document.querySelector('#send-message').onsubmit = () => 
   {
      const message = document.querySelector('#message').value;
      socket.emit('message', {'username':localStorage.getItem("username"), 'channel': localStorage.getItem("channel"), 'message':message});
      document.querySelector('#message').value='';
      document.querySelector('#chatroom-submit').disabled = true;
      return false;
   }

   //on submiting private message, send username, private username, and message info to server over socketio by emiting 'priv-message' event

   document.querySelector('#send-priv-message').onsubmit = () => 
   {
      const message = document.querySelector('#priv-message').value;
      const privuser = document.querySelector('#priv-user').value;
      console.log(message);
      console.log(privuser);
      socket.emit('priv-message', {'username':localStorage.getItem("username"), 'priv-user':privuser , 'message':message});
      document.querySelector('#priv-message').value='';
      document.querySelector('#priv-user').value='';
      document.querySelector('#priv-submit').disabled = true;
      return false;
   }

   socket.on('new user connected', data => {
           console.log('user is connected');
   });

   // when a user join a chat room/channel, it receives that 'I join chat room" event along with list of users in chat room and all historical messages (max 100) 
   socket.on('I join chat room', data => {
           message_history = data.message_history;
           users_list = data.users_list;
           var count;
           for (count = 0; count < users_list.length; count++)
           {
              const li = document.createElement('li');
              li.innerHTML = `${users_list[count]}`;
              document.querySelector('#users').append(li);
           }
           document.querySelector('#numOfUsers').innerHTML = users_list.length;
           document.querySelector('#room').innerHTML = localStorage.getItem("channel");
           document.querySelectorAll('.user').forEach(function(span) {
                       span.innerHTML = localStorage.getItem("username");
           });
           ;
           for (count = 0; count < message_history.length; count++)
           {
              const p = document.createElement('p');
              p.innerHTML = `${message_history[count]}`;
              p.innerHTML = `[${message_history[count].time}] ${message_history[count].username}: ${message_history[count].message}`;
              document.querySelector('#chat').append(p);
           }
 
           //hide
           document.querySelector('#nickWrap').style.display = "none";
           document.querySelector('#contentWrap').style.display = "block";
           document.querySelector('#channelWrap').style.display = "none";
   });

   // when a user join a chat room/channel, the other users gets this event to alert them that a new user has joined the chat room.

   socket.on('user join chat room', data => 
   {
           const li = document.createElement('li');
           li.innerHTML = `${data.username}`;
           document.querySelector('#users').append(li);
           var cur_users = document.querySelector('#numOfUsers').innerHTML;
           cur_users++;
           document.querySelector('#numOfUsers').innerHTML = cur_users;
           const p = document.createElement('p');
           p.innerHTML = `[${data.time}] ${data.username} join the chat room`;
           document.getElementById("chat").appendChild(p); 
   });

   // when a user leave the chat room (all the browser tabs are closed and no sockets are open for the user),the other users gets this event to alert them that the user has left the chat room.

   socket.on('user left', data => 
   {
           const p = document.createElement('p');
           p.innerHTML = `[${data.time}] ${data.username} left the chat room`;
           document.getElementById("chat").appendChild(p); 
           var ul = document.getElementById("users");
           var items = ul.getElementsByTagName("li");
           for (var i = 0; i < items.length; ++i) {
            // do something with items[i], which is a <li> element
            if (items[i].textContent === data.username)
            {
               ul.removeChild(ul.childNodes[i]);
               break;
            }
           }
           var cur_users = document.querySelector('#numOfUsers').innerHTML;
           cur_users--;
           document.querySelector('#numOfUsers').innerHTML = cur_users;
   });

   //when a user sends a message in chat room
   socket.on('user message', data => {
           console.log('user message');
           console.log(data);
           const p = document.createElement('p');
           p.innerHTML = `[${data.time}] ${data.username}: ${data.message}`;
           document.getElementById("chat").appendChild(p); 
   });

   //when a user sends a private message
   socket.on('user priv message', data => {
           console.log('priv user message');
           console.log(data);
           const p = document.createElement('p');
           p.innerHTML = `[${data.time}] ${data.username}: ${data.message}`;
           document.getElementById("privchat").appendChild(p); 
   });

   //when a user sends a private message and that needs to get displayed on sender's screen as well
   socket.on('sent priv message', data => {
           console.log('sent user message');
           console.log(data);
           const p = document.createElement('p');
           p.innerHTML = `[${data.time}] message to ${data.username}: ${data.message}`;
           document.getElementById("privchat").appendChild(p); 
   });

   //when a user logged-in first time - user will be asked to enter channel to join
   socket.on('I logged-in', data => 
   {
           console.log('I logged-in');
           console.log(data);
           var count;
           for (count = 0; count < data.length; count++)
           {
              const li = document.createElement('li');
              li.innerHTML = `${data[count]}`;
              document.querySelector('#channelList').append(li);
           }
           document.querySelectorAll('.user').forEach(function(span) {
                       span.innerHTML = localStorage.getItem("username");
           });
           document.querySelector('#nickWrap').style.display = "none";
           document.querySelector('#contentWrap').style.display = "none";
           document.querySelector('#channelWrap').style.display = "block";
   });

   //when a user logged-in failed due to duplicate username
   socket.on('login failed', data => {
           console.log('duplicate display name');
           document.querySelector('#nickError').innerHTML = "Duplicate user";
           document.querySelector('#nickWrap').style.display = "block";
           document.querySelector('#contentWrap').style.display = "none";
           document.querySelector('#channelWrap').style.display = "none";
   });
});
