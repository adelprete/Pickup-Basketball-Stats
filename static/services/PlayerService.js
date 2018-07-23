'use strict';

angular.module('saturdayBall').factory('PlayerService', PlayerService);

function PlayerService($q, $http) {

  var service = {
    createPlayer: createPlayer,
    updatePlayer: updatePlayer,
    getPlayer: getPlayer,
    deletePlayer: deletePlayer,
    getPlayers: getPlayers,
    getPlayerAverages: getPlayerAverages,
    getPlayerTotals: getPlayerTotals,
    getPlayerAdvTotals: getPlayerAdvTotals,
    getPlayerPer100: getPlayerPer100,
    getPlayerAdvPer100: getPlayerAdvPer100,
    getAwards: getAwards
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

  function getPlayerTotals(playerId) {
    var deferred = $q.defer();
    $http.get('/api/players/' + playerId + '/overall_totals').then(function(response){
      deferred.resolve(response.data);
    }, function(response) {
      deferred.reject(response);
    });
    return deferred.promise;
  };

  function getPlayerAdvTotals(playerId) {
    var deferred = $q.defer();
    $http.get('/api/players/' + playerId + '/overall_adv_totals').then(function(response){
      deferred.resolve(response.data);
    }, function(response) {
      deferred.reject(response);
    });
    return deferred.promise;
  };

  function getPlayerPer100(playerId) {
    var deferred = $q.defer();
    $http.get('/api/players/' + playerId + '/overall_per100').then(function(response){
      deferred.resolve(response.data);
    }, function(response) {
      deferred.reject(response);
    });
    return deferred.promise;
  };

  function getPlayerAdvPer100(playerId) {
    var deferred = $q.defer();
    $http.get('/api/players/' + playerId + '/overall_adv_per100').then(function(response){
      deferred.resolve(response.data);
    }, function(response) {
      deferred.reject(response);
    });
    return deferred.promise;
  };

  function getAwards(params) {
    var deferred = $q.defer();
    $http.get('/api/awards/', {'params': params}).then(function(response){
      deferred.resolve(response.data);
    }, function(response) {
      deferred.reject(response);
    });
    return deferred.promise;
  };

};
