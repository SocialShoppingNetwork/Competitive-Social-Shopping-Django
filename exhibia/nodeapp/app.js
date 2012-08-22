/**
 * Module dependencies.
 */

var express = require('express')
  , stylus = require('stylus')
  , nib = require('nib')
  , sio = require('socket.io');
var nMemcached = require( 'memcached')
memcached = new nMemcached( "127.0.0.1:11211");
var io=null;
/**
 * App.
 */

var app = express.createServer();

/**
 * App configuration.
 */
app.use(express.bodyParser());

app.configure(function () {
  app.use(stylus.middleware({ src: __dirname + '/public', compile: compile }));
  app.use(express.static(__dirname + '/public'));
  app.set('views', __dirname);
  app.set('view engine', 'jade');

  function compile (str, path) {
    return stylus(str)
      .set('filename', path)
      .use(nib());
  };
});

/**
 * App routes.
 */

app.post('/message/', function (req, res) {
  //console.log(req.body);
  console.log('index==============');
  console.log(req.body);
  io.sockets.emit('user_message', req.body.username, req.body.message, req.body.picture);
  res.send('OK');
});

app.post('/ban-user/', function (req, res) {
  io.sockets.emit('ban_user', req.body.username);
  res.send('OK');
});
/**
 * App listen.
 */

var port = process.env.PORT || 4000;
console.log('POOOOORT ' + port);
app.listen(port, function () {
  var addr = app.address();
  console.log('   app listening on http://' + addr.address + ':' + addr.port);
});

/**
 * Socket.IO server (single process only)
 */

var io = sio.listen(app, {log:false})
  , nicknames = {};

// Set our transports
if (process.env.PORT){
io.configure(function () { 
  io.set("transports", ["xhr-polling"]); 
  io.set("polling duration", 20); 
});
}

io.sockets.on('connection', function (socket) {
  socket.on('user message', function (msg) {
    socket.broadcast.emit('user message', socket.nickname, msg);
  });

  socket.on('nickname', function (nick, fn) {
    if (nicknames[nick]) {
      fn(true);
    } else {
      fn(false);
      nicknames[nick] = socket.nickname = nick;
      socket.broadcast.emit('announcement', nick + ' connected');
      io.sockets.emit('nicknames', nicknames);
    }
  });

  socket.on('disconnect', function () {
    if (!socket.nickname) return;

    delete nicknames[socket.nickname];
    socket.broadcast.emit('announcement', socket.nickname + ' disconnected');
    socket.broadcast.emit('nicknames', nicknames);
  });

  socket.on('update', function (data) {
    //console.log("-------------------------");
    //console.log(data);
    //console.log("-------------------------");

    if (data){
      memcached.get("bidstick:1:a_" + data['id'], function( err, result ){
        if( err ) console.error( err );
        //console.log('>>>>>>>>>>>>>>>>>>>');
        //console.log(result);
        socket.volatile.emit('update', {'auctions':result});
        //console.log('<<<<<<<<<<<<<<<<<<<<');
          //socket.volatile.emit('update', {'auctions':result});
      });
            
    }else{
    	memcached.get( "bidstick:1:auctions_json", function( err, result ){
    		if( err ) console.error( err );
		//console.log(result);
        	socket.volatile.emit('update', {'auctions':result});
    	});
    }

  });

});
