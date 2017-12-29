angular.module('saturdayBall')

.factory('routeResolver', routeResolver);

routeResolver.$inject = ['Session', '$route', '$q', '$location', 'GroupService'];

function routeResolver(Session, $route, $q, $location, GroupService) {

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
          }, function(response) {

          })
        }
        deferred.resolve(response);
      });
    } else {
      deferred.resolve(Session);
    }
  }

  function redirectTo(path, deferred, session) {
        window.location.replace(path);
        $location.path(path).search(params);
        $location.replace();
        deferred.resolve(session);
    };

  return function() {
    var deferred = $q.defer();
    initSession(deferred);
    return deferred.promise;
  };
};
