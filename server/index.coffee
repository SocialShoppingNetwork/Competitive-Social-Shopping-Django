config = require './config'
io = require("socket.io").listen(config.port)
io.sockets.on "connection", (socket) ->
  socket.emit "news",
    hello: "world"

  socket.on "my other event", (data) ->
    console.log data

