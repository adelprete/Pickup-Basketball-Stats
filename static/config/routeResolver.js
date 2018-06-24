angular.module('saturdayBall')

.factory('routeResolver', routeResolver);

routeResolver.$inject = ['Session', '$route', '$q', '$location', 'GroupService',
  'RoleHelper'];

function routeResolver(Session, $route, $q, $location, GroupService, RoleHelper) {
  var groupId = $route.current.params.groupId;
  var gameId = $route.current.params.gameid;
  var playerId = $route.current.params.playerId;

  function initSession(deferred) {
    if (!Session.available()) {
      Session.init().then(function(response){
        if (response.username === "" && $route.current.originalPath === '/accept-invite/:inviteCode/') {
          redirectTo('/accounts/login/?next=' + $location.path(), deferred, response);
          return;
        }
        else if (response.username !== "" && $route.current.originalPath === '/accept-invite/:inviteCode/'){
          var data = {
            code: $route.current.params.inviteCode,
            active: false
          }
          GroupService.updateMemberInvite(data).then(function(response) {
            redirectTo('/group/' + response.group + '/', deferred, response)
          }, function(response) {})
        }
        else if ($route.current.originalPath === '/group/:groupId/games/:gameid/add-plays/') {
          if (response.username === '' || !(RoleHelper.isAdmin(response, groupId) ||
                RoleHelper.canEdit(response, groupId))) {
                redirectTo('/group/' + groupId + '/games/' + gameId, deferred, response);
          }
        }
        else if ($route.current.originalPath === '/group/:groupId/players/:playerId/edit') {
          if (response.username === '' || !(RoleHelper.isAdmin(response, groupId) ||
                RoleHelper.canEditPlayer(response, groupId, playerId))) {
                redirectTo('/group/' + groupId + '/players/', deferred, response);
          }
        }
        else if ($route.current.originalPath === '/group/:groupId/settings') {
          if (response.username === '' || !RoleHelper.isAdmin(response, groupId)) {
                redirectTo('/group/' + groupId, deferred, response);
          }
        }
        else if ($route.current.originalPath === '/group/create/') {
          if (response.username === '') {
            redirectTo('/accounts/login/?next=' + $location.path(), deferred, response);
          }
        }
        deferred.resolve(response);
      });
    } else {
      deferred.resolve(Session);
    }
  }

  function redirectTo(path, deferred, session) {
        window.location.replace(path);
        deferred.reject(session);
    };

  return function() {
    var deferred = $q.defer();
    initSession(deferred);
    return deferred.promise;
  };
};
