'use strict';

angular.module('saturdayBall').controller('AddPlaysController', AddPlaysController);

AddPlaysController.$inject = ['$scope', '$routeParams', 'GameService', 'Session', 'playOptions',
  '$anchorScroll', '$timeout'];

function AddPlaysController($scope, $routeParams, GameService, Session, playOptions,
  $anchorScroll, $timeout) {

    $scope.calculateScore = calculateScore;
    $scope.createPlay = createPlay;
    $scope.deletePlay = deletePlay;
    $scope.editplay = {};
    $scope.fillEditForm = fillEditForm;
    $scope.game = {};
    $scope.groupId = $routeParams['groupId']
    $scope.loading = true;
    $scope.play = {};
    $scope.playform = {};
    $scope.playOptions = playOptions;
    $scope.seekToTime = seekToTime;
    $scope.team1_score = "-";
    $scope.team2_score = "-";
    $scope.updatePlay = updatePlay;
    $scope.user = Session.currentUser();

    ///////////////////////

    init();

    function init() {
      $scope.playOptions.PLAYERS = [];
      GameService.getGame($routeParams['gameid']).then(function (response){
        $scope.game = response;
        //Combine all players into an array.  Team1 is first then Team2.
        //Add Team1 and Team2 players later
        var player_objs = $scope.game.team1.concat($scope.game.team2);
        angular.forEach(player_objs, function(value, key) {
          if (value.id !== 5 && value.id !== 6){
            this.push({'code':value.id, 'name': value.first_name + ' ' + value.last_name});
          }
        }, $scope.playOptions.PLAYERS);
        $scope.playOptions.PLAYERS.splice(0, 0, {'code': 5, 'name': "Team1"})
        $scope.playOptions.PLAYERS.splice($scope.game.team1.length, 0, {'code': 6, 'name': "Team2"})

        $scope.loading = false;
        getPlays();
      });

    }

    function getPlays(){
      GameService.getGamePlays($routeParams['gameid']).then(function (response){
        $scope.plays = _.reverse(_.sortBy(response, 'time'));
        calculateScore();
      }, function(response){
      });
    }

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

    function calculateScore() {
      $scope.team1_score = 0;
      $scope.team2_score = 0;
      var scoring_plays = ['fgm', 'threepm'];
      var score_type = $scope.game.score_type;
      var score_to_add;
      _.forEach($scope.plays, function(play){
        if (scoring_plays.includes(play.primary_play)) {
          if (score_type === '2and3'){
            score_to_add = (play.primary_play == 'fgm') ? 2 : 3;
          }
          else {
            score_to_add = (play.primary_play == 'fgm') ? 1 : 2;
          }
          if (_.find($scope.game.team1, function(player) {return play.primary_player.id === player.id;})) {
            $scope.team1_score += score_to_add;
          } else {
            $scope.team2_score += score_to_add;
          }
        }
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
        $scope.editplaymessage = "Successfully saved";
        getPlays();
        calculateScore();
        GameService.calculateStatlines($scope.game.id).then(function(response){});
      }, function(response){
        console.log(response);
        $scope.editplaymessage = "Failed to save play";
      });
    }

    function createPlay(play) {
        play.game = $scope.game.id
        if (play.secondary_player && !play.secondary_play){
          delete play.secondary_player;
        }
        if (play.assist_player && !play.assist){
          delete play.assist_player;
        }
        if (play.secondary_play == null){
          delete play.secondary_play;
          delete play.secondary_player;
        }
        if (play.assist == null){
          delete play.assist;
          delete play.assist_player;
        }
        $scope.message = "Adding Play...."
        GameService.createPlay(play).then(function(response){
          $scope.message = "Successfully Added";
          $scope.play = {};
          $scope.plays.push(response);
          $scope.plays = _.reverse(_.sortBy($scope.plays, 'time'));
          calculateScore();
          GameService.calculateStatlines($scope.game.id).then(function(response){});
          $scope.playform.play.$setUntouched();
          $timeout(function() {
            $anchorScroll("playeranchor");
          }, 1000);
        }, function(response){
          $scope.message = "Failed to add play";
        });
      }

    function deletePlay(playid) {
        GameService.deletePlay(playid).then(function(response){
          _.remove($scope.plays, function(play) { return play.id === playid; });
          calculateScore();
          GameService.calculateStatlines($scope.game.id).then(function(response){});
          calculateScore();
        });
    }


    // YouTube player logic.  Should move to a directive.
    $scope.specifiedTime = null;
    $scope.player = null;
    $scope.playModal = {
      'grabTime': grabTime
    }

    $scope.$on('youtube.player.ready', function($event, player) {
      $scope.player = player;
    })

    function grabTime(offset) {
      var formattedTime, seconds
      if (offset) {
        seconds = $scope.player.getCurrentTime() - offset
        if (seconds < 0) {
          seconds = 0;
        }
      }
      else{
        seconds = $scope.player.getCurrentTime()
      }

      var hours = '' + Math.floor(seconds / 3600)
      if (hours.length < 2){
        hours = '0' + hours;
      }
      var minutes = '' + Math.floor(seconds / 60) % 60
      if (minutes.length < 2){
        minutes = '0' + minutes;
      }
      seconds = '' + Math.floor(seconds % 60)
      if (seconds.length < 2){
        seconds = '0' + seconds;
      }
      formattedTime = hours + ':' + minutes + ":" + seconds
      $scope.play.time = formattedTime;
    }

    $scope.clearRanks = function() {
      $scope.editplay['top_play_rank'] = "";
      $scope.editplay['description'] = "";
      $scope.editplay['top_play_players'] = [];
    }

    function seekToTime(timestamp) {
      var split_time = timestamp.split(':');
      var seconds = parseInt(split_time[0]) * 3600;
      seconds += parseInt(split_time[1]) * 60;
      seconds += parseInt(split_time[2]);
      $scope.player.playVideo();
      $scope.player.seekTo(seconds);
      $anchorScroll("playeranchor");
    };

};
