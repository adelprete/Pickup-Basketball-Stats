'use strict';

angular
    .module('saturdayBall')
    .constant('settingOptions', {
      SCORE_TYPES: [
        {'code': '1and2', 'name': '1\'s and 2\'s'},
        {'code': '2and3', 'name': '2\'s and 3\'s'}
      ],
      GAME_TYPES: [
        {'code': '5v5', 'name': '5 on 5'},
        {'code': '4v4', 'name': '4 on 4'},
        {'code': '3v3', 'name': '3 on 3'},
        {'code': '2v2', 'name': '2 on 2'},
        {'code': '1v1', 'name': '1 on 1'}
      ],
      POINTS_TO_WIN: [
        {'code': '11', 'name': '11'},
        {'code': '30', 'name': '30'},
        {'code': 'other', 'name': 'Other'}
      ]
    })
    .constant('playOptions', {
      PRIMARY_PLAY: [
          {'code': 'fgm', 'name': 'FGM'},
          {'code': 'fga', 'name': 'FGA'},
          {'code': 'threepm', 'name': '3PM'},
          {'code': 'threepa', 'name': '3PA'},
          {'code': 'blk', 'name': 'BLK'},
          {'code': 'to', 'name': 'TO'},
          {'code': 'pf', 'name': 'FOUL'},
          {'code': 'sub_out', 'name': 'SUB OUT'},
          {'code': 'misc', 'name': 'Misc'}
      ],
      SECONDARY_PLAY: [
          {'code': 'dreb', 'name': 'DREB'},
          {'code': 'oreb', 'name': 'OREB'},
          {'code': 'stls', 'name': 'STL'},
          {'code': 'ba', 'name': 'Block Against'},
          {'code': 'fd', 'name': 'Foul Drawn'},
          {'code': 'sub_in', 'name': 'SUB IN'},
      ],
      ASSIST_PLAY: [
          {'code': 'pot_ast', 'name': 'Potential Assist'},
          {'code': 'asts', 'name': 'Assist'}
      ],
      PLAY_RANKS: [
          {'code': 't01', 'name': 'Top 1'},
          {'code': 't02', 'name': 'Top 2'},
          {'code': 't03', 'name': 'Top 3'},
          {'code': 't04', 'name': 'Top 4'},
          {'code': 't05', 'name': 'Top 5'},
          {'code': 't06', 'name': 'Top 6'},
          {'code': 't07', 'name': 'Top 7'},
          {'code': 't08', 'name': 'Top 8'},
          {'code': 't09', 'name': 'Top 9'},
          {'code': 't10', 'name': 'Top 10'},
          {'code': 'nt01', 'name': 'Not Top 1'},
          {'code': 'nt02', 'name': 'Not Top 2'},
          {'code': 'nt03', 'name': 'Not Top 3'},
          {'code': 'nt04', 'name': 'Not Top 4'},
          {'code': 'nt05', 'name': 'Not Top 5'},
          {'code': 'nt06', 'name': 'Not Top 6'},
          {'code': 'nt07', 'name': 'Not Top 7'},
          {'code': 'nt08', 'name': 'Not Top 8'},
          {'code': 'nt09', 'name': 'Not Top 9'},
          {'code': 'nt10', 'name': 'Not Top 10'},
      ],
      PLAYERS: []
    })
    .constant('statDescriptions', {
      'gp': 'Games Played',
      'points': 'Points',
      'fd': 'Fouls Drawn (Whenever you are fouled)',
      'fgm': 'Field Goals Made',
      'fga': 'Field Goals Attempted',
      'threepm': '3 Pointers Made',
      'threepa': '3 Pointers Attempted',
      'fgm_percent': 'Field Goal Percentage.  Percentage of Field Goals Made',
      'threepm_percent': '3 Point Percentage. Percentage of 3 pointers made',
      'asts': 'Assists',
      'pot_ast': 'Potential Assists. A pass that would’ve lead to a score if the receiver made the shot.',
      'dreb': 'Defensive Rebounds',
      'oreb': 'Offensive Rebounds',
      'dreb_percent': 'Percentage of defensive rebounds grabbed against total defensive rebounds available',
      'oreb_percent': 'Percentage of offensive rebounds grabbed against total offensive rebounds available',
      'total_rebounds': 'Total Rebounds',
      'treb_percent': 'Percentage of possessions that result in a rebound',
      'stl': 'Steals (Anytime you cause a turnover from the other team)',
      'to': 'Turnovers',
      'blks': 'Blocks (Whenever you deflect a shot attempt)',
      'ba': "Block Against (Whenver your shot gets blocked)",
      'off_rating': 'Points scored per 100 possessions while you\'re on the floor',
      'def_rating': 'Points scored against your per 100 possessions while you\'re on the floor',
      'ts_percent': 'True Shooting Percentage. Percentage of Field Goals made with the 3 pointers weighed higher.  Formula is Points / FGA',
      'tp_percent': 'True Passing Percentage. Percentage of points made following your assists and potential assists',
      'ast_fgm_percent': 'Assisted Shooting %.  Shooting percentage of shots that were assisted by another player.',
      'ast_fga_percent': 'Assisted Field Goal %. Percentage of shots attempted that were assisted by another player.',
      'unast_fgm_percent': 'Unassisted Shooting %. Shooting percentage of shots that were not assisted by another player.',
      'unast_fga_percent': 'Unassisted Field Goal %. Percentage of shots attempted that were not assisted by another player.',
      'pgm_percent': 'Putback Shooting %.  Percentage of putbacks that go in.',
      'pga_percent': 'Putback Field Goal %.  Percentage of shots that are considered putbacks.',
      'pf': 'Personal Fouls (Amount of fouls that you have been called on)'
    });
