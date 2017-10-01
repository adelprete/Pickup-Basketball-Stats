angular.module('saturdayBall')

.controller('GroupSettingsController', function GroupSettingsController($scope, $routeParams, GroupService, User){
    $scope.OPTIONS = {
      SCORE_TYPES: [
        {'code': '1and2', 'name': '1\'s and 2\'s'},
        {'code': '2and3', 'name': '2\'s and 3\'s'}
      ],
      GAME_TYPES: [
        {'code': '5v5', 'name': '5 on 5'},
        {'code': '4v4', 'name': '4 on 4'},
        {'code': '3v3', 'name': '3 on 3'},
        {'code': '2v2', 'name': '2 on 2'},
        {'code': '1v1', 'name': '1 on 1'}
      ],
      POINTS_TO_WIN: [
        {'code': '11', 'name': '11'},
        {'code': '30', 'name': '30'},
        {'code': 'other', 'name': 'Other'},
      ]
    }


    $scope.user = User.currentUser();

    GroupService.getGroup(1).then(function(response){
      $scope.settings = response
    }, function(response){
      console.log(response);
    })

    $scope.save = function(){
      $scope.message = "Saving..."
      GroupService.updateGroup($scope.settings).then(function(response){
        $scope.message = "Saved Successfully";
      }, function(response){
        $scope.message = "Failed to save"
      });
    }
});
