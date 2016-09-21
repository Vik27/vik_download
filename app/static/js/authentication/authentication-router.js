
angular.module('noviga')
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/login', {
        templateUrl: 'static/views/authentication/login.html',
        controller: 'loginController',
        access1: {restricted: false}
      })
      // .when('/logout', {
      //   controller: 'logoutController',
      //   access1: {restricted: true}
      // })
      .when('/register1', {
        templateUrl: 'static/views/authentication/register.html',
        controller: 'registerController',
        access1: {restricted: false}
      })
      .when('/loggedOut', {
        template: "<h1> You are logged out in Angular but not in Flask </h1>",
        access1: {restricted: true}
    })
      .when('/dummy', {
        template: "<h1> You are dumb and you are viewing dummy </h1>",
        access1: {restricted: true}
      })
    }]);