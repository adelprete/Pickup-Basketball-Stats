'use strict';

angular.module('saturdayBall').factory('GroupService', function($q, $http){
  return {
    getGroup: function(groupid){
      var deferred = $q.defer();
      $http.get(`/api/groups/${groupid}/`).then(function(response, status, config, headers){
        deferred.resolve(response.data);
      }, function(response){
        deferred.reject(response);
      });
      return deferred.promise;
    },
    updateGroup: function(data){
      var deferred = $q.defer();
      $http.put(`/api/groups/${data.id}/`, data).then(function(response, status, config, headers){
        deferred.resolve(response.data);
      }, function(response){
        deferred.reject(response);
      });
      return deferred.promise;
    },
  };
});
