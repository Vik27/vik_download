'use strict';

angular.module('noviga')
  .factory('Quantity', ['$resource', function ($resource) {
    return $resource('noviga/quantities/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);


angular.module('noviga')
  .factory('Quantitydata', ['$resource', function ($resource) {
    return $resource('noviga/quantities/all', {}, {
      'get': { method: 'GET'},
    });
  }]);
