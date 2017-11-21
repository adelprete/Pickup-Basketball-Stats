'use strict';

angular.module('saturdayBall').factory('GroupService', GroupService);

GroupService.$inject = ['$q', '$http'];

function GroupService($q, $http){
  var service = {
      getGroup: getGroup,
      getGroupSeasons: getGroupSeasons,
      updateGroup: updateGroup,
      createGroup: createGroup,
      isGroupAdmin: isGroupAdmin
  };
  return service;

  ////////////////////

  function getGroup(groupid) {
    var deferred = $q.defer();
    $http.get('/api/groups/' + groupid + '/').then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });
    return deferred.promise;
  }

  function updateGroup(data) {
    var deferred = $q.defer();
    $http.put('/api/groups/' + data.id + '/', data).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });
    return deferred.promise;
  }

  function createGroup(data) {
    var deferred = $q.defer();
    $http.post('/api/groups/', data).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });
    return deferred.promise;
  }

  function isGroupAdmin(groupid) {
    var deferred = $q.defer();
    $http.get('/api/groups/' + groupid + '/verify-group-admin/').then(function(response, status, config, headers){
      deferred.resolve(response.data.message);
    }, function(response){
      deferred.reject(response);
    });
    return deferred.promise;
  }

  function getGroupSeasons(groupId) {
    var deferred = $q.defer();
    $http.get('/api/group/' + groupId + '/seasons/').then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });
    return deferred.promise;
  }
};
