'use strict';

angular.module('saturdayBall').factory('User', ['$q', '$http', 'UserService', function($q, $http, UserService){
  var currentUser;

  function getCurrentUser() {
    var deferred = $q.defer();
    if (currentUser) {
      console.log('returned cached user');
      deferred.resolve(currentUser);
    }
    else {
      console.log('grabbing user data');
      UserService.currentUser().then(function(response){
        console.log('grabbed user: ', response);
        currentUser = response;
        deferred.resolve(currentUser);
      }, function(response){
        deferred.reject(response.data);
        console.log("currentUser Error: ", response);
      })
    }
    return deferred.promise;
  }

  return{
      currentUser: getCurrentUser
    }

}]);
