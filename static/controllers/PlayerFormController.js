'use strict';

angular.module('saturdayBall').controller('PlayerFormController', PlayerFormController);

PlayerFormController.$inject = ['$scope', '$routeParams', 'PlayerService',
  '$anchorScroll', '$window'];

function PlayerFormController($scope, $routeParams, PlayerService,
  $anchorScroll, $window) {

    $scope.formErrors = {};
    $scope.groupId = $routeParams.groupId;
    $scope.loading = true;
    $scope.playerImage = null;
    $scope.player = {
      is_active: true
    };
    $scope.savePlayer = savePlayer;
    $scope.submitDisabled = false;

    ///////////////////////

    init();

    function init() {

      if ($routeParams.playerId) {
          PlayerService.getPlayer($routeParams.playerId).then(function(result){
            $scope.player = result;
            $scope.playerImage = $scope.player.image_src;
            $scope.loading = false;
            console.log("Player: ", $scope.player);
          }, function(result){
            console.log("Error: ", result);
            $scope.loading = false;
          })
      }
      else {
        $scope.loading = false;
      }

    }

    function savePlayer() {
      $scope.submitDisabled = true;
      $scope.player.group = $routeParams['groupId'];
      if (!_.has($scope.player, 'id')) {
        PlayerService.createPlayer($scope.player).then(function(result){
          $scope.message = "Player Created";
          $scope.player = result;
          window.location.replace("/group/"+$routeParams.groupId+"/players/"+result.id);
        }, function(result){
          $scope.formErrors = result.data;
          $scope.submitDisabled = false;
        });
      }
      else {
        if ($scope.player.image_src === null) {
          delete $scope.player.image_src;
        }
        PlayerService.updatePlayer($scope.player).then(function(result){
          $scope.message = "Player Updated";
          $scope.player = result;
          $window.location.href = "/group/"+$routeParams.groupId+"/players/"+result.id;
        }, function(result){
        });
      }
    }

    var handleFileSelect=function(evt) {
      var file=evt.currentTarget.files[0];
      var reader = new FileReader();
      reader.onload = function (evt) {
        $scope.$apply(function($scope){
          $scope.playerImage=evt.target.result;
        });
      };
      reader.readAsDataURL(file);
    };

    angular.element(document.querySelector('#fileInput')).on('change', handleFileSelect);

  }
