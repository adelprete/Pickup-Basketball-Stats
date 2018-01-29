'use strict';

angular.module('saturdayBall')

.controller('GameController', GameController);

GameController.$inject = ['$scope', '$routeParams', 'GameService', 'Session', 'RoleHelper',
  '$anchorScroll', 'playOptions', '$http']

function GameController($scope, $routeParams, GameService, Session, RoleHelper,
  $anchorScroll, playOptions, $http) {

  $scope.adv_box_scores = null;
  $scope.box_scores = null;
  $scope.exportPlays = exportPlays;
  $scope.filterFormVisible = false;
  $scope.game = null;
  $scope.groupId = $routeParams['groupId'];
  $scope.playOptions = playOptions;
  $scope.player = null;
  $scope.PLAYERS = [];
  $scope.seekToTime = seekToTime;
  $scope.showHideFilter = showHideFilter;
  $scope.user = Session.currentUser();

  ///////////////////

  init();

  function init() {

    GameService.getGameBoxScore($routeParams['gameId']).then(function(response) {
      $scope.box_scores = response;
    })

    GameService.getGameAdvBoxScore($routeParams['gameId']).then(function(response) {
      $scope.adv_box_scores = response;
    })

    GameService.getGamePlays($routeParams['gameId']).then(function(response) {
      $scope.plays = response;
    })

    GameService.getGame($routeParams['gameId']).then(function(response) {
      $scope.game = response;
      var params = {date: $scope.game.date}
      GameService.getGames($routeParams['groupId'], params).then(function(response) {
        var games = response;
        for (var i = 0; i < games.length; i++) {
          if (games[i].id === $scope.game.id) {
            $scope.next_game = i+1 < games.length ? games[i+1] : null;
            $scope.prev_game = i-1 >= 0 ? games[i-1] : null;
          }
        }
      })

      var all_players = $scope.game.team1.concat($scope.game.team2);
      $scope.PLAYERS = _.map(all_players, function(obj) {
        return {code: obj.id, name: obj.first_name + " " + obj.last_name}
      });

      $scope.$on('youtube.player.ready', function($event, player) {
        $scope.player = player;
      })

    }, function() {});

  };

  var jumpToPlayerAnchor = function() {
    $anchorScroll("playeranchor");
  }

  function seekToTime(timestamp) {
    var split_time = timestamp.split(':');
    var seconds = parseInt(split_time[0]) * 3600;
    seconds += parseInt(split_time[1]) * 60;
    seconds += parseInt(split_time[2]);
    $scope.player.playVideo();
    $scope.player.seekTo(seconds);
    jumpToPlayerAnchor();
  };

  function showHideFilter() {
    $scope.filterFormVisible = $scope.filterFormVisible ? false : true;
  };

  function exportPlays() {
    $http({method: 'GET', url: '/api/games/656/export'}).then(function(response) {
      console.log('response: ', response);
    }, function(response) {
      console.log('failed: ', response)
    })
  }
};
