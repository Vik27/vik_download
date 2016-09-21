'use strict';

angular.module('noviga')
  .factory('Chassis', ['$resource', function ($resource) {
    return $resource('noviga/Chassis/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);
