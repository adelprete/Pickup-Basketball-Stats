'use strict';

// bind featureFlags to rootScope
angular.module('saturdayBall').run(['$rootScope', 'Session', function ($rootScope, Session) {
    $rootScope.session = Session;
}]);
