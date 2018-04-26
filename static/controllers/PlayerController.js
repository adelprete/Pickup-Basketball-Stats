'use strict';

angular.module('saturdayBall').controller('PlayerController', PlayerController);

PlayerController.$inject = ['$scope', '$routeParams', 'PlayerService', 'StatlineService',
  '$anchorScroll', '$window', 'Per100Service'];

function PlayerController($scope, $routeParams, PlayerService, StatlineService,
  $anchorScroll, $window, Per100Service) {

    $scope.player = {};

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
        console.log("Error: ", response)
      })
    }

    function calculateSnapshotStats() {
      var total_statline = StatlineService.sumStatlines($scope.season_total_statlines);
      $scope.snapshot_per100_statline = Per100Service.calculatePer100Statlines([total_statline]);
      console.log('snapshot_per100_statline: ', $scope.snapshot_per100_statline);
    }
}
