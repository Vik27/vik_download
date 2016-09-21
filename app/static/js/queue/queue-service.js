'use strict';

angular.module('noviga')
  .factory('Queue', ['$resource', function ($resource) {
    return $resource('noviga/queues/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);

angular.module('noviga')
  .factory('binessQueue', ['$resource', function ($resource) {
    return $resource('noviga/businesses/:businessId/queues/:id', {}, {
      'query': { method: 'GET', isArray: true},
    });
  }]);


angular.module('noviga')
  .factory('Queuedata', ['$resource', function ($resource) {
    return $resource('noviga/queues/all', {}, {
      'query': { method: 'GET'},
    });
  }]);
