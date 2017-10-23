'use strict'

angular.module('saturdayBall')

.controller('RegisterController', RegisterController);

RegisterController.$inject = ['$scope', 'UserService']

function RegisterController($scope, UserService){
    $scope.betacode;
    $scope.message = "";
    $scope.submit = submit;
    $scope.userModel = {};
    $scope.verifypassword;

    //////////////////

    function submit() {
      UserService.createUser($scope.userModel).then(function (response){
        console.log(response);
      }, function(response){
        $scope.message = response.data;
      })
    }
};
