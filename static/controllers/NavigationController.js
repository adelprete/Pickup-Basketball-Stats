angular.module('saturdayBall')

.controller('NavigationController', NavigationController);

NavigationController.$inject = ['$scope', '$route', 'Session']

function NavigationController($scope, $route, Session) {

    $scope.user = {};
    $scope.isGroupAdmin = [];

    ////////////////////////

    $scope.$watch('session.currentUser().username', function () {
        $scope.user = Session.currentUser();
        if ($scope.user){
          $scope.isGroupAdmin = $scope.user.admin_groups.filter(group => (group[0] == $route.current.params.groupid));
        }
    });

};
