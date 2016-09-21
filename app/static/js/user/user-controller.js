'use strict';

angular.module('noviga')
  .controller('UserController', ['$scope', '$modal', 'User', 'resolvedAjaxItems', '$timeout', '$filter',
    function ($scope, $modal, User, resolvedAjaxItems, $timeout, $filter) {

      console.log(resolvedAjaxItems.users);
      console.log(resolvedAjaxItems.businesses);
      $scope.error = false;
      $scope.allusers = resolvedAjaxItems.users;
      $scope.businesses = resolvedAjaxItems.businesses;
      $scope.activebinessname = 'All';

      $scope.users = $scope.allusers;
      $scope.setActiveBiness = function(business) {
        if (business === 'all') {
          $scope.activebinessname = 'All';
          $scope.users = $scope.allusers;
        } else {
          $scope.activebinessname = business.name;
          $scope.activebinessid = business.id
          $scope.users = $filter('filter')($scope.allusers, {businessId: business.id});
        }
      };

      $scope.create = function () {
        $scope.error=false;
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.error =false;
        $scope.user = $filter('filter')($scope.allusers, {id: id})[0];;
        console.log($scope.user);
        $scope.open(id);
      };

      $scope.delete = function (id) {
        User.delete({id: id},
          function () {
            var ar = $scope.allusers.map(function(e) {return e.id}).indexOf(id);
            $scope.allusers.splice(ar,1);
            if ($scope.activebinessname !== 'All') {
              $scope.users = $filter('filter')($scope.allusers, {businessId: $scope.activebinessid});
            } else {
              $scope.users = $scope.allusers;
            }
          });
      };

      $scope.save = function (id) {
        if (id) {
          User.update({id: id}, $scope.user, function (data) {
            console.log(data);
            var usr = {};
            angular.forEach(data, function(value,key) {
              if(key !== '$promise' && key !== '$resolved') {
                usr[key] = value;
              };
            });
            var ar = $scope.allusers.map(function(e) {return e.id}).indexOf(id);
            $scope.allusers[ar] = usr;

            if ($scope.activebinessname !== 'All') {
              $scope.users = $filter('filter')($scope.allusers, {businessId: $scope.activebinessid});
            } else {
              $scope.users = $scope.allusers;
            }
            
            $scope.clear();
          },
          function (response) {
            console.log(response.data.message);
            $scope.error = true;
            $scope.errorMessage = response.data.message;
            $scope.users = User.query();
            $timeout(function () {
              $scope.error = false;
            },3000);
          });
        } else {
          User.save($scope.user, function (data) {
            console.log(data);
            var usr = {};
            angular.forEach(data, function(value,key) {
              if(key !== '$promise' && key !== '$resolved') {
                usr[key] = value;
              };
            });
            $scope.allusers[$scope.allusers.length] = usr;

            if ($scope.activebinessname !== 'All') {
              $scope.users = $filter('filter')($scope.allusers, {businessId: $scope.activebinessid});
            } else {
              $scope.users = $scope.allusers;
            }

            $scope.clear();
          },
          function (response) {
            console.log(response.data.message);
            $scope.error = true;
            $scope.errorMessage = response.data.message;
            $timeout(function () {
              $scope.error = false;
            },3000);
          });
        }
      };

      $scope.clear = function () {
        $scope.user = {
          
          "username": "",
          
          "password": "",
          
          "contact_email": "",

          "role": "",
          
          "id": "",

          "businessId": "",
        };
      };

      $scope.open = function (id) {
        var userSave = $modal.open({
          templateUrl: 'user-save.html',
          controller: 'UserSaveController',
          size: 'sm',
          windowClass: 'my-modal-popup',
          resolve: {
            user: function () {
              return $scope.user;
            },
            businesses: function() {
              return $scope.businesses;
            }
          }
        });

        userSave.result.then(function (entity) {
          $scope.user = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('UserSaveController', ['$scope', '$modalInstance', 'user', 'businesses',
    function ($scope, $modalInstance, user, businesses) {
      $scope.user = user;
      $scope.businesses = businesses;
      

      $scope.ok = function () {
        $modalInstance.close($scope.user);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
