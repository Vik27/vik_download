'use strict';

angular.module('noviga')
  .factory('binessAcqSettings', ['$resource', function ($resource) {
    return $resource('noviga/businesses/:businessId/hardwareSetups/:hwsetupId/acqsettings', {}, {
      'update': { method: 'PUT'}
    });
  }]);

angular.module('noviga')
  .factory('AcqSettings', ['$resource', function ($resource) {
    return $resource('noviga/hardwareSetups/:hwsetupId/acqsettings', {}, {
      'update': { method: 'PUT'}
    });
  }]);
