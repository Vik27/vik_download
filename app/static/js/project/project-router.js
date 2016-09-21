'use strict';

angular.module('noviga')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/eolQC/projects', {
        templateUrl: '/static/views/project/projects.html',
        controller: 'ProjectController',
        resolve:{
          resolvedAjaxItems: ['$q', '$rootScope', 'onegetProject', 'onegetbinessProject', 'AuthService',
          function ($q, $rootScope, onegetProject, onegetbinessProject, AuthService) {
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
                    onegetProject.get(function(data) {
                      deferred.resolve(data);
                    });
                  } else {
                    onegetbinessProject.get({businessId: data.businessId}, function(data) {
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
