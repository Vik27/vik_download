angular.module('noviga').controller('loginController',
  ['$rootScope', '$scope', '$location', 'AuthService',
  function ($rootScope, $scope, $location, AuthService) {

    $scope.login = function () {

      // initial values
      $scope.error = false;
      $scope.disabled = true;

      // call login from service
      AuthService.login($scope.loginForm.username, $scope.loginForm.password)
        // handle success
        .then(function (data) {
          $location.path('/eolQC/projects/');
          $scope.disabled = false;
          $scope.loginForm = {};
          $rootScope.$broadcast('login', $scope.loginForm.username);
          console.log(data);
          $rootScope.loggedInUser = {'name': data.name, 'role': data.role, 'businessId': data.businessId};
        })
        // handle error
        .catch(function () {
          $scope.error = true;
          $scope.errorMessage = "Invalid username and/or password";
          $scope.disabled = false;
          $scope.loginForm = {};
          $rootScope.loggedInUser = null;
        });

    };

}]);

angular.module('noviga').controller('logoutController',
  ['$scope', '$location', 'AuthService',
  function ($scope, $location, AuthService) {

    $scope.logout = function () {

      // initial values
      $scope.error = false;
      $scope.disabled = true;

      // call login from service
      AuthService.logout()
        // handle success
        .then(function () {
          $location.path('/login');
          $scope.disabled = false;
          $scope.loginForm = {};
        })
        // handle error
        .catch(function () {
          $location.path('/loggedOut');
        });

    };

    //     $scope.getStatus = function() {

    //   AuthService.getStatus()
    //   .then(function () {
    //     $location.path('/loggedOut')
    //   },
    //   function () {
    //     $location.path('/dummy')
    //   })
    // };

}]);

// angular.module('noviga').controller('dummyController',
//   ['$scope', '$location', 'AuthService',
//   function ($scope, $location, AuthService) {

//     $scope.getStatus = function() {

//       AuthService.getStatus()
//       .then(function () {
//         $location.path('/loggedOut')
//       },
//       function () {
//         $location.path('/dummy')
//       })
//     }
// }]);

// angular.module('noviga').controller('registerController',
//   ['$scope', '$location', 'AuthService',
//   function ($scope, $location, AuthService) {

//     $scope.register = function () {

//       // initial values
//       $scope.error = false;
//       $scope.disabled = true;

//       // call login from service
//       AuthService.register($scope.registerForm.username, $scope.registerForm.password, $scope.registerForm.email)
//         // handle success
//         .then(function () {
//           $location.path('/login');
//           $scope.disabled = false;
//           $scope.registerForm = {};
//         })
//         // handle error
//         .catch(function () {
//           $scope.error = true;
//           $scope.disabled = false;
//           $scope.registerForm = {};
//           $scope.errorMessage = "User may already exist. Try again!"
//         });

//     };

// }]);