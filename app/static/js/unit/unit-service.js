'use strict';

angular.module('noviga')
  .factory('Unit', ['$resource', function ($resource) {
    return $resource('noviga/units/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);
