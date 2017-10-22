angular.module('saturdayBall').factory('routeResolver', ['Session', '$route', '$q', function(Session, $route, $q){

  return function() {

    if (!Session.available()) {
      Session.init();
    }

    var deferred = $q.defer();
    deferred.resolve(Session);
    return deferred.promise;
  };
}]);
