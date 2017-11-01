'use strict';

angular.module('saturdayBall').controller('OverviewBoardController', OverviewBoardController);

OverviewBoardController.$inject = ['$scope', '$controller'];

function OverviewBoardController($scope, $controller) {

    init();

    /////////////////

    function init() {

      console.log($scope.filterForm);

    }
};
