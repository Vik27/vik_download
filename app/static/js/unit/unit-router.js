'use strict';

angular.module('noviga')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/admincontrol/units', {
        templateUrl: '/static/views/unit/units.html',
        controller: 'UnitController',
        resolve:{
          resolvedAjaxItems: ['$q', '$rootScope', 'Unit', 'AuthService',
          function ($q, $rootScope, Unit, AuthService) {
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
                    Unit.query(function(data) {
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