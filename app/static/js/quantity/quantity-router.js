'use strict';

angular.module('noviga')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/admincontrol/quantities', {
        templateUrl: '/static/views/quantity/quantities.html',
        controller: 'QuantityController',
        resolve:{
          resolvedAjaxItems: ['$q', '$rootScope', 'Quantitydata', 'AuthService',
          function ($q, $rootScope, Quantitydata, AuthService) {
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
                    Quantitydata.get(function(data) {
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