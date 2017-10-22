'use strict';

angular.module('saturdayBall').config(function($locationProvider, $routeProvider) {
  var routeResolver = {
    preLoad: function (routeResolver){
      return routeResolver();
    }
  };
    $routeProvider
      .when("/group/:groupid/games/:gameid/add-plays/", {
        templateUrl: "static/views/add_plays.html",
        controller: 'AddPlaysController',
        resolve: routeResolver
      })
      .when("/group/:groupid/settings", {
        templateUrl: 'static/views/settings.html',
        controller: 'GroupSettingsController',
        resolve: routeResolver
      })
      .when("/group/create/", {
        templateUrl: 'static/views/creategroup.html',
        controller: 'CreateGroupController',
        resolve: routeResolver
      })
      .when("/register", {
        templateUrl: 'static/views/register.html',
        controller: 'RegisterController',
        resolve: routeResolver
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
