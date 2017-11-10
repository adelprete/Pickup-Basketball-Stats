'use strict';

angular.module('saturdayBall').factory('Per100Service', Per100Service);

Per100Service.$inject = ['$q', '$http']

function Per100Service($q, $http) {

  var simple_statistics = [
    'dreb',
    'oreb',
    'total_rebounds',
    'asts',
    'pot_ast',
    'stls',
    'to',
    'points',
    'blk',
    'ast_fga',
    'ast_fgm',
  ]

  var advanced_statistics = [
    'dreb_percent',
    'oreb_percent',
    'treb_percent',
    'off_rating',
    'def_rating',
    'fgm_percent',
    'threepm_percent',
    'ts_percent',
    'tp_percent',
    'ast_fgm_percent',
    'ast_fga_percent',
    'unast_fgm_percent',
    'unast_fga_percent',
    'pgm_percent',
    'pga_percent'
  ]

  var service = {
    calculatePer100Statlines: calculatePer100Statlines,
    calculateSimplePer100: calculateSimplePer100
  };

  return service;

  /////////////////

  function calculatePer100Statlines(statlines) {
    var per100statlines = []

    for (var i = 0; i < statlines.length; i++) {
      var statline = statlines[i];
      var per100statline = {
        player: statline.player,
        gp: statline.gp,
        off_pos: statline.off_pos,
        fga: statline.fga,
        threepa: statline.threepa
      };

      for (var j = 0; j < simple_statistics.length; j++) {
        per100statline[simple_statistics[j]] = calculateSimplePer100(statline, simple_statistics[j]);
      }

      for (var j = 0; j < advanced_statistics.length; j++) {
        per100statline[advanced_statistics[j]] = calculateAdvancedPer100(statline, advanced_statistics[j]);
      }

      per100statlines.push(per100statline);
    }

    return per100statlines;
  };

  function calculateSimplePer100(statline, stat) {
      var result = (statline[stat] / statline.off_pos) * 100;
      return isNaN(result) ? 0 : result;
  };

  function calculateAdvancedPer100(statline, stat) {
    var result = NaN;

    switch(stat) {
      case 'dreb_percent':
        result = (statline['dreb'] / statline['dreb_opp']) * 100;
        break;
      case 'oreb_percent':
        result = (statline['oreb'] / statline['oreb_opp']) * 100;
        break;
      case 'treb_percent':
        result = (statline['total_rebounds'] /
                (statline['oreb_opp'] + statline['dreb_opp']))
                * 100;
        break;
      case 'off_rating':
        result = statline['off_team_pts'] / statline['off_pos'] * 100
        break;
      case 'def_rating':
        result = statline['def_team_pts'] / statline['def_pos'] * 100;
        break;
      case 'fgm_percent':
        result = statline['fgm'] / statline['fga'] * 100;
        break;
      case 'threepm_percent':
        result = statline['threepm'] / statline['threepa'] * 100;
        break;
      case 'ts_percent':
        result = statline['points'] / statline['fga'] * 100;
        break;
      case 'tp_percent':
        result = statline['ast_points'] / (statline['asts'] + statline['pot_ast']) * 100;
        break;
      case 'ast_fgm_percent':
        result = statline['ast_fgm'] / statline['ast_fga'] * 100
        break;
      case 'ast_fga_percent':
        result = statline['ast_fga'] / statline['fga'] * 100
        break;
      case 'unast_fgm_percent':
        result = (statline['unast_fgm'] - statline['pgm']) / (statline['unast_fga'] - statline['pga']) * 100
        break;
      case 'unast_fga_percent':
        result = (statline['unast_fga'] - statline['pga']) / statline['fga'] * 100
        break;
      case 'pgm_percent':
        result = statline['pgm'] / statline['pga'] * 100
        break;
      case 'pga_percent':
        result = statline['pga'] / statline['fga'] * 100
        break;
    }

    return isNaN(result) ? 0 : result;
  }

};
