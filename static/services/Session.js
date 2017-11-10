'use strict';

angular.module('saturdayBall').factory('Session', Session);

Session.$inject = ['$q', '$http', 'UserService', 'GroupService']

function Session($q, $http, UserService, GroupService) {
  var user;
  var currentGroup;
  var service = {
      init: init,
      available: available,
      currentUser: function() {
        return user
      },
      currentGroup: function() {
        return currentGroup
      }
    }
  return service;

  ////////////////////

  function init() {
    var deferred = $q.defer();
    getCurrentUser().then(function(result){
      user = result;
      getCurrentGroup().then(function(group){
        currentGroup = group;
        deferred.resolve(user);
      });
    }, function(error){
      console.log(error);
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

  function getCurrentGroup() {
    var deferred = $q.defer();
    deferred.resolve({'test': 'TODO later'});
    return deferred.promise;
  }

  function available() {
    return !!user && !!currentGroup;
  }

};
