'use strict';

angular.module('saturdayBall', [
  'ngRoute',
  'ngAnimate',
  'ui.bootstrap',
  'youtube-embed'
]);
;'use strict';

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
;'use strict';

angular.module('saturdayBall').run(['$rootScope', 'Session', function ($rootScope, Session) {
    $rootScope.session = Session;
}]);
;'use strict';

angular.module('saturdayBall').config(['$locationProvider', '$routeProvider', function($locationProvider, $routeProvider) {
  var routeResolver = {
    preLoad: function (routeResolver){
      return routeResolver()
    }
  };
    $routeProvider
      .when("/group/:groupId/games/", {
        templateUrl: "static/views/games.html",
        controller: 'GamesController',
        resolve: routeResolver,
        activetab: 'games'
      })
      .when("/group/:groupId/games/:gameid/add-plays/", {
        templateUrl: "static/views/add_plays.html",
        controller: 'AddPlaysController',
        resolve: routeResolver,
        activetab: 'games'
      })
      .when("/group/:groupId/settings", {
        templateUrl: 'static/views/settings.html',
        controller: 'GroupSettingsController',
        resolve: routeResolver,
        activetab: 'settings'
      })
      .when("/group/create/", {
        templateUrl: 'static/views/creategroup.html',
        controller: 'CreateGroupController',
        resolve: routeResolver
      })
      .when("/register", {
        templateUrl: 'static/views/register.html',
        controller: 'RegisterController',
        resolve: routeResolver
      })
      .when("/group/:groupId/leaderboard/", {
        templateUrl: 'static/views/leaderboard.html',
        controller: 'LeaderboardController',
        resolve: routeResolver,
        activetab: 'leaderboard'
      })
      .otherwise({
        resolve: {
          factory: checkRouting
        }
      });

    $locationProvider.html5Mode(true);
}]);

angular.module('saturdayBall').config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

var checkRouting= function ($q, $rootScope, $location) {
  var path = $location.path();
  window.location = $location.host()+ ':8000' + path;
}
;angular.module('saturdayBall')

.factory('routeResolver', routeResolver);

routeResolver.$inject = ['Session', '$route', '$q'];

function routeResolver(Session, $route, $q) {

  function initSession(deferred) {
    if (!Session.available()) {
      Session.init().then(function(response){
        deferred.resolve(response);
      });
    } else {
      deferred.resolve(Session);
    }
  }

  return function() {
    var deferred = $q.defer();
    initSession(deferred);
    return deferred.promise;
  };
};
;'use strict';

angular
    .module('saturdayBall')
    .directive('gameSnippet', gameSnippet);

function gameSnippet() {
    var directive = {
        link: link,
        scope: {
          groupId: '@',
          game: '='
        },
        templateUrl: 'static/partials/directives/gameSnippet.html',
        restrict: 'EA'
    };
    return directive;

    function link(scope, element, attrs) {
    }
  }
;'use strict';

angular.module('saturdayBall').directive('ngConfirmClick', [
    function() {
        return {
            link: function (scope, element, attr) {
                var msg = attr.ngConfirmClick || "Are you sure?";
                var clickAction = attr.confirmedClick;
                element.bind('click', function (event) {
                    if (window.confirm(msg)) {
                        scope.$eval(clickAction)
                    }
                });
            }
        };
}])
;'use strict';

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
;'use strict';

angular.module('saturdayBall').factory('GameService', GameService);

function GameService($q, $http) {
  var apiurl;
  var myData;
  var service = {
    getGamePlays: getGamePlays,
    getGame: getGame,
    getGames: getGames,
    calculateStatlines: calculateStatlines,
    createPlay: createPlay,
    updatePlay: updatePlay,
    getPlay: getPlay,
    deletePlay: deletePlay
  };
  return service;

  /////////////////

  function getGamePlays(gameid) {
    var deferred = $q.defer();
    $http.get('/api/plays/?gameid=' + gameid).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }

  function getGame(gameid) {
    var deferred = $q.defer();
    $http.get('/api/games/gameid/' + gameid + '/').then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }

  function getGames(groupId, params) {
    var deferred = $q.defer();
    $http.get('/api/games/groupid/' + groupId, {params: params}).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }

  function calculateStatlines(gameid) {
    var deferred = $q.defer();
    $http.get('/api/games/' + gameid + '/calculate-statlines').then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }

  function createPlay(data){
    var deferred = $q.defer();
    $http.post('/api/plays/', data).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }

  function updatePlay(play) {
    var deferred = $q.defer();
    $http.post('/api/plays/' + play.id + '/', play).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }

  function getPlay(playid) {
    var deferred = $q.defer();
    $http.get('/api/plays/' + playid + '/').then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }

  function deletePlay(playid) {
    var deferred = $q.defer();
    $http.delete('/api/plays/' + playid + '/').then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }
};
;'use strict';

angular.module('saturdayBall').factory('GroupService', GroupService);

GroupService.$inject = ['$q', '$http'];

function GroupService($q, $http){
  var service = {
      getGroup: getGroup,
      getGroupSeasons: getGroupSeasons,
      updateGroup: updateGroup,
      createGroup: createGroup,
      isGroupAdmin: isGroupAdmin
  };
  return service;

  ////////////////////

  function getGroup(groupid) {
    var deferred = $q.defer();
    $http.get('/api/groups/' + groupid + '/').then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });
    return deferred.promise;
  }

  function updateGroup(data) {
    var deferred = $q.defer();
    $http.put('/api/groups/' + data.id + '/', data).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });
    return deferred.promise;
  }

  function createGroup(data) {
    var deferred = $q.defer();
    $http.post('/api/groups/', data).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });
    return deferred.promise;
  }

  function isGroupAdmin(groupid) {
    var deferred = $q.defer();
    $http.get('/api/groups/' + groupid + '/verify-group-admin/').then(function(response, status, config, headers){
      deferred.resolve(response.data.message);
    }, function(response){
      deferred.reject(response);
    });
    return deferred.promise;
  }

  function getGroupSeasons(groupId) {
    var deferred = $q.defer();
    $http.get('/api/group/' + groupId + '/seasons/').then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });
    return deferred.promise;
  }
};
;'use strict';

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
;'use strict';

angular.module('saturdayBall').factory('PlayerService', PlayerService);

function PlayerService($q, $http) {

  var service = {
    getPlayers: getPlayers,
  };
  return service;

  /////////////////

  function getPlayers(groupId) {
    var deferred = $q.defer();
    $http.get('/api/players/' + groupId).then(function(response){
      deferred.resolve(response.data);
    }, function(response) {
      deferred.reject(response);
    });

    return deferred.promise;
  };

};
;'use strict';

angular.module('saturdayBall').factory('Session', Session);

Session.$inject = ['$q', '$http', 'UserService', 'GroupService']

function Session($q, $http, UserService, GroupService) {
  var user;
  var currentGroup;
  var service = {
      init: init,
      available: available,
      currentUser: function() {
        return user
      },
      currentGroup: function() {
        return currentGroup
      }
    }
  return service;

  ////////////////////

  function init() {
    var deferred = $q.defer();
    getCurrentUser().then(function(result){
      user = result;
      getCurrentGroup().then(function(group){
        currentGroup = group;
        deferred.resolve(user);
      });
    }, function(error){
      console.log(error);
      deferred.reject(error);
    });

    return deferred.promise;
  }

  function getCurrentUser() {
    var deferred = $q.defer();
    UserService.currentUser().then(function(response){
      user = response;
      deferred.resolve(user);
    }, function(response){
      deferred.reject(response.data);
    });

    return deferred.promise;
  }

  function getCurrentGroup() {
    var deferred = $q.defer();
    deferred.resolve({'test': 'TODO later'});
    return deferred.promise;
  }

  function available() {
    return !!user && !!currentGroup;
  }

};
;'use strict';

angular.module('saturdayBall').factory('StatlineService', StatlineService);

function StatlineService($q, $http) {

  var service = {
    getDailyStatlines: getDailyStatlines,
    getSeasonStatlines: getSeasonStatlines
  };
  return service;

  /////////////////

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

};
;'use strict';

angular.module('saturdayBall').factory('UserService', UserService);

UserService.$inject = ['$q', '$http'];

function UserService($q, $http) {
  var service = {
    createUser: createUser,
    currentUser: currentUser
  };
  return service;

  /////////////////////

  function createUser(data) {
    var deferred = $q.defer();
    $http.post('/api/user/create', data).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }

  function currentUser() {
    var deferred = $q.defer();
    $http.get('/api/user/current').then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }
};
;'use strict';

angular.module('saturdayBall').controller('AddPlaysController', AddPlaysController);

AddPlaysController.$inject = ['$scope', '$routeParams', 'GameService', 'Session', 'playOptions'];

function AddPlaysController($scope, $routeParams, GameService, Session, playOptions) {

    $scope.createPlay = createPlay;
    $scope.deletePlay = deletePlay;
    $scope.editplay = {};
    $scope.fillEditForm = fillEditForm;
    $scope.game = {};
    $scope.play = {};
    $scope.playOptions = playOptions;
    $scope.team1_score = 0;
    $scope.team2_score = 0;
    $scope.updatePlay = updatePlay;
    $scope.user = Session.currentUser();

    ///////////////////////

    init();

    function init() {

      GameService.getGame($routeParams['gameid']).then(function (response){
        $scope.game = response;
        var player_objs = $scope.game.team1.concat($scope.game.team2);
        angular.forEach(player_objs, function(value, key) {
          this.push({'code':value.id, 'name': value.first_name + ' ' + value.last_name});
        }, $scope.playOptions.PLAYERS);
        getPlays();
      });

    }

    function getPlays(){
      GameService.getGamePlays($routeParams['gameid']).then(function (response){
        $scope.plays = _.reverse(_.sortBy(response, 'time'));
        calculateScore();
      }, function(response){
      });
    }

    function fillEditForm(playid) {
      GameService.getPlay(playid).then(function (response){
        $scope.editplaymessage = "";
        $scope.editplay = response;
        $scope.editplay.primary_player = response.primary_player.id;
        $scope.editplay.secondary_player = (response.secondary_player && response.secondary_player.id) ? response.secondary_player.id : '';
        $scope.editplay.assist_player = (response.assist_player && response.assist_player.id)? response.assist_player.id : '';
        $scope.editplay.top_play_players = response.top_play_players;
      });
    }

    function calculateScore() {
      $scope.team1_score = 0;
      $scope.team2_score = 0;
      var scoring_plays = ['fgm', 'threepm'];
      var score_type = $scope.game.score_type;
      var score_to_add;
      _.forEach($scope.plays, function(play){
        if (scoring_plays.includes(play.primary_play)) {
          if (score_type === '2and3'){
            score_to_add = (play.primary_play == 'fgm') ? 2 : 3;
          }
          else {
            score_to_add = (play.primary_play == 'fgm') ? 1 : 2;
          }
          if (_.find($scope.game.team1, function(player) {return play.primary_player.id === player.id;})) {
            $scope.team1_score += score_to_add;
          } else {
            $scope.team2_score += score_to_add;
          }
        }
      });
    }

    function updatePlay(play) {
      if (play.secondary_player && !play.secondary_play){
        play.secondary_player = "";
        play.secondary_play = "";
      }
      if (play.assist_player && !play.assist){
        play.assist_player = '';
        play.assist = "";
      }
      if (play.hasOwnProperty('top_play_rank') && !play.top_play_rank){
        play.top_play_rank = "";
      }

      $scope.editplaymessage = "Saving Play...."
      GameService.updatePlay(play).then(function(response){
        $scope.editplaymessage = "Successfully saved";
        getPlays();
        calculateScore();
        GameService.calculateStatlines($scope.game.id).then(function(response){});
      }, function(response){
        console.log(response);
        $scope.editplaymessage = "Failed to save play";
      });
    }

    function createPlay(play) {
        play.game = $scope.game.id
        if (play.secondary_player && !play.secondary_play){
          delete play.secondary_player;
        }
        if (play.assist_player && !play.assist){
          delete play.assist_player;
        }
        if (play.secondary_play == null){
          delete play.secondary_play;
          delete play.secondary_player;
        }
        if (play.assist == null){
          delete play.assist;
          delete play.assist_player;
        }
        $scope.message = "Adding Play...."
        GameService.createPlay(play).then(function(response){
          $scope.message = "Successfully Added";
          $scope.play = {};
          $scope.plays.push(response);
          $scope.plays = _.reverse(_.sortBy($scope.plays, 'time'));
          calculateScore();
          GameService.calculateStatlines($scope.game.id).then(function(response){});
          $scope.playform.$setUntouched();
          //setTimeout(jumpToPlayerAnchor, 2000);
        }, function(response){
          $scope.message = "Failed to add play";
        });
      }

    function deletePlay(playid) {
        GameService.deletePlay(playid).then(function(response){
          _.remove($scope.plays, function(play) { return play.id === playid; });
          calculateScore();
        });
    }


    // YouTube player logic.  Should move to a directive.
    $scope.specifiedTime = null;
    $scope.player = null;

    $scope.$on('youtube.player.ready', function($event, player) {
      $scope.player = player;
    })
    $scope.$on('youtube.player.playing', function ($event, player) {
      // If specifiedTime, convert to seconds and seek the player to it.
      if ($scope.specifiedTime) {
        var split_time = $scope.specifiedTime.split(':');
        var seconds = parseInt(split_time[0]) * 3600;
        seconds += parseInt(split_time[1]) * 60;
        seconds += parseInt(split_time[2]);
        player.seekTo(seconds);
        jumpToPlayerAnchor();
        player.playVideo();
        $scope.specifiedTime = null;
      }
    });

    var jumpToPlayerAnchor = function(){
      window.location = String(window.location).replace(/\#.*$/, "") + "#playeranchor";
    }

    $scope.grabTime = function(offset) {
      var formattedTime, seconds
      if (offset) {
        seconds = $scope.player.getCurrentTime() - offset
      }
      else{
        seconds = $scope.player.getCurrentTime()
      }

      var hours = '' + Math.floor(seconds / 3600)
      if (hours.length < 2){
        hours = '0' + hours;
      }
      var minutes = '' + Math.floor(seconds / 60) % 60
      if (minutes.length < 2){
        minutes = '0' + minutes;
      }
      seconds = '' + Math.floor(seconds % 60)
      if (seconds.length < 2){
        seconds = '0' + seconds;
      }
      formattedTime = hours + ':' + minutes + ":" + seconds
      $scope.play.time = formattedTime;
    }

    $scope.clearRanks = function() {
      $scope.editplay['top_play_rank'] = "";
      $scope.editplay['description'] = "";
      $scope.editplay['top_play_players'] = [];
    }

};
;'use strict';

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
;'use strict';

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
;angular.module('saturdayBall')

.controller('CreateGroupController', CreateGroupController);

CreateGroupController.$inject = ['$scope', '$location', 'GroupService', 'Session', 'settingOptions']

function CreateGroupController($scope, $location, GroupService, Session, settingOptions) {

    $scope.message = "";
    $scope.save = save;
    $scope.settingOptions = settingOptions;
    $scope.settings = {
      score_type: $scope.settingOptions.SCORE_TYPES[0].code,
      game_type: $scope.settingOptions.GAME_TYPES[0].code,
      points_to_win: $scope.settingOptions.POINTS_TO_WIN[0].code,
      possessions_min: 100,
      fga_min: 15
    };
    $scope.user = {};

    ////////////////////

    init();

    function init() {
      $scope.user = Session.currentUser();
    }

    function save() {
      $scope.message = "Saving..."
      GroupService.createGroup($scope.settings).then(function(response) {
        $scope.message = "Saved Successfully";
        var path = $location.path('/group/' + response.id);
        window.location = $location.host() + path;
      }, function(response) {
        $scope.message = "Failed to save"
      });
    }
};
;'use strict';

angular.module('saturdayBall')

.controller('GamesController', GamesController);

GamesController.$inject = ['$scope', '$routeParams', 'GameService']

function GamesController($scope, $routeParams, GameService) {

  $scope.changeFiltering = changeFiltering;
  $scope.games = [];
  $scope.groupId = $routeParams.groupId;
  $scope.filteredDailyGames = [];
  $scope.loadingPage = true;
  $scope.filterMessage = "View Unpublished Games"
  $scope.publishedGames = true;


  $scope.pageChanged = pageChanged;
  $scope.pagination = {
    published: true,
    currentPage: 1,
    numPerPage: 12,
    maxSize: 5
  }

  ///////////////////

  init();

  function init() {
    pageChanged()
  }

  function changeFiltering() {
    if ($scope.pagination.published) {
      $scope.pagination.published = false;
      $scope.pagination.currentPage = 1;
      $scope.filterMessage = "View Published Games"
    }
    else {
      $scope.pagination.published = true;
      $scope.pagination.currentPage = 1;
      $scope.filterMessage = "View Unpublished Games"
    }

    getGamesPage();
  }

  function getGamesPage(published) {
    $scope.loadingPage = true;
    GameService.getGames($routeParams.groupId, $scope.pagination).then(function(results){
      $scope.pagination.currentPage = results.currentPage;
      $scope.pagination.totalItems = results.totalItems;
      $scope.filteredDailyGames = results.items;

      $scope.loadingPage = false;

    }, function(err){
      console.log(err)
    });
  }

  function pageChanged() {

    if ($scope.pagination.currentPage) {
      getGamesPage();
    }
    console.log('Page changed to: ' + $scope.pagination.currentPage);
  };

}
;'use strict';

angular.module('saturdayBall')

.controller('GroupSettingsController', GroupSettingsController);

GroupSettingsController.$inject = ['$scope', '$routeParams', 'GroupService', 'Session', 'settingOptions']

function GroupSettingsController($scope, $routeParams, GroupService, Session, settingOptions) {

    $scope.message = "";
    $scope.save = save;
    $scope.settings = undefined;
    $scope.settingOptions = settingOptions;
    $scope.user = Session.currentUser();

    ///////////////////////

    init();

    function init() {
      console.log('stuff2');
      GroupService.getGroup($routeParams.groupId).then(function(response) {
        $scope.settings = response;
      }, function(response) {
        console.log(response);
      });
    }

    function save() {
      $scope.message = "Saving..."
      GroupService.updateGroup($scope.settings).then(function(response) {
        $scope.message = "Saved Successfully";
      }, function(response){
        $scope.message = "Failed to save"
      });
    }
};
;'use strict';

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
;angular.module('saturdayBall')

.controller('NavigationController', NavigationController);

NavigationController.$inject = ['$scope', '$route', 'Session']

function NavigationController($scope, $route, Session) {

    $scope.user = {};
    $scope.isGroupAdmin = [];
    $scope.$route = $route;

    ////////////////

    $scope.$watch('session.currentUser().username', function () {
        $scope.user = Session.currentUser();
        if ($scope.user) {
          $scope.isGroupAdmin = $scope.user.admin_groups.filter(function(group) { return group[0] == $route.current.params.groupId});
        }
    });

};
;'use strict';

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
;'use strict'

angular.module('saturdayBall')

.controller('RegisterController', RegisterController);

RegisterController.$inject = ['$scope', 'UserService']

function RegisterController($scope, UserService){
    $scope.betacode;
    $scope.message = "";
    $scope.submit = submit;
    $scope.userModel = {};
    $scope.verifypassword;

    //////////////////

    function submit() {
      UserService.createUser($scope.userModel).then(function (response){
        console.log(response);
      }, function(response){
        $scope.message = response.data;
      })
    }
};
;'use strict';

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

//# sourceMappingURL=app.concat.js.map