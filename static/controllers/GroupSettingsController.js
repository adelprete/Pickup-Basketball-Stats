'use strict';

angular.module('saturdayBall')

.controller('GroupSettingsController', GroupSettingsController);

GroupSettingsController.$inject = ['$scope', '$routeParams', 'GroupService', 'Session',
    'settingOptions', '$uibModal', '$document', 'inviteOptions', 'PlayerService']

function GroupSettingsController($scope, $routeParams, GroupService, Session,
    settingOptions, $uibModal, $document, inviteOptions, PlayerService) {

    $scope.close = close;
    $scope.editingMembers = {};
    $scope.invite = {};
    $scope.inviteOptions = inviteOptions;
    $scope.message = "";
    $scope.modify = modify;
    $scope.open = open;
    $scope.playerDisplay = playerDisplay;
    $scope.players = {};
    $scope.remove = remove;
    $scope.save = save;
    $scope.send = send;
    $scope.settings = undefined;
    $scope.settingOptions = settingOptions;
    $scope.update = update;
    $scope.user = Session.currentUser();

    ///////////////////////

    init();

    function init() {
      GroupService.getGroup($routeParams.groupId).then(function(response) {
        $scope.settings = response;
      }, function(response) {
        console.log('Getting group failed: ', response);
      });
      getPlayers();
      getMembers();
    }

    function getPlayers() {
      PlayerService.getPlayers({'group': $routeParams.groupId}).then(function(response) {
        $scope.players = _.filter(response, function(player){
          return (player.first_name !== 'Team1' && player.first_name !== 'Team2');
        });
      }, function(response) {
        console.log("Getting players failed: ", response)
      });
    }

    function getMembers() {
      GroupService.getMemberPermissions({'group': $routeParams.groupId}).then(function(response) {
        $scope.members = response;
        for (var i = 0, length = $scope.members.length; i < length; i++) {
          $scope.editingMembers[$scope.members[i].id] = false;
        }
      }, function(response) {
        console.log("Getting members failed: ", response)
      });
    }

    function modify(member){
        $scope.editingMembers[member.id] = true;
    };


    function update(member){
        $scope.editingMembers[member.id] = false;
        GroupService.updateMemberPermission(member).then(function(response){
        }, function(response){
          console.log(response);
        })
    };

    function remove(member){
        GroupService.deleteMemberPermission(member).then(function(response){
          getMembers();
        }, function(response){
          console.log(response);
        })
    };

    function save() {
      $scope.message = "Saving..."
      GroupService.updateGroup($scope.settings).then(function(response) {
        $scope.message = "Saved Successfully";
      }, function(response){
        $scope.message = "Failed to save"
      });
    }

    var modalInstance;
    function open(size, parentSelector) {
      var parentElem = parentSelector ?
        angular.element($document[0].querySelector('.modal-demo ' + parentSelector)) : undefined;
      modalInstance = $uibModal.open({
        animation: true,
        templateUrl: 'static/partials/inviteModal.html',
        size: size,
        scope: $scope
      });

      modalInstance.result.then(function (selectedItem) {
        $scope.selected = selectedItem;
      }, function () {
        console.log('Modal dismissed at: ' + new Date());
      });
    }

    function close() {
      modalInstance.close();
    }

    function send(form) {
      if (form.$valid) {
        $scope.inviteMessage = "Sending Invite...";
        $scope.invite.group = $routeParams.groupId;
        GroupService.createMemberInvite($scope.invite).then(function(response) {
          $scope.inviteMessage = "Invite Sent";
        }, function(response){
          $scope.inviteMessage = response.data.message;
        })
      }
      console.log("ok clicked");
    }

    function playerDisplay(id) {
      let player = _.filter($scope.players, function(player){
        return player.id === id;
      })
      if (player.length) {
        return player[0].first_name + ' ' + player[0].last_name
      }
      else {
        return "None"
      }
    }
};
