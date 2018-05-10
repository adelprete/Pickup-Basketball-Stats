'use strict';

angular.module('saturdayBall').controller('PlayerController', PlayerController);

PlayerController.$inject = ['$scope', '$routeParams', 'PlayerService', 'StatlineService',
  '$anchorScroll', '$window', 'Per100Service', 'GroupService'];

function PlayerController($scope, $routeParams, PlayerService, StatlineService,
  $anchorScroll, $window, Per100Service, GroupService) {

    $scope.adv_per100_statlines = {};
    $scope.adv_per100_overall = {};
    $scope.adv_totals_statlines = {};
    $scope.adv_totals_overall = {};
    $scope.averages_statlines = {};
    $scope.averages_overall = {};
    $scope.game_types = [];
    $scope.getSeasonGames = getSeasonGames;
    $scope.group_id = $routeParams.groupId;
    $scope.per100_statlines = {};
    $scope.per100_overall = {};
    $scope.player = {};
    $scope.seasons = [];
    $scope.selected_season = {};
    $scope.total_game_counts = {};
    $scope.totals_statlines = {};
    $scope.totals_overall = {};

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
            $scope.game_types.push(game_type);

            // while we're here, count the player's total games for each game_type
            var total_games = 0;
            for (var statline in $scope.averages_statlines[game_type]) {
              total_games += $scope.averages_statlines[game_type][statline]['gp'];
            }
            $scope.total_game_counts[game_type] = total_games;
          }
        }

        $scope.game_types.reverse();

      }, function(response){
        console.log("Error: ", response);
      })

      PlayerService.getPlayerTotals($routeParams.playerId).then(function(response){
        $scope.totals_statlines = response.totals;
        $scope.totals_overall = response.overall;
      }, function(response){
        console.log("Error: ", response)
      })

      PlayerService.getPlayerAdvTotals($routeParams.playerId).then(function(response){
        $scope.adv_totals_statlines = response.totals;
        $scope.adv_totals_overall = response.overall;
      }, function(response){
        console.log("Error: ", response)
      })

      PlayerService.getPlayerPer100($routeParams.playerId).then(function(response){
        $scope.per100_statlines = response.per100;
        $scope.per100_overall = response.overall;
      }, function(response){
        console.log("Error: ", response)
      })

      PlayerService.getPlayerAdvPer100($routeParams.playerId).then(function(response){
        $scope.adv_per100_statlines = response.per100;
        $scope.adv_per100_overall = response.overall;
      }, function(response){
        console.log("Error: ", response);
      })

      initGameLog();
    }

    function initGameLog() {
      GroupService.getGroupSeasons($routeParams.groupId).then(function(response){
        $scope.seasons = response.seasons;
        $scope.selected_season.id = $scope.seasons[0].id;
        getSeasonGames();
      }, function(response){
        console.log("Error: ", response)
      })
    }

    function getSeasonGames() {

      var season = $scope.seasons.find(function(s){
        return s.id === $scope.selected_season.id;
      })
      var params = {
        'start_date': season.start_date,
        'end_date': season.end_date,
        'player_id': $routeParams.playerId,
      }
      StatlineService.getStatlines(params).then(function(response){
        $scope.game_statlines = _.chain(response)
                            .orderBy(['game.date', 'game.title'], ['asc', 'asc'])
                            .groupBy(function(s) {
                              return s.game.game_type
                            })
                            .value()
      }, function(response){
        console.log("Error: ", response);
      })
    }

    function calculateSnapshotStats() {
      var total_statline = StatlineService.sumStatlines($scope.season_total_statlines);
      $scope.snapshot_per100_statline = Per100Service.calculatePer100Statlines([total_statline]);
    }
}
