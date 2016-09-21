'use strict';

angular.module('noviga')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/admincontrol/devices', {
        templateUrl: '/static/views/devicetable/devicetables.html',
        controller: 'DevicetableController',
        resolve: {
          resolvedAjaxItems: ['$q', '$rootScope', 'Devicedata', 'AuthService',
          function ($q, $rootScope, Devicedata, AuthService) {
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
                    Devicedata.get(function(data) {
                      deferred.resolve(data);
                    });
                  } else {
                    deferred.reject({authenticated: 'unauthorized'});
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