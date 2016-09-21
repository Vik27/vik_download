'use strict';

angular.module('noviga')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/admincontrol/chassis', {
        templateUrl: 'static/views/Chassis/Chassis.html',
        controller: 'ChassisController',
        resolve:{
          resolvedAjaxItems: ['$q', '$rootScope', 'Chassis', 'AuthService',
          function ($q, $rootScope, Chassis, AuthService) {
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
                    Chassis.query(function(data) {
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