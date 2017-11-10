'use strict';

angular.module('saturdayBall').controller('AdvPer100BoardController', AdvPer100BoardController);

AdvPer100BoardController.$inject = ['$scope', '$controller', 'StatlineService', 'PlayerService'];

function AdvPer100BoardController($scope, $controller, StatlineService, PlayerService) {

    $scope.arrowDown = arrowDown;
    $scope.arrowUp = arrowUp;
    $scope.decimals = 1;
    $scope.descending = true;
    $scope.loading = true;
    $scope.sort = sort;
    $scope.statSorted = "";
    $scope.tableStatlines = [];
    $scope.title = "Advanced Per 100";

    $scope.headers = [
      ['player.first_name', 'Name'],
      ['gp', 'GP'],
      ['ts_percent', 'TS%'],
      ['tp_percent', 'TP%'],
      ['ast_fgm_percent', 'AST.FGM%'],
      ['ast_fga_percent', 'AST.FGA%'],
      ['unast_fgm_percent', 'UNAST.FGM%'],
      ['unast_fga_percent', 'UNAST.FGA%'],
      ['pgm_percent', 'PGM%'],
      ['pga_percent', 'PGA%']
    ]

    /////////////////

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
