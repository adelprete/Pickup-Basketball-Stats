'use strict';

angular.module('saturdayBall').factory('UserService', function($q, $http){
  return {
    createUser: function(data){
      var deferred = $q.defer();
      $http.post(`/api/user/create`, data).then(function(response, status, config, headers){
        deferred.resolve(response.data);
      }, function(response){
        deferred.reject(response);
      });

      return deferred.promise;
    },
  };
});
