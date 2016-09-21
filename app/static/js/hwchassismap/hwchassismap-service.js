'use strict';

angular.module('noviga')
  .factory('Hwchassismap', ['$resource', function ($resource) {
    return $resource('noviga/hwchassismaps/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);
