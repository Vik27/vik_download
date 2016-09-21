'use strict';

angular.module('noviga')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/eolQC/channels', {
        templateUrl: 'static/views/channelsetup/channelsetups.html',
        controller: 'ChannelsetupController',
        resolve: {
          resolvedAjaxItems: ['$q', '$rootScope', 'onegetChansetup', 'onegetbinessChansetup', 'AuthService',
          function ($q, $rootScope, onegetChansetup, onegetbinessChansetup, AuthService) {
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
                    onegetChansetup.get(function(data) {
                      deferred.resolve(data);
                    });
                  } else {
                    onegetbinessChansetup.get({businessId: data.businessId}, function(data) {
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