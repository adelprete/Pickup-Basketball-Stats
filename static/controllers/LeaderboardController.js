'use strict';

angular.module('saturdayBall').controller('LeaderboardController', LeaderboardController);

LeaderboardController.$inject = ['$scope', '$routeParams', 'GroupService'];

function LeaderboardController($scope, $routeParams, GroupService) {

  $scope.filterForm = {};
  $scope.filterOptions = {'seasons': []};
  $scope.isFormVisible = false;
  $scope.ShowHideForm = ShowHideForm;

  init();

  ///////////////////////

  function init() {
    GroupService.getGroupSeasons($routeParams.groupId).then(function(response) {
      $scope.filterOptions.seasons = response.seasons;
      $scope.filterForm.season = response.seasons[0].id;
    }, function(response){
      console.log("Failed: ", response);
    })

    GroupService.getGroup($routeParams.groupId).then(function(response) {
      $scope.filterForm.possessions_min = response.possessions_min;
    }, function(response) {
      console.log(response);
    });
  }

  function ShowHideForm() {
      $scope.isFormVisible = $scope.isFormVisible ? false : true;
  }

};
