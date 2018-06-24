'use strict';

angular.module('saturdayBall').factory('GroupService', GroupService);

GroupService.$inject = ['$q', '$http'];

function GroupService($q, $http){
  var service = {
      getGroup: getGroup,
      getGroupSeasons: getGroupSeasons,
      updateGroup: updateGroup,
      createGroup: createGroup,
      isGroupAdmin: isGroupAdmin,
      getMemberPermissions: getMemberPermissions,
      updateMemberPermission: updateMemberPermission,
      deleteMemberPermission: deleteMemberPermission,
      createMemberInvite: createMemberInvite,
      updateMemberInvite: updateMemberInvite

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

  function getMemberPermissions(params) {
    var deferred = $q.defer();
    $http.get('/api/member-permissions/', {params: params}).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }

  function updateMemberPermission(data) {
    var deferred = $q.defer();
    $http.put('/api/member-permissions/' + data.id + '/', data).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });
    return deferred.promise;
  }

  function deleteMemberPermission(data) {
    var deferred = $q.defer();
    $http.delete('/api/member-permissions/' + data.id + '/', data).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });
    return deferred.promise;
  }

  function createMemberInvite(data) {
    var deferred = $q.defer();
    $http.post('/api/member-invite/', data).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });
    return deferred.promise;
  }

  function updateMemberInvite(data) {
    var deferred = $q.defer();
    $http.put('/api/member-invite/' + data.code + '/', data).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });
    return deferred.promise;
  }
};
