document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
//    socket.on('connect', () => {
  //      console.log("web socket connected");
   //     document.querySelector('button').onClick = () => {
    //           const username = document.querySelector('#username').value;
     //          socket.emit('I am connected', {'username': username});
      //      };
 //   });
    socket.on('connect', () => {
            socket.emit('I am connected');
           };
    });
    // When new user is connectedn add to the unordered list
    socket.on('new user connected', data => {
       const li = document.createElement('li');
       li.innerHTML = `${data.username} joins the chat room`;
       document.querySelector('#users').append(li);
    });
});
