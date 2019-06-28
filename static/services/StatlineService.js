'use strict';

angular.module('saturdayBall').factory('StatlineService', StatlineService);

function StatlineService($q, $http) {

  var service = {
    getDailyStatlines: getDailyStatlines,
    getSeasonStatlines: getSeasonStatlines,
    sumStatlines: sumStatlines,
    getStatlines: getStatlines
  };
  return service;

  /////////////////

  function sumStatlines(statlines, id) {
    var stats = ['gp', 'dreb', 'oreb', 'total_rebounds', 'asts', 'pot_ast', 'stls',
    'to', 'points', 'blk', 'ast_fga', 'ast_fgm', 'off_pos', 'def_pos', 'dreb_opp', 'oreb_opp',
    'off_team_pts', 'def_team_pts', 'fgm', 'fga', 'threepm', 'threepa', 'ast_points', 'ba',
    'fd', 'pf', 'unast_fgm', 'unast_fga', 'pgm', 'pga', 'fastbreak_points', 'second_chance_points'];
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

  function getDailyStatlines(query) {
    var deferred = $q.defer();
    $http.get('/api/daily-statlines/' + query).then(function(response){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  };

  function getSeasonStatlines(query) {
    if (!query) {
      query = "";
    }
    var deferred = $q.defer();
    $http.get('/api/season-statlines/' + query).then(function(response){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  };

  function getStatlines(params) {
    var deferred = $q.defer();
    $http.get('/api/statlines/', {params: params}).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  };

};
