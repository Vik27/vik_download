'use strict';

angular.module('noviga')
  .controller('QuantityController', ['$scope', '$modal', 'resolvedAjaxItems', 'Quantity', '$filter',
    function ($scope, $modal, resolvedAjaxItems, Quantity, $filter) {

      console.log(resolvedAjaxItems);
      $scope.quantities = resolvedAjaxItems.quantities;
      $scope.units = resolvedAjaxItems.units;

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.quantity = $filter('filter')($scope.quantities, {id:id})[0];
        $scope.open(id);
      };

      $scope.delete = function (id) {
        Quantity.delete({id: id},
          function () {
            var arr = $scope.quantities.map(function(e) {return e.id}).indexOf(id);
            $scope.quantities.splice(arr,1);
          });
      };

      $scope.save = function (id) {
        if (id) {
          console.log($scope.quantity);
          $scope.quantity.units = $scope.quantity.units.map(function(e) {
            if (e.id) {
              return e.id;
            } else {
              return e;
            }
          });
          Quantity.update({id: id}, $scope.quantity, function (data) {
            console.log(data);
            var quant = {};
            angular.forEach(data, function(value,key) {
              if(key !== '$promise' && key !== '$resolved') {
                quant[key] = value;
              };
            });
            var arr = $scope.quantities.map(function(e) {return e.id}).indexOf(id);
            $scope.quantities[arr] = quant;
            $scope.clear()
          });
        } else {
          console.log($scope.quantity);
          Quantity.save($scope.quantity, function (data) {
            console.log(data);
            var quant = {};
            angular.forEach(data, function(value,key) {
              if(key !== '$promise' && key !== '$resolved') {
                quant[key] = value;
              };
            });
            $scope.quantities[$scope.quantities.length] = quant;
            $scope.clear();
          });
        }
      };

      $scope.clear = function () {
        $scope.quantity = {
          
          "name": "",
          
          "id": "",

          "units": ""
        };
      };

      $scope.open = function (id) {
        var quantitySave = $modal.open({
          templateUrl: 'quantity-save.html',
          controller: 'QuantitySaveController',
          size: 'sm',
          windowClass: 'my-modal-popup',
          resolve: {
            quantity: function () {
              return $scope.quantity;
            },
            units: function() {
              return $scope.units;
            }
          }
        });

        quantitySave.result.then(function (entity) {
          $scope.quantity = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('QuantitySaveController', ['$scope', '$modalInstance', 'quantity', 'units',
    function ($scope, $modalInstance, quantity, units) {
      $scope.quantity = quantity;
      $scope.units = units;
      
      $scope.mapps = function(unitId) {
        if ($scope.quantity.units != "") {
          var tr = $scope.quantity.units.map(function(e) {return e.id}).indexOf(unitId)
          if (tr === -1) {
            return false;
          } else {
            return true;
          }
        }
      }

      $scope.ok = function () {
        $modalInstance.close($scope.quantity);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
