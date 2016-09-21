'use strict';

angular.module('noviga')
  .controller('BusinessController', ['$filter', '$scope', '$modal', 'resolvedAjaxItems', 'Business',
    function ($filter, $scope, $modal, resolvedAjaxItems, Business) {

      console.log(resolvedAjaxItems);
      // $scope.businesses = [];
      // angular.forEach(resolvedAjaxItems, function(value,key) {
      //   if (key !== '$promise' && key !== '$resolved') {
      //     var business = {};
      //     angular.forEach(value, function(v,k) {
      //       business[k] = v;
      //     });
      //     $scope.businesses[key] = business;
      //   };
      // });
      // console.log($scope.businesses);
      $scope.businesses = resolvedAjaxItems;

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.business = $filter('filter')($scope.businesses, {id: id})[0];
        console.log($scope.business);
        $scope.open(id);
      };

      $scope.delete = function (id) {
        Business.delete({id: id},
          function () {
            var ar = $scope.businesses.map(function(e) {return e.id}).indexOf(id);
            $scope.businesses.splice(ar,1);
          });
      };

      $scope.save = function (id) {
        if (id) {
          Business.update({id: id}, $scope.business, function (data) {
            console.log(data);
            var biness = {};
            angular.forEach(data, function(value,key) {
              if (key !== '$promise' && key !== '$resolved') {
                biness[key] = value;
              }
            });
            var ar = $scope.businesses.map(function(e) {return e.id}).indexOf(id);
            $scope.businesses[ar] = biness;
            $scope.clear();
          });
        } else {
          Business.save($scope.business, function (data) {
            console.log(data);
            var biness = {};
            angular.forEach(data, function(value,key) {
              if (key !== '$promise' && key !== '$resolved') {
                biness[key] = value;
              }
            });
            $scope.businesses[$scope.businesses.length] = biness;
            $scope.clear();
          });
        }
      };

      $scope.clear = function () {
        $scope.business = {
          
          "name": "",
          
          "id": "",

          "allowedRunProjects": "",

          "allowedUsers": "",
        };
      };

      $scope.open = function (id) {
        var businessSave = $modal.open({
          templateUrl: 'business-save.html',
          controller: 'BusinessSaveController',
          size: 'sm',
          windowClass: 'my-modal-popup',
          resolve: {
            business: function () {
              return $scope.business;
            }
          }
        });

        businessSave.result.then(function (entity) {
          $scope.business = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('BusinessSaveController', ['$scope', '$modalInstance', 'business',
    function ($scope, $modalInstance, business) {
      $scope.business = business;

      

      $scope.ok = function () {
        $modalInstance.close($scope.business);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
