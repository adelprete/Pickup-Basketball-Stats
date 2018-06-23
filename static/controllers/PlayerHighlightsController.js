'use strict';

angular.module('saturdayBall').controller('PlayerHighlightsController', PlayerHighlightsController);

PlayerHighlightsController.$inject = ['$scope', '$routeParams', 'PlayService', 'GameService',
  '$anchorScroll', '$window', 'Per100Service', '$timeout'];

function PlayerHighlightsController($scope, $routeParams, PlayService, GameService,
  $anchorScroll, $window, Per100Service, $timeout) {

    $scope.topPlays = [];
    $scope.notTopPlays = [];
    $scope.initYoutubePlayer = initYoutubePlayer;
    $scope.specifiedTime = null;
    $scope.youtube_id = null;
    $scope.youtubePlayer = null;

    ///////////////////////

    init();

    function init() {
      var query = {
        'top_play_players': $routeParams.playerId,
        'top_play_rank__startswith': 't'
      }
      PlayService.getPlays(query).then(function(response){
        $scope.topPlays = response;
        $scope.initYoutubePlayer($scope.topPlays[0].game, $scope.topPlays[0].time, 'paused')
      }, function(response){
        console.log("Error: ", response)
      })

      var query = {
        'top_play_players': $routeParams.playerId,
        'top_play_rank__startswith': 'nt'
      }
      PlayService.getPlays(query).then(function(response){
        $scope.notTopPlays = response;
      }, function(response){
        console.log("Error: ", response)
      })
    }

    function initYoutubePlayer(game_id, timestamp, action) {
        // YouTube player logic

      GameService.getGame(game_id).then(function(response){
        $scope.youtube_id = response.youtube_id;

        $scope.$on('youtube.player.ready', function($event, player) {
          $scope.youtubeplayer = player;
          seekToTime(timestamp);
          if (action == 'play') {
            $anchorScroll("playeranchor");
            $timeout(function() {
              $scope.youtubeplayer.playVideo();
              seekToTime(timestamp);
            }, 1000);
          }
          else {
            $scope.youtubeplayer.pauseVideo();
          }

        })
      }, function(response){
        console.log("Error: ", response);
      })
    }

    function seekToTime(timestamp) {
      var split_time = timestamp.split(':');
      var seconds = parseInt(split_time[0]) * 3600;
      seconds += parseInt(split_time[1]) * 60;
      seconds += parseInt(split_time[2]);
      $scope.youtubeplayer.seekTo(seconds);
    };
}
