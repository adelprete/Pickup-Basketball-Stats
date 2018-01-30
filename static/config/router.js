'use strict';

angular.module('saturdayBall').config(['$locationProvider', '$routeProvider', function($locationProvider, $routeProvider) {
  var routeResolver = {
    preLoad: function (routeResolver){
      return routeResolver()
    }
  };
    $routeProvider
      .when("/group/:groupId/games/", {
        templateUrl: "static/views/games.html",
        controller: 'GamesController',
        resolve: routeResolver,
        activetab: 'games'
      })
      .when("/group/:groupId/games/:gameId/", {
        templateUrl: "static/views/game.html",
        controller: 'GameController',
        resolve: routeResolver,
        activetab: 'games'
      })
      .when("/group/:groupId/games/:gameid/add-plays/", {
        templateUrl: "static/views/add_plays.html",
        controller: 'AddPlaysController',
        resolve: routeResolver,
        activetab: 'games'
      })
      .when("/group/:groupId/settings", {
        templateUrl: 'static/views/settings.html',
        controller: 'GroupSettingsController',
        resolve: routeResolver,
        activetab: 'settings'
      })
      .when("/group/create/", {
        templateUrl: 'static/views/creategroup.html',
        controller: 'CreateGroupController',
        resolve: routeResolver
      })
      .when("/register/", {
        templateUrl: 'static/views/register.html',
        controller: 'RegisterController',
        resolve: routeResolver
      })
      .when("/group/:groupId/leaderboard/", {
        templateUrl: 'static/views/leaderboard.html',
        controller: 'LeaderboardController',
        resolve: routeResolver,
        activetab: 'leaderboard'
      })
      .when("/accept-invite/:inviteCode/", {
        resolve: routeResolver,
      })
      .otherwise({
        resolve: {
          factory: checkRouting
        }
      });

    $locationProvider.html5Mode(true);
}]);

angular.module('saturdayBall').config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

var checkRouting= function ($q, $rootScope, $location) {
  var path = $location.path();
  window.location = $location.host()+ ':8000' + path;
}
