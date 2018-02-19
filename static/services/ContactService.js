'use strict';

angular.module('saturdayBall').factory('ContactService', ContactService);

ContactService.$inject = ['$q', '$http'];

function ContactService($q, $http) {
  var service = {
    createContact: createContact
  };
  return service;

  /////////////////////

  function createContact(data) {
    var deferred = $q.defer();
    $http.post('/api/contacts/', data).then(function(response, status, config, headers){
      deferred.resolve(response.data);
    }, function(response){
      deferred.reject(response);
    });

    return deferred.promise;
  }
}
