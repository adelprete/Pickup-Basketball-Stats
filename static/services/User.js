'use strict';

angular.module('saturdayBall').factory('User', ['$q', '$http', 'UserService', function($q, $http, UserService){
  var currentUser;

  function getCurrentUser() {
    var deferred = $q.defer();
    if (currentUser) {
      console.log("Cached User: ", currentUser);
      deferred.resolve(currentUser);
    }
    else {
      UserService.currentUser().then(function(response){
        currentUser = response;
        console.log("Grabbed User: ", currentUser);
        deferred.resolve(currentUser);
      }, function(response){
        deferred.reject(response.data);
      })
    }
    return deferred.promise;
  }

  return{
      currentUser: getCurrentUser
    }

}]);
