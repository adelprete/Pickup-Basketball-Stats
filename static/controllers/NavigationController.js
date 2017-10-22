angular.module('saturdayBall')

.controller('NavigationController', function NavigationController($scope, $rootScope, $route, $routeParams, Session){

    $scope.$watch('session.currentUser().username', function (curValue, oldValue) {

        $scope.user = Session.currentUser();

        if ($scope.user){
          $scope.isGroupAdmin = $scope.user.admin_groups.filter(group => (group[0] == $route.current.params.groupid));
        }
    });

});
