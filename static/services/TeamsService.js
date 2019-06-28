'use strict';

angular.module('saturdayBall').factory('TeamService', TeamService);

TeamService.$inject = ['$q', '$http', '$routeParams'];

function TeamService($q, $http, $routeParams) {
  var apiurl;
  var myData;
  var service = {
    getTeam: getTeam,
    getTeams: getTeams,
  };
  return service;

  /////////////////

  function getTeam(teamId) {
    var deferred = $q.defer();
    $http.get('/api/teams/' + teamId + '/').then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }

  function getTeams(params) {
    var deferred = $q.defer();
    $http.get('/api/teams/', {"params": params}).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }
};
