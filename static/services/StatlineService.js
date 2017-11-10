'use strict';

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
    $http.get(`/api/daily-statlines/${query}`).then(function(response){
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
    $http.get(`/api/season-statlines/${query}`).then(function(response){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  };

};
