angular.module('noviga').factory('AuthService',
  ['$q', '$timeout', '$http', '$rootScope',
  function ($q, $timeout, $http, $rootScope) {

    // create user variable
    var user = null;
    $rootScope.loggedInUser = null;

    return ({
      isLoggedIn: isLoggedIn,
      login: login,
      logout: logout,
      getUser: getUser,
      getStatus: getStatus,
      // checkUser:checkUser,
    });


    function login(username, password) {

    // create a new instance of deferred
    var deferred = $q.defer();

    // send a post request to the server
    $http.post('/noviga/login', {username: username, password: password})
    // handle success
    .success(function (data, status) {
      if(status === 200 && data.result){
        user = true;
        deferred.resolve(data);
      } else {
        user = false;
        deferred.reject();
      }
    })
    // handle error
    .error(function (data) {
      user = false;
      deferred.reject();
    });

    // return promise object
    return deferred.promise;
  };

  function logout() {

    var deferred = $q.defer();

    $http.get('/noviga/logout')
    .success(function(data){
      if (data.result) {
        console.log(data.result);
        user = false;
        deferred.resolve();
      }
    })
    .error(function(){
      user = false;
      deferred.reject();
    })

    return deferred.promise;
  };

  function getStatus() {

   var deferred = $q.defer();

   $http.get('/noviga/getStatus')
   .success(function (data) {
    if (data.status) {
      user = true;
      console.log('world')
      deferred.resolve();
    } else {
      user = false;
      console.log('round')
      deferred.resolve();
    }
   })
   .error(function (data) {
    user = false;
    deferred.reject();
   })

   return deferred.promise;
  };


  function getUser() {

    var deferred = $q.defer();
    $http.get('/noviga/getUser')
    .success(
      function (response) {
        if(response !== 'null') {
          user = true;
          deferred.resolve(response);
        } else {
          user = false;
          deferred.resolve(response);
        }
      }
    )
    .error(
      function (errResponse) {
        console.error('Error while fetching current user');
        deferred.reject(errResponse);
      }
    );
    return deferred.promise;
  };


  function isLoggedIn() {

    if (user) {
      console.log('what')
      return true;
    } else {
      console.log('where')
      return false;
    }
  };

  // function getone() {
  //   return $http.get('/noviga/users/1')
  //   .then(function (response) {
  //     return response.data;
  //   },
  //   function (errResponse) {
  //     console.error('Error while fetching current user');
  //       return $q.reject(errResponse);
  //   })
  // };

  // function checkUser() {
  //   var deferred = $q.defer();

  //  $http.post('/noviga/checkUser', {'name': loggenInUser.name})
  //  .success(function (data) {
  //   if (data.status) {
  //     user = true;
  //     console.log('world')
  //     deferred.resolve();
  //   } else {
  //     user = false;
  //     console.log('round')
  //     deferred.resolve();
  //   }
  //  })
  //  .error(function (data) {
  //   user = false;
  //   deferred.reject();
  //  })

  //  return deferred.promise;
  // };

}]);