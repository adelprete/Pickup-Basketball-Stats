'use strict';

angular.module('saturdayBall').controller('TeamFormController', TeamFormController);

TeamFormController.$inject = ['$scope', '$routeParams', 'TeamService',
  '$anchorScroll', '$window'];

function TeamFormController($scope, $routeParams, TeamService,
  $anchorScroll, $window) {

    $scope.formErrors = {};
    $scope.groupId = $routeParams.groupId;
    $scope.loading = true;
    $scope.teamImage = null;
    $scope.team = {
      is_active: true
    };
    $scope.saveTeam = saveTeam;
    $scope.submitDisabled = false;

    ///////////////////////

    init();

    function init() {

      if ($routeParams.teamId) {
          TeamService.getTeam($routeParams.teamId).then(function(result){
            $scope.team = result;
            $scope.teamImage = $scope.team.image_src;
            console.log("Team: ", $scope.team);
          }, function(result){
            console.log("Error: ", result);
          })
          
          PlayerService.getPlayers($scope.groupId).then(function(result){
            $scope.players = result;
            console.log("Players: ", $scope.players);
          }, function(result){
            console.log("Error: ", result);
          })
      }
      else {
        $scope.loading = false;
      }

    }

    function saveTeam() {
      $scope.submitDisabled = true;
      $scope.team.group = $scope.groupId;
      if (!_.has($scope.team, 'id')) {
        TeamService.createTeam($scope.team).then(function(result){
          $scope.message = "Team Created";
          $scope.team = result;
          window.location.replace("/group/"+$scope.groupId+"/teams/"+result.id);
        }, function(result){
          $scope.formErrors = result.data;
          $scope.submitDisabled = false;
        });
      }
      else {
        if ($scope.team.image_src === null) {
          delete $scope.team.image_src;
        }
        TeamService.updateTeam($scope.team).then(function(result){
          $scope.message = "Team Updated";
          $scope.team = result;
          $window.location.href = "/group/"+$scope.groupId+"/teams/"+result.id;
        }, function(result){
        });
      }
    }

    var handleFileSelect=function(evt) {
      var file=evt.currentTarget.files[0];
      var reader = new FileReader();
      reader.onload = function (evt) {
        $scope.$apply(function($scope){
          $scope.teamImage=evt.target.result;
        });
      };
      reader.readAsDataURL(file);
    };

    angular.element(document.querySelector('#fileInput')).on('change', handleFileSelect);

  }
