'use strict';

angular.module('saturdayBall').config(function($locationProvider, $routeProvider) {
    $routeProvider
      .when("/games/:gameid/add-plays/", {
        templateUrl: "static/views/add_plays.html",
        controller: 'AddPlaysController'
      })
      .when("/settings", {
        templateUrl: 'static/views/settings.html',
        controller: 'SettingsController'
      })
      .otherwise({
        resolve: {
          factory: checkRouting
        }
      });

    $locationProvider.html5Mode(true);
});

angular.module('saturdayBall').config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

var checkRouting= function ($q, $rootScope, $location) {
  var path = $location.path();
  window.location = $location.host()+ ':8000' + path;
}
