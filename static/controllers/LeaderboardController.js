'use strict';

angular.module('saturdayBall').controller('LeaderboardController', LeaderboardController);

LeaderboardController.$inject = ['$scope', '$routeParams', 'GroupService', 'PlayerService',
    'StatlineService', 'Session', 'Per100Service', 'statDescriptions'];

function LeaderboardController($scope, $routeParams, GroupService, PlayerService,
  StatlineService, Session, Per100Service, statDescriptions) {

  $scope.groupId = $routeParams.groupId;
  $scope.filterForm = {};
  $scope.filterOptions = {'seasons': []};
  $scope.isFormVisible = false;
  $scope.ShowHideForm = ShowHideForm;
  $scope.statlines = [];
  $scope.statDescriptions = statDescriptions;
  $scope.per100Statlines = [];

  init();

  ///////////////////////

  function init() {
    GroupService.getGroupSeasons($routeParams.groupId).then(function(response) {
      response.seasons.push({id:0, title: 'All'});
      $scope.filterOptions.seasons = response.seasons;
      $scope.filterForm.season = response.seasons[0].id;
    }, function(response) {
      console.log("Failed: ", response);
    })

    GroupService.getGroup($routeParams.groupId).then(function(response) {
      $scope.group = response;
      $scope.filterForm.possessions_min = $scope.group.possessions_min;
      $scope.filterForm.fga_min = $scope.group.fga_min;
    }, function(response) {
      console.log('Failed: ', response);
    });
  }

  function generateTotalStatlines() {

    var query = "?game_type=5v5";
    query += $scope.filterForm.season === 0 ? "" : '&season=' + $scope.filterForm.season;
    StatlineService.getSeasonStatlines(query).then(function(response) {
      var grouped_lines = _.chain(response)
                          .groupBy(function(s) {
                            return s.player.id
                          })
                          .map(function(statlines, key) {
                            var stat = "dreb"
                            var player = {
                              id: key,
                              player: statlines[0].player
                            };
                            _.assign(player, sumStatline(statlines, key));
                            return player;
                          })
                          .filter(function(statline) {
                            return (['Team1', 'Team2'].indexOf(statline.player.first_name) <= -1)
                          })
                          .orderBy(['player.first_name'], ['asc'])
                          .value()
      $scope.statlines = grouped_lines;
      $scope.per100Statlines = createPer100Statlines();
    });
  }

  function createPer100Statlines() {
    return Per100Service.calculatePer100Statlines($scope.statlines);
  }

  function ShowHideForm() {
      $scope.isFormVisible = $scope.isFormVisible ? false : true;
  }

  function sumStatline(statlines, id) {
    var stats = ['gp', 'dreb', 'oreb', 'total_rebounds', 'asts', 'pot_ast', 'stls',
    'to', 'points', 'blk', 'ast_fga', 'ast_fgm', 'off_pos', 'def_pos', 'dreb_opp', 'oreb_opp',
    'off_team_pts', 'def_team_pts', 'fgm', 'fga', 'threepm', 'threepa', 'ast_points', 'ba',
    'fd', 'pf', 'unast_fgm', 'unast_fga', 'pgm', 'pga', 'fastbreak_points', 'second_chance_points',
    'ast_points'];
    var statline_aggregate = {};
    for (var i = 0; i < statlines.length; i++) {
      var statline = statlines[i];
      for (var j = 0; j < stats.length; j++) {
        var stat = stats[j];
        if (!(stat in statline_aggregate)) {
          statline_aggregate[stat] = 0;
        }
        statline_aggregate[stat] += statline[stat];
      }
    }
    return statline_aggregate;
  }

  function sortTotalsBoard(stat) {
    _.orderBy($scope.totalsBoardStatlines, [stat], ['asc'])
  }


  $scope.$watch('filterForm', function(newVal, oldVal) {
    if(newVal!=oldVal) {
      $scope.season = _.find($scope.filterOptions.seasons, {'id': $scope.filterForm.season});
      if ($scope.season) {
        generateTotalStatlines();
      }
    }
  }, true);


};