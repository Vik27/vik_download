'use strict';

angular.module('noviga')
  .factory('Project', ['$resource', function ($resource) {
    return $resource('noviga/projects/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);


angular.module('noviga')
  .factory('binessProject', ['$resource', function ($resource) {
    return $resource('noviga/businesses/:businessId/projects/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);


angular.module('noviga')
  .factory('onegetbinessProject', ['$resource', function ($resource) {
    return $resource('noviga/businesses/:businessId/projectsdata', {}, {
      'get': { method: 'GET'},
    });
  }]);


angular.module('noviga')
  .factory('onegetProject', ['$resource', function ($resource) {
    return $resource('noviga/businesses/all/projectsdata', {}, {
      'get': { method: 'GET'},
    });
  }]);


angular.module('noviga')
  .factory('runProject', ['$resource', function($resource) {
    return $resource('noviga/runproject/:id', {}, {
      'get': { method: 'GET'},
    })
  }]);


angular.module('noviga')
  .factory('runbinessProject', ['$resource', function($resource) {
    return $resource('noviga/businesses/:businessId/runproject/:id', {}, {
      'get': { method: 'GET'},
    })
  }]);
