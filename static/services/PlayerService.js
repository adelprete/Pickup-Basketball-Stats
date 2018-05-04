'use strict';

angular.module('saturdayBall').factory('PlayerService', PlayerService);

function PlayerService($q, $http) {

  var service = {
    createPlayer: createPlayer,
    updatePlayer: updatePlayer,
    getPlayer: getPlayer,
    deletePlayer: deletePlayer,
    getPlayers: getPlayers,
    getPlayerAverages: getPlayerAverages
  };
  return service;

  /////////////////

  function createPlayer(data) {
    var deferred = $q.defer();
    $http.post('/api/players/', data).then(function(response){
      deferred.resolve(response.data);
    }, function(response) {
      deferred.reject(response);
    });

    return deferred.promise;
  };

  function updatePlayer(data) {
    var deferred = $q.defer();
    $http.put('/api/players/' + data.id + '/', data).then(function(response){
      deferred.resolve(response.data);
    }, function(response) {
      deferred.reject(response);
    });

    return deferred.promise;
  };

  function getPlayer(playerId) {
    var deferred = $q.defer();
    $http.get('/api/players/' + playerId + '/').then(function(response){
      deferred.resolve(response.data);
    }, function(response) {
      deferred.reject(response);
    });

    return deferred.promise;
  };

  function deletePlayer(playerId) {
    var deferred = $q.defer();
    $http.delete('/api/players/' + playerId).then(function(response){
      deferred.resolve(response.data);
    }, function(response) {
      deferred.reject(response);
    });

    return deferred.promise;
  };

  function getPlayers(params) {
    var deferred = $q.defer();
    $http.get('/api/players/', {params: params}).then(function(response){
      deferred.resolve(response.data);
    }, function(response) {
      deferred.reject(response);
    });

    return deferred.promise;
  };

  function getPlayerAverages(playerId) {
    var deferred = $q.defer();
    $http.get('/api/players/' + playerId + '/overall_averages').then(function(response){
      deferred.resolve(response.data);
    }, function(response) {
      deferred.reject(response);
    });

    return deferred.promise;
  };

};
