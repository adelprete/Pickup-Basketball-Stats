angular.module('saturdayBall')

.controller('GroupSettingsController', function GroupSettingsController($scope, $routeParams, GroupService){

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
