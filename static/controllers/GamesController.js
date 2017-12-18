'use strict';

angular.module('saturdayBall')

.controller('GamesController', GamesController);

GamesController.$inject = ['$scope', '$routeParams', 'GameService']

function GamesController($scope, $routeParams, GameService) {

  $scope.changeFiltering = changeFiltering;
  $scope.games = [];
  $scope.groupId = $routeParams.groupId;
  $scope.filteredDailyGames = [];
  $scope.loadingPage = true;
  $scope.filterMessage = "View Unpublished Games"
  $scope.publishedGames = true;


  $scope.pageChanged = pageChanged;
  $scope.pagination = {
    published: true,
    currentPage: 1,
    numPerPage: 12,
    maxSize: 5
  }

  ///////////////////

  init();

  function init() {
    pageChanged()
  }

  function changeFiltering() {
    if ($scope.pagination.published) {
      $scope.pagination.published = false;
      $scope.pagination.currentPage = 1;
      $scope.filterMessage = "View Published Games"
    }
    else {
      $scope.pagination.published = true;
      $scope.pagination.currentPage = 1;
      $scope.filterMessage = "View Unpublished Games"
    }

    getGamesPage();
  }

  function getGamesPage(published) {
    $scope.loadingPage = true;
    GameService.getGames($routeParams.groupId, $scope.pagination).then(function(results){
      $scope.pagination.currentPage = results.currentPage;
      $scope.pagination.totalItems = results.totalItems;
      $scope.filteredDailyGames = results.items;

      $scope.loadingPage = false;

    }, function(err){
      console.log(err)
    });
  }

  function pageChanged() {

    if ($scope.pagination.currentPage) {
      getGamesPage();
    }
    console.log('Page changed to: ' + $scope.pagination.currentPage);
  };

}
