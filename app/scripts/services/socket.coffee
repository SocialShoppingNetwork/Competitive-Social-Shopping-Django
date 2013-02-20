angular.module('exhibiaApp').factory 'socket', ($rootScope) ->
  # save to local var and destroy global var
  io = window.io
  delete window.io
  # start connecting
  socket = io.connect('http://localhost:5000')
  on: (eventName, callback) ->
    socket.on eventName, ->
      args = arguments
      $rootScope.$apply ->
        callback.apply socket, args
  emit: (eventName, data, callback) ->
    socket.emit eventName, data, ->
      args = arguments
      $rootScope.$apply ->
        callback.apply socket, args if callback
