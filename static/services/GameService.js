'use strict';

angular.module('saturdayBall').factory('GameService', GameService);

function GameService($q, $http) {
  var apiurl;
  var myData;
  var service = {
    getGamePlays: getGamePlays,
    getGame: getGame,
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
    $http.get(`/api/plays/?gameid=${gameid}`).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }

  function getGame(gameid) {
    var deferred = $q.defer();
    $http.get(`/api/games/${gameid}/`).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }

  function calculateStatlines(gameid) {
    var deferred = $q.defer();
    $http.get(`/api/games/${gameid}/calculate-statlines`).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }

  function createPlay(data){
    var deferred = $q.defer();
    $http.post(`/api/plays/`, data).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }

  function updatePlay(play) {
    var deferred = $q.defer();
    $http.post(`/api/plays/${play.id}/`, play).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }

  function getPlay(playid) {
    var deferred = $q.defer();
    $http.get(`/api/plays/${playid}/`).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }

  function deletePlay(playid) {
    var deferred = $q.defer();
    $http.delete(`/api/plays/${playid}/`).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }
};
