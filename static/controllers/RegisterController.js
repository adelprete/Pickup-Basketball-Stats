'use strict'

angular.module('saturdayBall')

.controller('RegisterController', RegisterController);

RegisterController.$inject = ['$scope', '$route', 'UserService', '$timeout', '$location']

function RegisterController($scope, $route, UserService, $timeout, $location){

    $scope.betacode;
    $scope.message = "";
    $scope.submit = submit;
    $scope.userModel = {};
    $scope.verifypassword;

    //////////////////

    function submit() {
      UserService.createUser($scope.userModel).then(function (response){
        $scope.message = "Success! You may now log in. Redirecting to log in page."
        $timeout(function() {
          if ('next' in $route.current.params) {
            window.location.replace('/accounts/login/?next=' + $route.current.params['next']);
          }
          else {
            window.location.replace('/accounts/login/');
          }
        }, 3000);

      }, function(response){
        $scope.message = response.data;
      })
    }
};
