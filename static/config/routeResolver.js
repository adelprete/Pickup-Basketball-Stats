'use strict';

angular.module('saturdayBall').factory('routeResolver', routeResolver);

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
