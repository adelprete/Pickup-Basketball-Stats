'use strict';

angular.module('saturdayBall').controller('AdvTotalsBoardController', AdvTotalsBoardController);

AdvTotalsBoardController.$inject = ['$scope', '$controller', 'StatlineService', 'PlayerService'];

function AdvTotalsBoardController($scope, $controller, StatlineService, PlayerService) {
    $scope.arrowDown = arrowDown;
    $scope.arrowUp = arrowUp;
    $scope.decimals = 1;
    $scope.descending = true;
    $scope.loading = true;
    $scope.sort = sort;
    $scope.statSorted = "";
    $scope.tableStatlines = [];
    $scope.title = "Advanced Totals";

    $scope.headers = [
      ['player.first_name', 'Name'],
      ['gp', 'GP'],
      ['ast_fgm', 'AST.FGM'],
      ['ast_fga', 'AST.FGA'],
      ['unast_fgm', 'UNAST.FGM'],
      ['unast_fga', 'UNAST.FGA'],
      ['ast_points', 'AST.PTS'],
      ['pgm', 'PGM'],
      ['pga', 'PGA'],
      ['fastbreak_points', 'FB.PTS'],
      ['second_chance_points', 'SC.PTS'],
      ['def_pos', 'DEF.POS'],
      ['off_pos', 'OFF.POS'],
      ['dreb_opp', 'DREB.OPP'],
      ['oreb_opp', 'OREB.OPP']
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

    $scope.$watch('statlines', function() {
      $scope.tableStatlines = $scope.statlines;
      $scope.loading = false;
    });

    $scope.$watch('filterForm', function() {
      $scope.loading = true;
      $scope.tableStatlines = [];
      $scope.statSorted = "";
    }, true);


};
