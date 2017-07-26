// Define the `phonecatApp` module
var saturdayBall = angular.module('saturdayBall', [
  'ngRoute',
]);

saturdayBall.config(['$locationProvider', '$routeProvider', function($locationProvider, $routeProvider) {
    $routeProvider
      .when("/add-game-plays", {
        templateUrl: "partials/add_plays.html",
        controller: 'TestController'
      })
      //.when('/', {
      //  template: 'home',
      //});

    $locationProvider.html5Mode(true);
}]);

saturdayBall.controller('TestController', function TestController($scope) {
  $scope.greeting = "hel goVsna"
});
