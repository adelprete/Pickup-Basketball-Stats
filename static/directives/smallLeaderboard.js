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
          stat: '@',
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
      scope.leaderboard = [];

      function updateSmallLeaderboard() {
        scope.calculating = true;
        if (['fgm_percent', 'ts_percent'].indexOf(scope.stat) > -1) {
          scope.leaderboard = _.chain(scope.per100Statlines)
                              .filter(function(statline) {
                                return (statline.off_pos > scope.filterForm.possessions_min &&
                                        statline.fga > scope.filterForm.fga_min &&
                                        ['Team1', 'Team2'].indexOf(statline.player.first_name) <= -1)
                              })
                              .orderBy([scope.stat], ['desc'])
                              .slice(0,5)
                              .value();
        } else if (['threepm_percent'].indexOf(scope.stat) > -1) {
          scope.leaderboard = _.chain(scope.per100Statlines)
                              .filter(function(statline) {
                                return (statline.off_pos > scope.filterForm.possessions_min &&
                                        statline.threepa > scope.filterForm.fga_min &&
                                        ['Team1', 'Team2'].indexOf(statline.player.first_name) <= -1)
                              })
                              .orderBy([scope.stat], ['desc'])
                              .slice(0,5)
                              .value();
        } else {
          var filtered_leaderboard = _.filter(scope.per100Statlines, function(statline) {
                                      return (statline.off_pos > scope.filterForm.possessions_min &&
                                            ['Team1', 'Team2'].indexOf(statline.player.first_name) <= -1)
                                    });
          if(scope.stat === 'def_rating') {
            scope.leaderboard = _.chain(filtered_leaderboard)
                                .orderBy(['def_rating'], ['asc'])
                                .slice(0,5)
                                .value();

          } else {
            scope.leaderboard = _.chain(filtered_leaderboard)
                                .orderBy([scope.stat], ['desc'])
                                .slice(0,5)
                                .value();
          }
        }
        scope.calculating = false;
      };

      scope.$watch('per100Statlines', function() {
        if (scope.per100Statlines) {
          console.log('per100Statlines');
          updateSmallLeaderboard();
        }
      });

      scope.$watch('filterForm', function() {
        scope.leaderboard = [];
        scope.calculating = true;
      }, true);

    }
}
