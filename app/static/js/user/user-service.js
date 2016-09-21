'use strict';

angular.module('noviga')
  .factory('User', ['$resource', function ($resource) {
    return $resource('noviga/users/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);

angular.module('noviga')
  .factory('UserBiness', ['$resource', function ($resource) {
    return $resource('noviga/businesses/:businessId/users/:userId', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
}]);

angular.module('noviga')
  .factory('Userdata', ['$resource', function ($resource) {
    return $resource('noviga/users/all', {}, {
      'get': { method: 'GET'},
    });
}]);
