angular.module('saturdayBall')

.controller('CreateGroupController', CreateGroupController);

CreateGroupController.$inject = ['$scope', '$location', 'GroupService', 'Session', 'settingOptions']

function CreateGroupController($scope, $location, GroupService, Session, settingOptions) {

    $scope.message = "";
    $scope.save = save;
    $scope.settingOptions = settingOptions;
    $scope.settings = {
      score_type: $scope.settingOptions.SCORE_TYPES[0].code,
      game_type: $scope.settingOptions.GAME_TYPES[0].code,
      points_to_win: $scope.settingOptions.POINTS_TO_WIN[0].code,
      possessions_min: 100,
      fga_min: 15
    };
    $scope.user = {};

    ////////////////////

    init();

    function init() {
      $scope.user = Session.currentUser();
    }

    function save() {
      $scope.message = "Saving..."
      GroupService.createGroup($scope.settings).then(function(response) {
        $scope.message = "Saved Successfully";
        window.location.replace('/group/' + response.id);
      }, function(response) { 
        if (response.status == 406) {
          $scope.message = "Invalid Beta Code";
        }
        else {
          $scope.message = "Failed"
        }
      });
    }
};
