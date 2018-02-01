'use strict';

angular.module('saturdayBall').factory('RoleHelper', RoleHelper);

RoleHelper.$inject = ['$q', '$http'];

function RoleHelper($q, $http) {
  var service = {
    canEdit: canEdit,
    isAdmin: isAdmin
  };
  return service;

  /////////////////////

  function canEdit(user, groupId) {
    if (user) {
      for (var i = 0; i < user.group_permissions.length; i++) {
        if (user.group_permissions[i][0] === parseInt(groupId, 10) && user.group_permissions[i][2] === 'edit') {
          return true;
        }
      }
    }
    return false;
  }

  function isAdmin(user, groupId) {
    if (user) {
      for (var i = 0; i < user.group_permissions.length; i++) {
        if (user.group_permissions[i][0] === parseInt(groupId, 10) && user.group_permissions[i][2] === "admin") {
          return true;
        }
      }
    }
    return false;
  }
}
