angular.module('saturdayBall')

.controller('CreateGroupController', function CreateGroupController($scope, $location, $routeParams, GroupService, User){
    $scope.user = User.currentUser();
    $scope.settings = {
      possessions_min: 100,
      fga_min: 15
    }
    var path = $location.path('/group/' + response.id);
    window.location = $location.host() + path;
    $scope.save = function(){
      $scope.message = "Saving..."
      console.log();
      GroupService.createGroup($scope.settings).then(function(response){
        $scope.message = "Saved Successfully";
        var path = $location.path('/group/' + response.id);
        window.location = $location.host() + path;
      }, function(response){
        $scope.message = "Failed to save"
      });
    }
});
