'use strict';

angular.module('noviga')
  .controller('ChassisController', ['$scope', '$modal', 'resolvedAjaxItems', 'Chassis', '$filter',
    function ($scope, $modal, resolvedAjaxItems, Chassis, $filter) {

      console.log(resolvedAjaxItems);
      $scope.Chasss = resolvedAjaxItems;

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.Chass = $filter('filter')($scope.Chasss, {id:id})[0];
        $scope.open(id);
      };

      $scope.delete = function (id) {
        Chassis.delete({id: id},
          function () {
            var arr = $scope.Chasss.map(function(e) {return e.id}).indexOf(id);
            $scope.Chasss.splice(arr,1);
          });
      };

      $scope.save = function (id) {
        if (id) {
          Chassis.update({id: id}, $scope.Chass, function (data) {
            console.log(data);
            var chas = {};
            angular.forEach(data, function(value,key) {
              if(key !== '$promise' && key !== '$resolved') {
                chas[key] = value;
              };
            });
            var arr = $scope.Chasss.map(function(e) {return e.id}).indexOf(id);
            $scope.Chasss[arr] = chas;
            $scope.clear();
          });
        } else {
          Chassis.save($scope.Chass, function (data) {
            console.log(data);
            var chas = {};
            angular.forEach(data, function(value,key) {
              if(key !== '$promise' && key !== '$resolved') {
                chas[key] = value;
              };
            });
            $scope.Chasss[$scope.Chasss.length] = chas;
            $scope.clear();
          });
        }
      };

      $scope.clear = function () {
        $scope.Chass = {
          
          "modelNo": "",
          
          "maxSlots": "",
          
          "connectionType": "",

          "daqmxDeviceId": "",
          
          "id": ""
        };
      };

      $scope.open = function (id) {
        var ChassisSave = $modal.open({
          templateUrl: 'Chassis-save.html',
          controller: 'ChassisSaveController',
          size: 'sm',
          windowClass: 'my-modal-popup',
          resolve: {
            hassis: function () {
              return $scope.Chass;
            }
          }
        });

        ChassisSave.result.then(function (entity) {
          $scope.Chass = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('ChassisSaveController', ['$scope', '$modalInstance', 'hassis',
    function ($scope, $modalInstance, hassis) {
      $scope.Chass = hassis;

      

      $scope.ok = function () {
        $modalInstance.close($scope.Chass);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
