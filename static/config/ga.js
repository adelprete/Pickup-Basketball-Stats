'use strict';

angular.module('saturdayBall').run(googleAnalytics);

googleAnalytics.$inject = ['$rootScope', '$location', '$window'];

function googleAnalytics($rootScope, $location, $window) {
    // initialise google analytics
    $window.ga('create', 'UA-66942273-1', 'auto');

    // track pageview on state change
    $rootScope.$on('$routeChangeSuccess', function (event) {
        $window.ga('send', 'pageview', $location.path());
    });
}
