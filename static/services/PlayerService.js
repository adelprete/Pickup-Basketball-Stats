'use strict';

angular.module('saturdayBall').factory('PlayerService', PlayerService);

function PlayerService($q, $http) {

  var service = {
    getPlayers: getPlayers,
  };
  return service;

  /////////////////

  function getPlayers(groupId) {
    var deferred = $q.defer();
    $http.get('/api/players/' + groupId + '/').then(function(response){
      deferred.resolve(response.data);
    }, function(response) {
      deferred.reject(response);
    });

    return deferred.promise;
  };

};
