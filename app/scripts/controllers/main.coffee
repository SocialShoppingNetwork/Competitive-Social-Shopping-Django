angular.module('exhibiaApp').controller 'MainCtrl', ($scope, socket)->
  $scope.awesomeThings = [
    'Exhibia'
    'HTML5 Boilerplate'
    'AngularJS'
    'Testacular'
  ]
  socket.on 'news', (data)->
    $scope.awesomeThings.push data.hello
