'use strict';

angular.module('saturdayBall').factory('routeResolver', routeResolver);

routeResolver.$inject = ['Session', '$route', '$q'];

function routeResolver(Session, $route, $q) {

  return function() {

    if (!Session.available()) {
      Session.init();
    }

    var deferred = $q.defer();
    deferred.resolve(Session);
    return deferred.promise;
  };
};
