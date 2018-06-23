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
  $scope.reloadMessage = "";
  $scope.playOptions = playOptions;
  $scope.player = null;
  $scope.PLAYERS = [];
  $scope.search = {};
  $scope.seekToTime = seekToTime;
  $scope.showHideFilter = showHideFilter;
  $scope.user = Session.currentUser();

  /* Update play scope variables */
  $scope.editplay = {};
  $scope.editplaymessage = "";
  $scope.fillEditForm = fillEditForm;
  $scope.updatePlay = updatePlay;
  /* end of update play variables */

  ///////////////////

  init();

  function init() {

    GameService.getGameBoxScore($routeParams['gameId']).then(function(response) {
      $scope.box_scores = response;
    })

    GameService.getGameAdvBoxScore($routeParams['gameId']).then(function(response) {
      $scope.adv_box_scores = response;
    })

    getPlays();

    GameService.getGame($routeParams['gameId']).then(function(response) {
      $scope.game = response;
      //check if this game is a aprt of the group, if not redirect.
      if ($scope.game.group.id.toString() !== $routeParams['groupId']){
        window.location.replace('/group/' + $routeParams['groupId'] + '/games');
        return;
      }
      var params = {date: $scope.game.date, group: $routeParams['groupId']}
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
      $scope.playOptions.PLAYERS = _.map(all_players, function(obj) {
        return {code: obj.id, name: obj.first_name + " " + obj.last_name}
      });

      $scope.$on('youtube.player.ready', function($event, player) {
        $scope.player = player;
      })

    }, function() {});

  };

  function getPlays() {
    GameService.getGamePlays($routeParams['gameId']).then(function(response) {
      $scope.plays = _.orderBy(response, ['time'], ['asc']);
    }, function(response) {
      console.log('Plays failed: ', response);
    })
  }

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

  /* Update Play logic */
  function fillEditForm(playid) {
    GameService.getPlay(playid).then(function (response){
      $scope.editplaymessage = "";
      $scope.editplay = response;
      $scope.editplay.primary_player = response.primary_player.id;
      $scope.editplay.secondary_player = (response.secondary_player && response.secondary_player.id) ? response.secondary_player.id : '';
      $scope.editplay.assist_player = (response.assist_player && response.assist_player.id)? response.assist_player.id : '';
      $scope.editplay.top_play_players = response.top_play_players;
    });
  }

  function updatePlay(play) {
    if (play.secondary_player && !play.secondary_play){
      play.secondary_player = "";
      play.secondary_play = "";
    }
    if (play.assist_player && !play.assist){
      play.assist_player = '';
      play.assist = "";
    }
    if (play.hasOwnProperty('top_play_rank') && !play.top_play_rank){
      play.top_play_rank = "";
    }

    $scope.editplaymessage = "Saving Play...."
    GameService.updatePlay(play).then(function(response){
      $scope.editplaymessage = "Successfully saved.  Game stats are being recalculated.  Refresh the page in a bit to see your changes.";
      getPlays();
      GameService.calculateStatlines($scope.game.id).then(function(response){});
    }, function(response){
      console.log(response);
      $scope.editplaymessage = "Failed to save play";
    });
  }
  /* end of update play logic */
};
