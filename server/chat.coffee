userNames = (->
  names = {}
  claim = (name) ->
    if not name or names[name]
      false
    else
      names[name] = true
      true


  # find the lowest unused "guest" name and claim it
  getGuestName = ->
    name = undefined
    nextUserId = 1
    loop
      name = "Guest " + nextUserId
      nextUserId += 1
      break unless not claim(name)
    name


  # serialize claimed names as an array
  get = ->
    res = []
    user = undefined
    for user of names
      res.push user
    res

  free = (name) ->
    delete names[name]  if names[name]

  claim: claim
  free: free
  get: get
  getGuestName: getGuestName
)()

# export function for listening to the socket
module.exports = (socket) ->
  name = userNames.getGuestName()

  # send the new user their name and a list of users
  socket.emit "init",
    name: name
    users: userNames.get()

  # notify other clients that a new user has joined
  socket.broadcast.emit "user:join",
    name: name


  # broadcast a user's message to other users
  socket.on "message:send", (data) ->
    socket.broadcast.emit "message:send",
      user: name
      text: data.message



  # clean up when a user leaves, and broadcast it to other users
  socket.on "disconnect", ->
    socket.broadcast.emit "user:leave",
      name: name
    userNames.free name
