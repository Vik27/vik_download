'use strict';

angular.module('noviga')
  .factory('binessHwchaschanmap', ['$resource', function ($resource) {
    return $resource('noviga/businesses/:businessId/hwchaschanmaps/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);
