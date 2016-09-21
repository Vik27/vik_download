'use strict';

angular.module('noviga')
  .factory('Business', ['$resource', function ($resource) {
    return $resource('noviga/businesses/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);
