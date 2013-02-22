config = require './config'
socket = require './socket.js'
io = require("socket.io").listen(config.port)
io.sockets.on "connection", socket
