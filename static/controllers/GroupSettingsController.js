'use strict';

angular.module('saturdayBall')

.controller('GroupSettingsController', GroupSettingsController);

GroupSettingsController.$inject = ['$scope', '$routeParams', 'GroupService', 'Session', 'settingOptions']

function GroupSettingsController($scope, $routeParams, GroupService, Session, settingOptions) {

    $scope.message = "";
    $scope.save = save;
    $scope.settings = undefined;
    $scope.settingOptions = settingOptions;
    $scope.user = Session.currentUser();

    ///////////////////////

    init();

    function init() {
      GroupService.getGroup($routeParams.groupId).then(function(response) {
        $scope.settings = response;
      }, function(response) {
        console.log(response);
      });
    }

    function save() {
      $scope.message = "Saving..."
      GroupService.updateGroup($scope.settings).then(function(response) {
        $scope.message = "Saved Successfully";
      }, function(response){
        $scope.message = "Failed to save"
      });
    }
};
