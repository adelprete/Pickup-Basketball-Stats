'use strict';

angular.module('saturdayBall').factory('Session', ['$q', '$http', 'UserService', 'GroupService', function($q, $http, UserService, GroupService){
  var user, currentGroup;

  function init() {
    console.log("Session init called");
    getCurrentUser().then(function(result){
      console.log("got User");
      user = result;
    }, function(error){
      console.log(error);
    });
    getCurrentGroup().then(function(group){
      currentGroup = group;
    });
  }

  function getCurrentUser() {
    var deferred = $q.defer();
    UserService.currentUser().then(function(response){
      user = response;
      console.log("Grabbed User: ", user);
      deferred.resolve(user);
    }, function(response){
      deferred.reject(response.data);
    });

    return deferred.promise;
  }

  function getCurrentGroup() {
    var deferred = $q.defer();
    deferred.resolve({'test': 'test'});
    return deferred.promise;
  }

  function available() {
    return !!user && !!currentGroup;
  }

  return {
      init: init,
      available: available,
      currentUser: function() {
        return user
      },
      currentGroup: function() {
        return currentGroup
      }
    }

}]);
