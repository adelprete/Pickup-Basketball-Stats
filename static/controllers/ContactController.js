'use strict'

angular.module('saturdayBall')

.controller('ContactController', ContactController);

ContactController.$inject = ['$scope', '$route', '$anchorScroll', 'ContactService']

function ContactController($scope, $route, $anchorScroll, ContactService){

  $scope.contactModel = {};
  $scope.submit = submit; 

  ////////////////////

  function submit() {
    $scope.message = "Sending..."
    ContactService.createContact($scope.contactModel).then(function (response){
      $scope.message = "Message Received!"
      $scope.contactform.$setPristine();
      $scope.contactform.$setUntouched();
      $scope.contactModel = {};
    }, function(response){
      $scope.message = "Message failed to send.";
    })

  }

};
