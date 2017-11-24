const express = require('express');
const app = express();
const server = require('http').Server(app);
const io = require('socket.io')(server);

global.io = io;

let count = 0;

server.listen(7777);

app.use(express.static(__dirname + '/static'));

app.get('/', function(req, res) {
  res.sendfile(__dirname + '/index.html');
});

app.get('/done', function(req, res) {
  global.io.emit('yo');
  res.send('yo');
});

global.io.on('connection', function(socket) {

  setInterval(function() {
    socket.emit('status', { count: count });
  }, 1000);

  socket.emit('count', { count: ++count });

  socket.on('disconnect', function() {
    socket.emit('count', { count: --count });
  });
});
