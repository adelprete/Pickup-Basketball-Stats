'use strict';

angular.module('saturdayBall').controller('PlayWizardController', PlayWizardController);

PlayWizardController.$inject = ['$scope', '$routeParams', 'GameService', 'Session', 'playOptions',
  '$anchorScroll'];

function PlayWizardController($scope, $routeParams, GameService, Session, playOptions,
  $anchorScroll) {
    var vm = this;
    vm.checkTeam = checkTeam;
    vm.currentStep = 0;
    vm.currentTemplate = "static/partials/playWizard/step0.html";
    vm.nonPlayerFilter = nonPlayerFilter;
    vm.play = {};
    vm.startOver = startOver;
    vm.stepTemplates = [
      "static/partials/playWizard/step0.html",
      "static/partials/playWizard/step1.html",
      "static/partials/playWizard/step2.html",
      "static/partials/playWizard/step3.html",
      "static/partials/playWizard/step4.html",
    ];
    vm.step0 = step0;
    vm.step1 = step1;
    vm.step2 = step2;
    vm.step3 = step3;
    vm.step4 = step4;

    ////////////////////

    init()

    function init() {
    }

    function nonPlayerFilter(player) {
      return player.first_name != "Team1" && player.first_name != "Team2";
    }

    function checkTeam(team, player_id) {
      return team.some(function(player) {
        return player.id == player_id
      })
    }

    function goToStep(step) {
      vm.currentStep = step;
      vm.currentTemplate = vm.stepTemplates[vm.currentStep];
    }

    function startOver() {
      vm.play = {};
      goToStep(0);
    }

    function step0(primary_play) {
      vm.play['primary_play'] = primary_play;
      goToStep(1);
      $anchorScroll("step-header-anchor");
    }

    function step1(primary_player_id, first_name, last_name) {
      vm.play['primary_player'] = primary_player_id;
      vm.play['primary_player_display'] = first_name + ' ' + last_name
      if (['fgm', 'threepm'].indexOf(vm.play['primary_play']) > -1) {
        goToStep(3);
      }
      else if (['fga', 'threepa', 'blk', 'pf', 'to', 'sub_out'].indexOf(vm.play['primary_play']) > -1) {
        goToStep(2);
      }
      $anchorScroll("step-header-anchor");
    }

    function step2(secondary_player_id, first_name, last_name) {
      if (['fga', 'threepa'].indexOf(vm.play.primary_play) > -1) {
        if ((checkTeam($scope.$parent.game.team1, secondary_player_id) && checkTeam($scope.$parent.game.team1, vm.play.primary_player)) ||
            (checkTeam($scope.$parent.game.team2, secondary_player_id) && checkTeam($scope.$parent.game.team2, vm.play.primary_player))) {
          vm.play['secondary_play'] = 'oreb';
        }
        else {
          vm.play['secondary_play'] = 'dreb';
        }
      } else if (vm.play.primary_play === 'blk') {
        vm.play['secondary_play'] = 'ba';
      } else if (vm.play.primary_play === 'to' && secondary_player_id) {
        vm.play['secondary_play'] = 'stls';
      } else if (vm.play.primary_play === 'pf') {
        vm.play['secondary_play'] = 'fd';
      } else if (vm.play.primary_play === 'sub_out') {
        vm.play['secondary_play'] = 'sub_in';
      }

      if (secondary_player_id) {
        vm.play['secondary_player'] = secondary_player_id;
        vm.play['secondary_player_display'] = first_name + ' ' + last_name
      }

      if (['fga', 'threepa'].indexOf(vm.play.primary_play) > -1) {
        goToStep(3);
      } else {
        goToStep(4);
      }
      $anchorScroll("step-header-anchor");
    }

    function step3(assist_player, first_name, last_name) {
      if (assist_player) {
        if (['fgm', 'threepm'].indexOf(vm.play['primary_play']) > -1) {
          vm.play.assist = "asts";
        }
        else {
          vm.play.assist = "pot_ast";
        }
        vm.play.assist_player = assist_player
        vm.play.assist_player_display = first_name + ' ' + last_name
      }
      goToStep(4);
      $anchorScroll("step-header-anchor");
    }

    function step4() {
      vm.play['time'] = calculateTime($scope.$parent.plays);
      vm.play['game'] = $scope.$parent.game.id;
      GameService.createPlay(vm.play).then(function(response){
        $scope.$parent.plays.unshift(response);
        $scope.$parent.calculateScore();
        GameService.calculateStatlines($scope.$parent.game.id).then(function(response){});
      }, function(response) {
        alert("Something went wrong.  Last play not added.");
        console.log("Create Play failed: ", response);
      });
      vm.play = {}
      goToStep(0);
      $anchorScroll("step-header-anchor");
    }

    function calculateTime(plays) {
      var previous_play = plays[0];
      var previous_play_seconds = parseInt(plays[0].time.split(":")[0] * 3600) +
                              parseInt(plays[0].time.split(":")[1] * 60) +
                              parseInt(plays[0].time.split(":")[2])

      var increment = 0;
      if (['fgm', 'threepm', 'fga', 'threepa'].indexOf(vm.play.primary_play) > -1) {
        increment = 11;
      }
      else if (['to'].indexOf(vm.play.primary_play) > -1) {
        increment = 6;
      }
      else if (['sub_out'].indexOf(vm.play.primary_play) > -1 && previous_play.primary_play !== 'sub_out') {
        increment = 5;
      }
      else if (['pf'].indexOf(vm.play.primary_play) > -1) {
        increment = 8;
      }
      var new_play_time = previous_play_seconds + increment;

      return new_play_time;

    }

}
