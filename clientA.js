var io = require('socket.io-client'),
    socket = io.connect('http://lilsonar.nodejitsu.com');

socket.on('connect', function() {
  console.log('connected to server');
});

socket.on('go', function(){
  var path =  process.cwd() + '',
      exec = require('child_process').exec,
      child;
  console.log(path);
  child = exec('python C:\\superbasic\\ListenandSpeak_ROUGHA.py 1' , function (error, stdout, stderr) {
    console.log('stdout: ' + stdout);
    console.log('stderr: ' + stderr);
    if (error !== null) {
      console.log('exec error: ' + error);
    }
  socket.emit('scriptRan');
  });
});

socket.on('requestData', function() {
  var fs = require('fs'),
      filename = 'A.txt';
  fs.exists(filename, function(exists) {
    if (exists) {
      fs.readFile(filename, 'utf8', function(err, data) {
        if (err) {throw err;}
        console.log('sending data');
        socket.emit('sendDataToServer', data);
        socket.on('returnDataToClient',function(data) {
          var fs = require('fs');
          fs.writeFile("B.txt", data, function(err) {
            if(err) {
              console.log(err);
            } else {
              console.log("The file was saved!");
            }
            var path = process.cwd() + '',
              exec = require('child_process').exec,
              child;
            child = exec('python C:\\superbasic\\distance.py', function (error, stdout, stderr) {
              console.log('stdout: ' + stdout);
              console.log('stderr: ' + stderr);
              if (error !== null) {
                console.log('exec error: ' + error);
              }
              console.log('disconnecting...');
              socket.emit('disconnectMe', function() {
                socket.disconnect();
              });
            });
          }); 
        });
      });
    }
    else {
      console.log('file not ready');
      socket.emit('fileNotReady');
    }
  });
});

socket.on('disconnect', function() {
  socket.emit('disconnectMe');
});

