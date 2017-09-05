angular.module('saturdayBall')

.controller('NavigationController', function NavigationController($scope, $routeParams, User){
    User.currentUser().then(function(response){
      $scope.user = response
    });
});
