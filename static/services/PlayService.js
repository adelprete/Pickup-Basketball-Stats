'use strict';

angular.module('saturdayBall').factory('PlayService', PlayService);

function PlayService($q, $http) {

  var service = {
    getPlays: getPlays,
  };
  return service;

  /////////////////

  function getPlays(params) {
    var deferred = $q.defer();
    $http.get('/api/plays/', {params: params}).then(function(response){
      deferred.resolve(response.data);
    }, function(response) {
      deferred.reject(response);
    });

    return deferred.promise;
  };
};
