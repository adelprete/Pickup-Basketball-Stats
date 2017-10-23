'use strict';

angular.module('saturdayBall').run(['$rootScope', 'Session', function ($rootScope, Session) {
    $rootScope.session = Session;
}]);
