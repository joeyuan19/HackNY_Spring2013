var io = require('socket.io-client'),
    socket = io.connect('http://localhost:8080'),
    file_created = 0;
socket.on('connect', function() {
  console.log('connected to server');
});

socket.on('go', function(){
  var path =  process.cwd() + '',
      exec = require('child_process').exec,
      child;
  console.log(path);
  child = exec('python ' + path + '/testcreate.py' , function (error, stdout, stderr) {
    console.log('stdout: ' + stdout);
    console.log('stderr: ' + stderr);
    if (error !== null) {
      console.log('exec error: ' + error);
    }
  });
  socket.emit('scriptRan');
});

socket.on('requestData', function() {
  var fs = require('fs'),
      filename = 'Output.txt';
  fs.exists(filename, function(exists) {
    if (exists) {
      fs.readFile(filename, 'utf8', function(err, data) {
        if (err) {throw err;}
        console.log('sending data');
        socket.emit('sendDataToServer', data);
        socket.on('returnDataToClient',function(data) {
          console.log('data received:\n' + data);
        });
      });
    }
    else {
      console.log('file not ready');
      socket.emit('fileNotReady');
    }
  });
});

