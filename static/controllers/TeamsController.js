'use strict';

angular.module('saturdayBall')

.controller('TeamsController', TeamsController);

TeamsController.$inject = ['$scope', '$routeParams', 'RoleHelper', 'Session', 'TeamService']

function TeamsController($scope, $routeParams, RoleHelper, Session, TeamService) {

  $scope.filterForm = {};
  $scope.groupId = $routeParams.groupId;
  $scope.loadingPage = true;
  $scope.teams = [];
  $scope.user = Session.currentUser();

  ///////////////////

  init();

  function init() {
    TeamService.getTeams({'group__id': $scope.groupId}).then(function(response) {
      $scope.teams = response;
      $scope.loadingPage = false;
    }, function(response) {
      console.log("Failed: ", response);
    })
    
  }

}
