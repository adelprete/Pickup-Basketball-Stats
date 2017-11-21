'use strict';

angular.module('saturdayBall').factory('UserService', UserService);

UserService.$inject = ['$q', '$http'];

function UserService($q, $http) {
  var service = {
    createUser: createUser,
    currentUser: currentUser
  };
  return service;

  /////////////////////

  function createUser(data) {
    var deferred = $q.defer();
    $http.post('/api/user/create', data).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }

  function currentUser() {
    var deferred = $q.defer();
    $http.get('/api/user/current').then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }
};
