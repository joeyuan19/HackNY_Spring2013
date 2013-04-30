var app = require('express')(),
    server = require('http').createServer(app),
    io = require('socket.io').listen(server),
    port = 8080,
    url = 'http://localhost:' + port + '/';

if (process.env.SUBDOMAIN) {
  url = 'http://' + process.env.SUBDOMAIN + 'jit.su/'
}
server.listen(port);
app.get('/', function (req, res) {
  res.sendfile(io.sockets.clients('test').length);
});
io.sockets.on('connection', function (socket) {
  var len_clients = io.sockets.clients('test').length;
  if (len_clients < 2) {
    socket.join('test');
    len_clients += 1;
  }
  console.log('number clients: ' + len_clients + '\n');  
  if ( len_clients === 2 ) {
    console.log('sending start signal');
    io.sockets.in('test').emit('go');
  }
  socket.on('scriptRan', function() {
    this.emit('requestData');
  });
  socket.on('fileNotReady', function() {
    this.emit('requestData');
  });
  socket.on('sendDataToServer', function (data) {
    console.log('data received:\n');
    console.log('' + data + '\nSending...\n');
    this.broadcast.to('test').emit('returnDataToClient', data);
  });
});
