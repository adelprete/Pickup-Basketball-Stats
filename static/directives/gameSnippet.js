'use strict';

angular
    .module('saturdayBall')
    .directive('gameSnippet', gameSnippet);

function gameSnippet() {
    var directive = {
        link: link,
        scope: {
          groupId: '@',
          game: '='
        },
        templateUrl: 'static/partials/directives/gameSnippet.html',
        restrict: 'EA'
    };
    return directive;

    function link(scope, element, attrs) {
    }
  }
