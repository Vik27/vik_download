angular.module('noviga')
  .controller('homeController', ['$scope', 'resolvedHome', 'User', 'AuthService', '$window', '$q',
    function ($scope, resolvedHome, User, AuthService, $window, $q) {
    	console.log('Y')
    	$scope.message = resolvedHome

    	$scope.user1 = function() {
    		var us = $q.when(User.get({id:1}));
    		console.log(us);
    		$window.alert(us.username);
    	}

    	$scope.user2 = function() {
    		var us = AuthService.getone();
    		console.log(us);
    		$window.alert(us.username);
    	}
    }])
