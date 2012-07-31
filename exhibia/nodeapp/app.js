var io = require('socket.io').listen(4000);
var	nMemcached = require( 'memcached')
memcached = new nMemcached( "127.0.0.1:11211" );

io.sockets.on('connection', function (socket) {
  socket.emit('news', { hello: 'world' });
  socket.on('my other event', function (data) {
    console.log(data);
  });

  socket.on('update', function (data) {
    console.log("-------------------------");
    console.log(data);
    console.log("-------------------------");

    if (data){
      memcached.get("bidstick:1:a_" + data['id'], function( err, result ){
        if( err ) console.error( err );
        console.log('>>>>>>>>>>>>>>>>>>>');
        console.log(result);
        socket.volatile.emit('update', {'auctions':result});
        console.log('<<<<<<<<<<<<<<<<<<<<');
          //socket.volatile.emit('update', {'auctions':result});
      });
            
    }else{
    	memcached.get( "bidstick:1:auctions_json", function( err, result ){
    		if( err ) console.error( err );
		console.log(result);
        	socket.volatile.emit('update', {'auctions':result});
    	});
    }

  });

});
