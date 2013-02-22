config = require './config'
socket = require './chat.coffee'
io = require("socket.io").listen(config.port)

io.sockets.on "connection", socket
