'use strict';

angular.module('noviga')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/eolQC/hardwares', {
        templateUrl: '/static/views/hardwareSetup/hardwaresetups.html',
        controller: 'HardwareSetupController',
        resolve: {
          resolvedAjaxItems: ['$q', '$rootScope', 'onegetHwsetup', 'onegetbinessHwsetup', 'AuthService',
          function ($q, $rootScope, onegetHwsetup, onegetbinessHwsetup, AuthService) {
            var deferred = $q.defer();
            AuthService.getUser()
            .then(
              function(data) {
                console.log(data);
                if (data === 'null') {
                  console.log(data);
                  $rootScope.loggedInUser = null;
                  deferred.reject({authenticated: 'notLoggedIn'});                  
                } else {
                  $rootScope.loggedInUser = {name: data.username, role: data.role, businessId: data.businessId};
                  console.log($rootScope.loggedInUser);
                  if (data.role === 'Admin') {
                    onegetHwsetup.get(function(data) {
                      deferred.resolve(data);
                    });
                  } else {
                    onegetbinessHwsetup.get({businessId: data.businessId}, function(data) {
                      deferred.resolve(data);
                    });
                  }
                }
              }
            )
            .catch(
              function(data) {
                $rootScope.loggedInUser = null;
                deferred.reject({authenticated: 'notLoggedIn'});
              }
            )
          return deferred.promise;}]
        }
      })

  }]);