'use strict'

angular.module('exhibiaApp').controller 'ChatCtrl', ($scope, socket) ->

  # Socket listeners

  socket.on 'init', (data) ->
    $scope.name = data.name
    $scope.users = data.users

  socket.on 'send:message', (message) ->
    $scope.messages.push message

  socket.on 'user:join', (data) ->
    $scope.messages.push({
      user: 'chatroom',
      text: 'User ' + data.name + ' has joined.'
    })
    $scope.users.push data.name
    console.log $scope.users, 'user list'

  # add a message to the conversation when a user disconnects or leaves the room
  socket.on 'user:left', (data) ->
    $scope.messages.push({
      user: 'chatroom',
      text: 'User ' + data.name + ' has left.'
    })
    i = 0
    while i < $scope.users.length
      user = $scope.users[i]
      if user is data.name
        $scope.users.splice i, 1
        break
      i++

  # Private helpers

  $scope.messages = []

  $scope.sendMessage = () ->
    socket.emit 'send:message', {
      message: $scope.message
    }

    # add the message to our model locally
    $scope.messages.push({
      user: $scope.name,
      text: $scope.message
    })

    # clear message box
    $scope.message = ''
