'use strict';

angular.module('saturdayBall')

.controller('GameController', GameController);

GameController.$inject = ['$scope', '$routeParams', 'GameService', 'Session', 'RoleHelper',
  '$anchorScroll', 'playOptions']

function GameController($scope, $routeParams, GameService, Session, RoleHelper,
  $anchorScroll, playOptions) {

  $scope.adv_box_scores = null;
  $scope.box_scores = null;
  $scope.filters = {
    primary_play: '',
    secondary_play: '',
    assist: '',
    primary_player: {'id': ''},
    secondary_player: {'id': ''},
    assist_player: {'id': ''}
  };
  $scope.filterFormVisible = false;
  $scope.game = null;
  $scope.groupId = $routeParams['groupId'];
  $scope.playOptions = playOptions;
  $scope.player = null;
  $scope.PLAYERS = [];
  $scope.search = {};
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
      $scope.plays = _.orderBy(response, ['time'], ['asc']);
    }, function(response) {
      console.log('Plays failed: ', response);
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

  $scope.$watch('filters', function () {
    $scope.search = {};
    if($scope.filters.primary_play) {
      $scope.search.primary_play = $scope.filters.primary_play;
    }
    if($scope.filters.secondary_play) {
      $scope.search.secondary_play = $scope.filters.secondary_play;
    }
    if($scope.filters.assist_play) {
      $scope.search.assist_play = $scope.filters.assist_play;
    }
    if($scope.filters.primary_player.id) {
      $scope.search.primary_player = {
        id: $scope.filters.primary_player.id
      }
    }
    if($scope.filters.secondary_player.id) {
      $scope.search.secondary_player = {
        id: $scope.filters.secondary_player.id
      }
    }
    if($scope.filters.assist_player.id) {
      $scope.search.assist_player = {
        id: $scope.filters.assist_player.id
      }
    }
  }, true);
};
