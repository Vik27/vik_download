'use strict';

angular.module('noviga')
  .factory('Devicetable', ['$resource', function ($resource) {
    return $resource('noviga/devicetables/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);

angular.module('noviga')
  .factory('binessDevice', ['$resource', function ($resource) {
    return $resource('noviga/businesses/:businessId/devicetables/:id', {}, {
      'query': { method: 'GET', isArray: true},
    });
  }]);


angular.module('noviga')
  .factory('Devicedata', ['$resource', function ($resource) {
    return $resource('noviga/devices/all', {}, {
      'query': { method: 'GET'},
    });
  }]);
