'use strict';

angular.module('noviga')
  .controller('UnitController', ['$scope', '$modal', 'resolvedAjaxItems', 'Unit', '$filter',
    function ($scope, $modal, resolvedAjaxItems, Unit, $filter) {

      console.log(resolvedAjaxItems);
      $scope.units = resolvedAjaxItems;

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.unit = $filter('filter')($scope.units, {id:id})[0];
        $scope.open(id);
      };

      $scope.delete = function (id) {
        Unit.delete({id: id},
          function () {
            var arr = $scope.units.map(function(e) {return e.id}).indexOf(id);
            $scope.units.splice(arr,1);
          });
      };

      $scope.save = function (id) {
        if (id) {
          Unit.update({id: id}, $scope.unit, function (data) {
            console.log(data);
            var uni = {};
            angular.forEach(data, function(value,key) {
              if(key !== '$promise' && key !== '$resolved') {
                uni[key] = value;
              };
            });
            var arr = $scope.units.map(function(e) {return e.id}).indexOf(id);
            $scope.units[arr] = uni;
            $scope.clear();
          });
        } else {
          Unit.save($scope.unit, function (data) {
            console.log(data);
            var uni = {};
            angular.forEach(data, function(value,key) {
              if(key !== '$promise' && key !== '$resolved') {
                uni[key] = value;
              };
            });
            $scope.units[$scope.units.length] = uni;
            $scope.clear();
          });
        }
      };

      $scope.clear = function () {
        $scope.unit = {
          
          "name": "",
          
          "id": ""
        };
      };

      $scope.open = function (id) {
        var unitSave = $modal.open({
          templateUrl: 'unit-save.html',
          controller: 'UnitSaveController',
          size: 'sm',
          windowClass: 'my-modal-popup',
          resolve: {
            unit: function () {
              return $scope.unit;
            }
          }
        });

        unitSave.result.then(function (entity) {
          $scope.unit = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('UnitSaveController', ['$scope', '$modalInstance', 'unit',
    function ($scope, $modalInstance, unit) {
      $scope.unit = unit;

      

      $scope.ok = function () {
        $modalInstance.close($scope.unit);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
