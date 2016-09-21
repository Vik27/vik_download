'use strict';

angular.module('noviga')
  .factory('HardwareSetup', ['$resource', function ($resource) {
    return $resource('noviga/hardwaresetups/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);


angular.module('noviga')
  .factory('binessHwsetup', ['$resource', function ($resource) {
    return $resource('noviga/businesses/:businessId/hardwaresetups/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);


angular.module('noviga')
  .factory('onegetbinessHwsetup', ['$resource', function ($resource) {
    return $resource('noviga/businesses/:businessId/hwsetupsdata', {}, {
      'get': { method: 'GET'},
    });
  }]);


angular.module('noviga')
  .factory('onegetHwsetup', ['$resource', function ($resource) {
    return $resource('noviga/businesses/all/hwsetupsdata', {}, {
      'get': { method: 'GET'},
    });
  }]);


angular.module('noviga')
  .factory('verifyHwsetup', ['$resource', function($resource) {
    return $resource('noviga/verifyhwsetup/:id', {}, {
      'get': { method: 'GET'},
    })
  }]);


angular.module('noviga')
  .factory('verifybinessHwsetup', ['$resource', function($resource) {
    return $resource('noviga/businesses/:businessId/verifyhwsetup/:id', {}, {
      'get': { method: 'GET'},
    })
  }]);