angular.module('saturdayBall')

.controller('NavigationController', function NavigationController($scope, $route, $routeParams, User){

    User.currentUser().then(function(response){
      $scope.user = response
      $scope.isGroupAdmin = $scope.user.admin_groups.filter(group => (group[0] == $route.current.params.groupid));
    });
});
