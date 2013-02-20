describe 'Controller: AboutCtrl', () ->

  # load the controller's module
  beforeEach module 'exhibiaApp'

  AboutCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller) ->
    scope = {}
    AboutCtrl = $controller 'AboutCtrl', {
      $scope: scope
    }

  it 'should attach a list of awesomeThings to the scope', ->
    expect(scope.awesomeThings.length).toBe 3
