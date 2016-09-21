'use strict';

angular.module('noviga')
  .controller('ModuleController', ['$scope', '$modal', 'resolvedAjaxItems', 'Module', '$filter',
    function ($scope, $modal, resolvedAjaxItems, Module, $filter) {

      console.log(resolvedAjaxItems);
      $scope.modules = resolvedAjaxItems.modules;
      $scope.quantities = resolvedAjaxItems.quantities;

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.module = $filter('filter')($scope.modules, {id:id})[0];
        console.log($scope.module);
        $scope.open(id);
      };

      $scope.delete = function (id) {
        Module.delete({id: id},
          function () {
            var arr = $scope.modules.map(function(e) {return e.id}).indexOf(id);
            $scope.modules.splice(arr,1);
          });
      };

      $scope.save = function (id) {
        if (id) {
          console.log($scope.module);
          $scope.module.quantities = $scope.module.quantities.map(function(e) {
            if (e.id) {
              return e.id;
            } else {
              return e;
            }
          });
          Module.update({id: id}, $scope.module, function (data) {
            console.log(data);
            var mod = {};
            angular.forEach(data, function(value,key) {
              if(key !== '$promise' && key !== '$resolved') {
                mod[key] = value;
              };
            });
            var arr = $scope.modules.map(function(e) {return e.id}).indexOf(id);
            $scope.modules[arr] = mod;
            $scope.clear();
          });
        } else {
          console.log($scope.module);
          Module.save($scope.module, function (data) {
            console.log(data);
            var mod = {};
            angular.forEach(data, function(value,key) {
              if(key !== '$promise' && key !== '$resolved') {
                mod[key] = value;
              };
            });
            $scope.modules[$scope.modules.length] = mod;
            $scope.clear();
          });
        }
      };

      $scope.clear = function () {
        $scope.module = {
          
          "modelNo": "",
          
          "maxChannels": "",
          
          "maxSamplingRate": "",
          
          "peakVoltRange": "",
          
          "type": "",
          
          "id": "",

          "quantities": "",

          "daqmxDeviceId": "",
        };
      };

      $scope.open = function (id) {
        var ModuleSave = $modal.open({
          templateUrl: 'Module-save.html',
          controller: 'ModuleSaveController',
          size: 'sm',
          windowClass: 'my-modal-popup',
          resolve: {
            module: function () {
              console.log($scope.module.quantities);
              return $scope.module;
            },
            quantities: function() {
              return $scope.quantities;
            }
          }
        });

        ModuleSave.result.then(function (entity) {
          $scope.module = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('ModuleSaveController', ['$scope', '$modalInstance', 'module', 'quantities',
    function ($scope, $modalInstance, module, quantities) {
      $scope.module = module;
      $scope.quantities = quantities;

      $scope.mapps = function(quantityId) {
        if ($scope.module.quantities !== "") {
          var tr = $scope.module.quantities.map(function(e) {return e.id}).indexOf(quantityId);
          if (tr === -1) {
            return false;
          } else {
            return true;
          }
        }
      }

      $scope.ok = function () {
        $modalInstance.close($scope.module);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
