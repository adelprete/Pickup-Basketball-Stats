angular.module('saturdayBall')

.controller('NavigationController', NavigationController);

NavigationController.$inject = ['$scope', '$route', 'Session', 'RoleHelper']

function NavigationController($scope, $route, Session, RoleHelper) {

    $scope.groupId = "";
    $scope.RoleHelper = RoleHelper;
    $scope.user = {};
    $scope.$route = $route;

    ////////////////

    $scope.$watch('session.currentUser().username', function () {
        $scope.user = Session.currentUser();
    });

};
