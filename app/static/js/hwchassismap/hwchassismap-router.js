'use strict';

angular.module('noviga')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/eolQC/hwchassismaps', {
        templateUrl: '/static/views/hwchassismap/hwchassismaps.html',
        controller: 'HwchassismapController',
        resolve:{
          resolvedHwchassismap: ['Hwchassismap', function (Hwchassismap) {
            return Hwchassismap.query();
          }]
        }
      })
    }]);
