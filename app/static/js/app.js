// Declare app level module which depends on filters, and services
angular.module('noviga', ['ngResource', 'ngRoute', 'ui.bootstrap', 'ui.date'])
.config(['$routeProvider', function ($routeProvider) {
  $routeProvider
  .when('/', {
    templateUrl: '/static/views/project/projects.html',
        controller: 'ProjectController',
        resolve:{
          resolvedAjaxItems: ['$q', '$rootScope', 'onegetProject', 'onegetbinessProject', 'AuthService', 'Business',
          function ($q, $rootScope, onegetProject, onegetbinessProject, AuthService, Business) {
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
                return deferred.reject({authenticated: 'notLoggedIn'});
              }
            )
          return deferred.promise;}]
          // resolvedProject: ['$q', 'Project','binessProject', 'AuthService',
          // function ($q, Project, binessProject, AuthService) {
          //   return AuthService.getStatus()
          //   .then(function() {
          //       if (AuthService.isLoggedIn()) {
          //         return AuthService.getUser()
          //           .then(function(data) {
          //             if (data.role === 'Admin') {
          //               return $q.when(Project.query());
          //             } else {
          //               return $q.when(binessProject.query({businessId: data.businessId}));
          //             }
          //           });
          //       } else {
          //         return $q.reject({authenticated: "notLoggedIn"});
          //       }
          //     }
          //   )
          // }],
          // resolvedHwsetups:['$q', 'HardwareSetup', 'binessHwsetup', 'AuthService',
          // function ($q, HardwareSetup, binessHwsetup, AuthService) {
          //   return AuthService.getStatus()
          //   .then(function() {
          //       if (AuthService.isLoggedIn()) {
          //         return AuthService.getUser()
          //           .then(function(data) {
          //             if (data.role === 'Admin') {
          //               return $q.when(HardwareSetup.query());
          //             } else {
          //               return $q.when(binessHwsetup.query({businessId: data.businessId}));
          //             }
          //           });
          //       } else {
          //         return $q.reject({authenticated: "notLoggedIn"});
          //       }
          //     }
          //   )
          // }],
          // resolvedUserBiness:['$q','Business','AuthService', function ($q,Business,AuthService) {
          //   return AuthService.getStatus()
          //   .then(function() {
          //       if (AuthService.isLoggedIn()) {
          //         return AuthService.getUser()
          //           .then(function(data) {
          //             if (data.role === 'Admin') {
          //               return $q.when(Business.query());
          //             } else {
          //               return $q.when(Business.get({id: data.businessId}));
          //             }
          //           });
          //       } else {
          //         return $q.reject({authenticated: "notLoggedIn"});
          //       }
          //     }
          //   )
          // }]
        }
      }) 
  .otherwise({redirectTo: '/'});
}]);

angular.module('noviga').run(function ($rootScope, $location, $route, AuthService) {
  $rootScope.$on('$routeChangeStart', function (event, next, current) {
    console.log("hello");
  });
});

angular.module('noviga')
  .run(["$rootScope", "$location", "AuthService", function($rootScope, $location, AuthService) {
    $rootScope.$on("$routeChangeError", function(event, current, previous, eventObj) {
      if (eventObj.authenticated === "notLoggedIn") {
        console.log("notLoggedIn");
        $location.path("/login");
      } else if (eventObj.authenticated === "unauthorized") {
        console.log("unauthorized");
        AuthService.logout()
        .then(function(){
          $location.path("/login");
        })
      }
    })
}]);

angular.module('noviga')
.controller('navbarController', ['$rootScope', '$location', '$scope', 'AuthService', 'indexnavside',
  function ($rootScope, $location, $scope, AuthService, indexnavside) {

    $scope.navbarshow=false;
    
    $rootScope.$on("login", function() {
      $scope.activeMenu = 'eolQC';
      console.log("loggedInJustNowNav");
    })

    $rootScope.$on("$routeChangeSuccess", function(event, current, previous) {
      console.log(event);
      console.log(current);
      console.log(previous);
      console.log("welcome");
      if (AuthService.isLoggedIn()) {
        console.log("hi");
        $scope.navbarshow = true;
        $scope.adminshow = false;
        $scope.managershow = false;
        
        indexnavside.get('sidebar').showtrue();
        
        var browserUrlLocation = $location.path();
        var slashindex = [];
        angular.forEach(browserUrlLocation, function(value, key) {
          if (value === '/') {slashindex.push(key);}
        });
        var navbarsel = browserUrlLocation.slice(slashindex[0]+1,slashindex[1]);
        var sidebarsel = '#' + browserUrlLocation;
        console.log([navbarsel, sidebarsel]);
        switch(navbarsel) {
          case 'admincontrol':
            $scope.activeMenu = 'adminControl';
            indexnavside.get('sidebar').setsidebarItems('adminControl');
            angular.forEach(indexnavside.get('sidebar').sidebarItems, function (value, key) {
              if (value.href === sidebarsel) {
                indexnavside.get('sidebar').activeItem['adminControl'].text = value.text;
                indexnavside.get('sidebar').activeItem['adminControl'].href = value.href;
              }
            });
            break;
          case 'eolQC':
            $scope.activeMenu = 'eolQC';
            indexnavside.get('sidebar').setsidebarItems('eolQC');
            angular.forEach(indexnavside.get('sidebar').sidebarItems, function (value, key) {
              if (value.href === sidebarsel) {
                indexnavside.get('sidebar').activeItem['eolQC'].text = value.text;
                indexnavside.get('sidebar').activeItem['eolQC'].href = value.href; 
              }
            })
            break;
          case 'managercontrol':
            $scope.activeMenu = 'managerControl';
            indexnavside.get('sidebar').setsidebarItems('managerControl');
            angular.forEach(indexnavside.get('sidebar').sidebarItems, function (value, key) {
              if (value.href === sidebarsel) {
                indexnavside.get('sidebar').activeItem['managerControl'].text = value.text;
                indexnavside.get('sidebar').activeItem['managerControl'].href = value.href; 
              }
            })
            break;
          case 'postanalysis':
            $scope.activeMenu = 'postAnalysis';
            indexnavside.get('sidebar').setsidebarItems('postAnalysis');
            angular.forEach(indexnavside.get('sidebar').sidebarItems, function (value, key) {
              if (key.value === sidebarsel) {
                indexnavside.get('sidebar').activeItem['postAnalysis'].text = value.text;
                indexnavside.get('sidebar').activeItem['postAnalysis'].href = value.href; 
              }
            })
            break;
          case 'statistics':
            $scope.activeMenu = 'statistics';
            indexnavside.get('sidebar').setsidebarItems('statistics');
            angular.forEach(indexnavside.get('sidebar').sidebarItems, function (value, key) {
              if (key.value === sidebarsel) {
                indexnavside.get('sidebar').activeItem['statistics'].text = value.text;
                indexnavside.get('sidebar').activeItem['statistics'].href = value.href; 
              }
            })
            break;
        };

        // AuthService.getUser()
        // .then(function(data) {
          // console.log(data);
          $scope.username = $rootScope.loggedInUser.name;
          console.log($rootScope.loggedInUser);
          $scope.setActiveView = function(navbarItem) {
            return indexnavside.get('sidebar').activeItem[navbarItem].href;
          }
          // console.log(indexnavside.get('sidebar').activeItem[navbarItem].href);
          if ($rootScope.loggedInUser.role === 'Admin') {
            $scope.adminshow = true;
            console.log(true);
            $scope.managershow = true;
          } else if ($rootScope.loggedInUser.role === 'Manager') {
            $scope.managershow = true;
          } else {};
        // })
      } else {
        $scope.navbarshow = false;
        indexnavside.get('sidebar').showfalse();
      }
    });

    indexnavside.store('navbar', $scope);

    // $scope.setActiveView = function(navbarItem) {
    //   console.log(indexnavside.get('sidebar').activeItem[navbarItem].href);
    //   return indexnavside.get('sidebar').activeItem[navbarItem].href;
    // }

    $scope.activeMenu = 'eolQC';
    $scope.setActiveMenu = function(navbarItem) {
      $scope.activeMenu = navbarItem;
      indexnavside.get('sidebar').setsidebarItems(navbarItem);
    }

    $scope.logout = function () {

      // call login from service
      AuthService.logout()
        // handle success
        .then(function () {
          $location.path('/login');
        })
        // handle error
        .catch(function () {
          $location.path('/loggedOut');
        });
    };
}]);

angular.module('noviga')
.controller('sidebarController', ['$rootScope','$location', '$scope', 'indexnavside',
  function ($rootScope, $location, $scope,indexnavside) {

    indexnavside.store('sidebar', $scope);
    // $scope.sidebarshowvar = 

    $scope.sidebarshow = false;
    $scope.showtrue = function() {
      $scope.sidebarshow = true;
    }

    $scope.showfalse = function() {
      $scope.sidebarshow = false;
    }
    
    $scope.sidebarItems = [
            {text: 'Projects',
            href: '#/eolQC/projects'},
            {text: 'Hardwares',
            href: '#/eolQC/hardwares'},
            {text: 'Channels',
            href: '#/eolQC/channels'},
            {text: 'DSPs',
            href: '#/eolQC/dsps'},
            {text: 'Reports',
            href: '#/eolQC/reports'},
            {text: 'Utilities',
            href: '#/eolQC/utilities'}
          ];
    $scope.setsidebarItems = function(navbarItem) {
      switch (navbarItem) {
        case "eolQC":
          $scope.sidebarItems = [
            {text: 'Projects',
            href: '#/eolQC/projects'},
            {text: 'Hardwares',
            href: '#/eolQC/hardwares'},
            {text: 'Channels',
            href: '#/eolQC/channels'},
            {text: 'DSPs',
            href: '#/eolQC/dsps'},
            {text: 'Reports',
            href: '#/eolQC/reports'},
            {text: 'Utilities',
            href: '#/eolQC/utilities'}
          ];
          break;
        case "postAnalysis":
          $scope.sidebarItems = [
            {text: 'A',
            href: '#/postanalysis/abcde'},
            {text: 'B',
            href: '#/postanalysis/bcdea'},
            {text: 'C',
            href: '#/postanalysis/cdeab'},
            {text: 'D',
            href: '#/postanalysis/deabc'},
            {text: 'E',
            href: '#/postanalysis/eabcd'},
          ];
          break;
        case "statistics":
          $scope.sidebarItems = [
            {text: 'F',
            href: '#/statistics/fghij'},
            {text: 'G',
            href: '#/statistics/ghijf'},
            {text: 'H',
            href: '#/statistics/hijfg'},
            {text: 'I',
            href: '#/statistics/ijfgh'},
            {text: 'J',
            href: '#/statistics/jfghi'},
          ];
          break;
        case "managerControl":
          $scope.sidebarItems = [
            {text: 'Users',
            href: '#/managercontrol/users'},
            {text: 'Licenses',
            href: '#/managercontrol/licenses'}
          ];
          break;
        case "adminControl":
          $scope.sidebarItems = [
            {text: 'Businesses',
            href: '#/admincontrol/businesses'},
            {text: 'Users',
            href: '#/admincontrol/users'},
            {text: 'Business Devices',
            href: '#/admincontrol/devices'},
            {text: 'Rabbit Queues',
            href: '#/admincontrol/queues'},
            {text: 'Chassis',
            href: '#/admincontrol/chassis'},
            {text: 'Modules',
            href: '#/admincontrol/modules'},
            {text: 'Quantities',
            href: '#/admincontrol/quantities'},
            {text: 'Units',
            href: '#/admincontrol/units'}
          ];
          break;
        case "referenceDocuments":
          $scope.sidebarItems = [
            {text: 'U',
            href: '#/referencedocuments/uvwxy'},
            {text: 'V',
            href: '#/referencedocuments/vwxyu'},
            {text: 'W',
            href: '#/referencedocuments/wxyuv'},
          ];
          break;
      }
    }    

    $scope.activeItem = {
      eolQC : {text: 'Projects',
            href: '#/eolQC/projects'},
      postAnalysis : {text: 'A',
            href: '#/postanalysis/abcde'},
      statistics : {text: 'F',
            href: '#/statistics/fghij'},
      managerControl : {text: 'Users',
            href: '#/managercontrol/users'},
      adminControl : {text: 'Businesses',
            href: '#/admincontrol/businesses'},
      referenceDocuments : {text: 'U',
            href: '#/referencedocuments/uvwxy'},
    };

    $rootScope.$on("login", function() {
      $scope.activeItem = {
        eolQC : {text: 'Projects',
            href: '#/eolQC/projects'},
        postAnalysis : {text: 'A',
            href: '#/postanalysis/abcde'},
        statistics : {text: 'F',
            href: '#/statistics/fghij'},
        managerControl : {text: 'Users',
            href: '#/managercontrol/users'},
        adminControl : {text: 'Businesses',
            href: '#/admincontrol/businesses'},
        referenceDocuments : {text: 'U',
            href: '#/referencedocuments/uvwxy'},
      };
      console.log("loggedInJustNowSide");
    })

    $scope.getActiveItemText = function() {
      var navItem = indexnavside.get('navbar').activeMenu; 
      // console.log($scope.activeItem[navItem].text)
      return $scope.activeItem[navItem].text;
    }
    $scope.setActive = function(sidebarItem) {
      var navItem = indexnavside.get('navbar').activeMenu;
      $scope.activeItem[navItem].text = sidebarItem.text;
      $scope.activeItem[navItem].href = sidebarItem.href;
    }
}]);

angular.module('noviga')
.factory('indexnavside', function ($rootScope) {
    
    var mem = {};
    return {
        store: function (key, value) {
            $rootScope.$emit('navside.stored', key);
            mem[key] = value;
        },
        get: function (key) {
            return mem[key];
        }
    };
});