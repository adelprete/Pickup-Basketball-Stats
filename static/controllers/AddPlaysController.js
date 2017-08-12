'use strict';

angular.module('saturdayBall').controller('AddPlaysController', function AddPlaysController($scope, $routeParams, GameService) {
    // CONSTANTS
    $scope.OPTIONS = {
      PRIMARY_PLAY: [
          {'code': 'fgm', 'name': 'FGM'},
          {'code': 'fga', 'name': 'FGA'},
          {'code': 'threepm', 'name': '3PM'},
          {'code': 'threepa', 'name': '3PA'},
          {'code': 'blk', 'name': 'BLK'},
          {'code': 'to', 'name': 'TO'},
          {'code': 'pf', 'name': 'FOUL'},
          {'code': 'sub_out', 'name': 'SUB OUT'},
          {'code': 'misc', 'name': 'Misc'}
      ],
      SECONDARY_PLAY: [
          {'code': 'dreb', 'name': 'DREB'},
          {'code': 'oreb', 'name': 'OREB'},
          {'code': 'stls', 'name': 'STL'},
          {'code': 'ba', 'name': 'Block Against'},
          {'code': 'fd', 'name': 'Foul Drawn'},
          {'code': 'sub_in', 'name': 'SUB IN'},
      ],
      ASSIST_PLAY: [
          {'code': 'pot_ast', 'name': 'Potential Assist'},
          {'code': 'asts', 'name': 'Assist'}
      ],
      PLAY_RANKS: [
          {'code': 't01', 'name': 'Top 1'},
          {'code': 't02', 'name': 'Top 2'},
          {'code': 't03', 'name': 'Top 3'},
          {'code': 't04', 'name': 'Top 4'},
          {'code': 't05', 'name': 'Top 5'},
          {'code': 't06', 'name': 'Top 6'},
          {'code': 't07', 'name': 'Top 7'},
          {'code': 't08', 'name': 'Top 8'},
          {'code': 't09', 'name': 'Top 9'},
          {'code': 't10', 'name': 'Top 10'},
          {'code': 'nt01', 'name': 'Not Top 1'},
          {'code': 'nt02', 'name': 'Not Top 2'},
          {'code': 'nt03', 'name': 'Not Top 3'},
          {'code': 'nt04', 'name': 'Not Top 4'},
          {'code': 'nt05', 'name': 'Not Top 5'},
          {'code': 'nt06', 'name': 'Not Top 6'},
          {'code': 'nt07', 'name': 'Not Top 7'},
          {'code': 'nt08', 'name': 'Not Top 8'},
          {'code': 'nt09', 'name': 'Not Top 9'},
          {'code': 'nt10', 'name': 'Not Top 10'},
      ]
    }
    $scope.editplay = {};
    $scope.play = {};

    GameService.getGame($routeParams['gameid']).then(function (response){
      $scope.game = response;
      $scope.OPTIONS.players = []
      var player_objs = $scope.game.team1.concat($scope.game.team2);
      angular.forEach(player_objs, function(value, key) {
        this.push({'code':value.id, 'name': `${value.first_name} ${value.last_name}`});
      }, $scope.OPTIONS.players);
      getPlays();
    }, function(response){
    });

    var getPlays = function(){
      GameService.getGamePlays($routeParams['gameid']).then(function (response){
        $scope.plays = _.reverse(_.sortBy(response, 'time'));
        calculateScore();
      }, function(response){
      });
    };

    $scope.fillEditForm = function(playid){
      GameService.getPlay(playid).then(function (response){
        $scope.editplaymessage = "";
        $scope.editplay = response;
        $scope.editplay.primary_player = response.primary_player.id;
        $scope.editplay.secondary_player = (response.secondary_player && response.secondary_player.id) ? response.secondary_player.id : '';
        $scope.editplay.assist_player = (response.assist_player && response.assist_player.id)? response.assist_player.id : '';
        $scope.editplay.top_play_players = response.top_play_players;
      }, function(response){

      })
    }

    var calculateScore = function(){
      $scope.team1_score = 0;
      $scope.team2_score = 0;
      var scoring_plays = ['fgm', 'threepm'];
      _.forEach($scope.plays, function(play){
        if (scoring_plays.includes(play.primary_play)) {
          var score_to_add = (play.primary_play == 'fgm') ? 1 : 2;
          if (_.find($scope.game.team1, player => play.primary_player.id === player.id)) {
            $scope.team1_score += score_to_add;
          } else {
            $scope.team2_score += score_to_add;
          }
        }
      });
    }

    $scope.update = function(play) {
      if (play.secondary_player && !play.secondary_play){
        play.secondary_player = "";
        play.secondary_play = "";
      }
      if (play.assist_player && !play.assist){
        play.assist_player = '';
        play.assist = "";
      }
      $scope.editplaymessage = "Saving Play...."
      GameService.updatePlay(play).then(function(response){
        $scope.editplaymessage = "Successfully saved";
        getPlays();
        calculateScore();
      }, function(response){
        $scope.editplaymessage = "Failed to save play";
      });
    }

    $scope.create = function(play) {
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
          $scope.playform.$setUntouched();;
          setTimeout(jumpToPlayerAnchor, 2000);
        }, function(response){
          $scope.message = "Failed to add play";
        });
      };

    $scope.edit = function(play){

    }

    $scope.delete = function(playid) {
        GameService.deletePlay(playid).then(function(response){
          _.remove($scope.plays, function(play) { return play.id === playid; });
          calculateScore();
        }, function(response){
        });
    };


    // YouTube player logic
    $scope.specifiedTime = null;
    $scope.player = null;

    $scope.$on('youtube.player.ready', function($event, player) {
      $scope.player = player;
    })
    $scope.$on('youtube.player.playing', function ($event, player) {
      // If specifiedTime, convert to seconds and seek the player to it.
      if ($scope.specifiedTime) {
        let split_time = $scope.specifiedTime.split(':');
        let seconds = parseInt(split_time[0]) * 3600;
        seconds += parseInt(split_time[1]) * 60;
        seconds += parseInt(split_time[2]);
        player.seekTo(seconds);
        jumpToPlayerAnchor();
        player.playVideo();
        $scope.specifiedTime = null;
      }
    });

    var jumpToPlayerAnchor = function(){
      window.location = String(window.location).replace(/\#.*$/, "") + "#playeranchor";
    }

    $scope.grabTime = function(offset=null) {
      var formattedTime, seconds
      if (offset) {
        seconds = $scope.player.getCurrentTime() - offset
      }
      else{
        seconds = $scope.player.getCurrentTime()
      }

      var hours = '' + Math.floor(seconds / 3600)
      if (hours.length < 2){
        hours = '0' + hours;
      }
      var minutes = '' + Math.floor(seconds / 60)
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

});
