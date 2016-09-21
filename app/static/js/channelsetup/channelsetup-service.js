'use strict';

angular.module('noviga')
  .factory('Channelsetup', ['$resource', function ($resource) {
    return $resource('noviga/channelsetups/:id', {}, {
      'query': { method: 'GET', isArray: true},
    });
  }]);


angular.module('noviga')
  .factory('binessChannelsetup', ['$resource', function ($resource) {
    return $resource('noviga/businesses/:businessId/channelsetups/:id', {}, {
      'query': { method: 'GET', isArray: true},
      'get': { method: 'GET'},
      'update': { method: 'PUT'}
    });
  }]);


angular.module('noviga')
  .factory('Channeltemplates', ['$resource', function ($resource) {
    return $resource('noviga/channeltemplates/:id', {}, {
      'query': { method: 'GET', isArray: true}
    });
  }]);


angular.module('noviga')
  .factory('binessChanneltemps', ['$resource', function ($resource) {
    return $resource('noviga/businesses/:businessId/channeltemplates/:id', {}, {
      'query': { method: 'GET', isArray: true}
    });
  }]);


angular.module('noviga')
  .factory('onegetbinessChansetup', ['$resource', function ($resource) {
    return $resource('noviga/businesses/:businessId/chansetupsdata', {}, {
      'get': { method: 'GET'},
    });
  }]);


angular.module('noviga')
  .factory('onegetChansetup', ['$resource', function ($resource) {
    return $resource('noviga/businesses/all/chansetupsdata', {}, {
      'get': { method: 'GET'},
    });
  }]);