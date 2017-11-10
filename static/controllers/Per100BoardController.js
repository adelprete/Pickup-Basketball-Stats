'use strict';

angular.module('saturdayBall').controller('Per100BoardController', Per100BoardController);

Per100BoardController.$inject = ['$scope', '$controller', 'StatlineService', 'PlayerService'];

function Per100BoardController($scope, $controller, StatlineService, PlayerService) {

    $scope.arrowDown = arrowDown;
    $scope.arrowUp = arrowUp;
    $scope.decimals = 1;
    $scope.descending = true;
    $scope.loading = true;
    $scope.sort = sort;
    $scope.statSorted = "";
    $scope.tableStatlines = [];
    $scope.title = "Per 100";

    $scope.headers = [
      ['player.first_name', 'Name'],
      ['gp', 'GP'],
      ['points', 'PTS'],
      ['fgm_percent', 'FGM%'],
      ['threepm_percent', '3PM%'],
      ['asts', 'AST'],
      ['pot_ast', 'P.AST'],
      ['dreb', 'DREB'],
      ['oreb', 'OREB'],
      ['dreb_percent', 'DREB%'],
      ['oreb_percent', 'OREB%'],
      ['total_rebounds', 'REB'],
      ['treb_percent', 'REB%'],
      ['stls', 'STL'],
      ['to', 'TO'],
      ['blk', 'BLK'],
      ['off_rating', 'OFF.RATING'],
      ['def_rating', 'DEF.RATING']
    ]

    ////////////////////

    function sort(stat) {
      $scope.descending = (stat === $scope.statSorted) ? !$scope.descending : true
      $scope.statSorted = stat;
      var sortDirection = $scope.descending ? 'desc' : 'asc';
      $scope.tableStatlines = _.orderBy($scope.tableStatlines, [stat], [sortDirection])
    }

    function arrowUp(stat) {
      return ($scope.statSorted === stat && $scope.descending);
    }

    function arrowDown(stat) {
      return ($scope.statSorted === stat && !$scope.descending);
    }

    $scope.$watch('per100Statlines', function() {
      $scope.tableStatlines = $scope.per100Statlines;
      $scope.loading = false;
    });

    $scope.$watch('filterForm', function() {
      $scope.tableStatlines = [];
      $scope.statSorted = "";
      $scope.loading = true;
    }, true);

};
