'use strict';

angular.module('saturdayBall').controller('TotalsLeaderboardController', TotalsLeaderboardController);

TotalsLeaderboardController.$inject = ['$scope', '$controller', 'StatlineService', 'PlayerService'];

function TotalsLeaderboardController($scope, $controller, StatlineService, PlayerService) {

    $scope.arrowDown = arrowDown;
    $scope.arrowUp = arrowUp;
    $scope.decimals = 1;
    $scope.descending = true;
    $scope.loading = true;
    $scope.sort = sort;
    $scope.statSorted = "";
    $scope.tableStatlines = [];
    $scope.title = "Totals";

    $scope.headers = [
      ['player.first_name', 'Name'],
      ['gp', 'GP'],
      ['fgm', 'FGM'],
      ['fga', 'FGA'],
      ['threepm', '3PM'],
      ['threepa', '3PA'],
      ['oreb', 'OFF'],
      ['dreb', 'DEF'],
      ['total_rebounds', 'REB'],
      ['asts', 'AST'],
      ['pot_ast', 'POT.AST'],
      ['to', 'TO'],
      ['stls', 'STL'],
      ['blk', 'BLK'],
      ['ba', 'BA'],
      ['fd', 'FD'],
      ['pf', 'PF'],
      ['points', 'PTS']
    ];

    /////////////////

    function sort(stat) {
      $scope.descending = (stat === $scope.statSorted) ? !$scope.descending : true
      $scope.statSorted = stat
      var sortDirection = $scope.descending ? 'desc' : 'asc';
      $scope.tableStatlines = _.orderBy($scope.tableStatlines, [stat], [sortDirection])
    }

    function arrowUp(stat) {
      return ($scope.statSorted === stat && $scope.descending);
    }

    function arrowDown(stat) {
      return ($scope.statSorted === stat && !$scope.descending);
    }

    $scope.$watch('statlines', function() {
      $scope.tableStatlines = $scope.statlines;
      $scope.loading = false;
    });

    $scope.$watch('filterForm', function() {
      $scope.tableStatlines = [];
      $scope.statSorted = "";
      $scope.loading = true;
    }, true);


};
