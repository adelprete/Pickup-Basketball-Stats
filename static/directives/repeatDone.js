'use strict';

angular
    .module('saturdayBall')
    .directive('colEqual', colEqual)

colEqual.$inject = ['$timeout']

function colEqual($timeout){
  var directive = {
      link: link
  };
  return directive;

  function link(scope, element, attrs) {
      if (scope.$last) { // all are rendered
          scope.$eval(function() {
            $timeout(function() {
              $(function() {
                $('.row').each(function(i, elem) {
                    $(elem)
                        .find('.col-equal')
                        .matchHeight({byRow: true});
                });
              });
            }, 0);
          });
      }
  };
}
