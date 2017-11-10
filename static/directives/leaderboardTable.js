'use strict';

angular
    .module('saturdayBall')
    .directive('smallLeaderboard', smallLeaderboard);

smallLeaderboard.$inject = ['PlayerService', '$q', 'Per100Service']

function smallLeaderboard(PlayerService, $q, Per100Service) {
    var directive = {
        link: link,
        scope: {
          title: '@',
          statlines: '@',
          color: '@',
          per100Statlines: '=',
          filterForm: '=',
          tooltipDesc: '@'
        },
        templateUrl: 'static/partials/directives/smallLeaderboard.html',
        restrict: 'EA'
    };
    return directive;

    function link(scope, element, attrs) {

      $scope.arrowUp = arrowUp;
      $scope.arrowDown = arrowDown;
      $scope.statSorted = "";
      $scope.sort = sort;
      $scope.descending = true;
      $scope.totalsBoardStatlines = [];

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

      function sort(stat) {
        $scope.descending = (stat === $scope.statSorted) ? !$scope.descending : true
        $scope.statSorted = stat
        var sortDirection = $scope.descending ? 'desc' : 'asc';
        $scope.totalsBoardStatlines = _.orderBy($scope.totalsBoardStatlines, [stat], [sortDirection])
      }

      function arrowUp(stat) {
        return ($scope.statSorted === stat && $scope.descending);
      }

      function arrowDown(stat) {
        return ($scope.statSorted === stat && !$scope.descending);
      }

      $scope.$watch('statlines', function() {
        $scope.totalsBoardStatlines = $scope.statlines;
      });

      $scope.$on('filterFormChanged', function() {
        $scope.totalsBoardStatlines = [];
        $scope.statSorted = "";
      });

    }
}
