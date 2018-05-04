'use strict';

angular.module('saturdayBall').controller('PlayerController', PlayerController);

PlayerController.$inject = ['$scope', '$routeParams', 'PlayerService', 'StatlineService',
  '$anchorScroll', '$window', 'Per100Service'];

function PlayerController($scope, $routeParams, PlayerService, StatlineService,
  $anchorScroll, $window, Per100Service) {

    $scope.averages_statlines = {};
    $scope.averages_overall = {};
    $scope.game_types = [];
    $scope.player = {};
    $scope.total_game_counts = {};

    ///////////////////////

    init();

    function init() {
      PlayerService.getPlayer($routeParams.playerId).then(function(response){
        $scope.player = response;
        var query = '?group_id='+$routeParams.groupId+'&player_id='+$scope.player.id;
        StatlineService.getSeasonStatlines(query).then(function(response){
          $scope.season_total_statlines = response;
          calculateSnapshotStats();
        }, function(response) {
          console.log("StatlineService Error: ", response);
        })
      }, function(response){
        console.log("Error: ", response);
      })

      PlayerService.getPlayerAverages($routeParams.playerId).then(function(response){
        $scope.averages_statlines = response.averages;
        $scope.averages_overall = response.overall;

        // Figure out which game_type buttons should be shown
        for (var game_type in $scope.averages_overall) {
          if (!_.isEmpty($scope.averages_overall[game_type])) {
            $scope.game_types.unshift(game_type);

            // while we're here, count the player's total games for each game_type
            var total_games = 0;
            for (var statline in $scope.averages_statlines[game_type]) {
              total_games += $scope.averages_statlines[game_type][statline]['gp'];
            }
            $scope.total_game_counts[game_type] = total_games;
          }
        }

      }, function(response){
        console.log("Error: ", response);
      })
    }

    function calculateSnapshotStats() {
      var total_statline = StatlineService.sumStatlines($scope.season_total_statlines);
      $scope.snapshot_per100_statline = Per100Service.calculatePer100Statlines([total_statline]);
    }
}
