'use strict';

angular.module('saturdayBall').factory('Session', Session);

Session.$inject = ['$q', '$http', 'UserService', 'GroupService']

function Session($q, $http, UserService, GroupService) {
  var user = {
    username: "",
    group_permissions: []
  };
  var currentGroup;
  var service = {
      init: init,
      available: available,
      currentUser: function() {
        return user
      },
    }
  return service;

  ////////////////////

  function init() {
    var deferred = $q.defer();
    getCurrentUser().then(function(result){
      user = result;
      deferred.resolve(user);
    }, function(error){
      deferred.reject(error);
    });

    return deferred.promise;
  }

  function getCurrentUser() {
    var deferred = $q.defer();
    UserService.currentUser().then(function(response){
      user = response;
      deferred.resolve(user);
    }, function(response){
      deferred.reject(response.data);
    });

    return deferred.promise;
  }

  function available() {
    return user.username !== "";
  }

};
