'use strict';

angular.module('saturdayBall').run(['$rootScope', 'Session', '$templateCache', function ($rootScope, Session, $templateCache) {
    $rootScope.session = Session;
    $rootScope.$on('$viewContentLoaded', function() {
          $templateCache.removeAll(); 
       });
}]);
