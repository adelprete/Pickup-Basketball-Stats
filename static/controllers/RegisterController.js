'use strict'

angular.module('saturdayBall')

.controller('RegisterController', function RegisterController($scope, $routeParams, UserService){
    $scope.betacode;
    $scope.verifypassword;

    $scope.submit = function(){

      UserService.createUser($scope.user).then(function (response){
        console.log(response);
      }, function(response){
        $scope.message = response.data;
      })
    }
});
