'use strict';

angular.module('saturdayBall').factory('GameService', function($q, $http){
  var apiurl, myData;
  return {
    getGamePlays: function(gameid){
      var deferred = $q.defer();
      $http.get(`/api/plays/?gameid=${gameid}`).then(function(response, status, config, headers){
        deferred.resolve(response.data);
      }, function(response){
        deferred.reject(response);
      });

      return deferred.promise;
    },
    getGame: function(gameid){
      var deferred = $q.defer();
      $http.get(`/api/games/${gameid}/`).then(function(response, status, config, headers){
        deferred.resolve(response.data);
      }, function(response){
        deferred.reject(response);
      });

      return deferred.promise;
    },
    calculateStatlines: function(gameid){
      var deferred = $q.defer();
      $http.get(`/api/games/${gameid}/calculate-statlines`).then(function(response, status, config, headers){
        deferred.resolve(response.data);
      }, function(response){
        deferred.reject(response);
      });

      return deferred.promise;
    },
    createPlay: function(data){
      var deferred = $q.defer();
      $http.post(`/api/plays/`, data).then(function(response, status, config, headers){
        deferred.resolve(response.data);
      }, function(response){
        deferred.reject(response);
      });

      return deferred.promise;
    },
    updatePlay: function(play){
      var deferred = $q.defer();
      $http.post(`/api/plays/${play.id}/`, play).then(function(response, status, config, headers){
        deferred.resolve(response.data);
      }, function(response){
        deferred.reject(response);
      });

      return deferred.promise;
    },
    getPlay: function(playid){
      var deferred = $q.defer();
      $http.get(`/api/plays/${playid}/`).then(function(response, status, config, headers){
        deferred.resolve(response.data);
      }, function(response){
        deferred.reject(response);
      });

      return deferred.promise;
    },
    deletePlay: function(playid){
      var deferred = $q.defer();
      $http.delete(`/api/plays/${playid}/`).then(function(response, status, config, headers){
        deferred.resolve(response.data);
      }, function(response){
        deferred.reject(response);
      });

      return deferred.promise;
    }
  };
});
