angular.module('saturdayBall')

.controller('NavigationController', NavigationController);

NavigationController.$inject = ['$scope', '$route', 'Session']

function NavigationController($scope, $route, Session) {

    $scope.user = {};
    $scope.isGroupAdmin = [];
    $scope.$route = $route;

    ////////////////

    $scope.$watch('session.currentUser().username', function () {
        $scope.user = Session.currentUser();
        if ($scope.user) {
          $scope.isGroupAdmin = $scope.user.admin_groups.filter(function(group) { return group[0] == $route.current.params.groupId});
        }
    });

};
