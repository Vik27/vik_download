'use strict';

angular.module('noviga')
  .controller('HwchassismapController', ['$scope', '$modal', 'Hwchassismap', 'Chassis','Module',
    function ($scope, $modal, Hwchassismap,Chassis,Module) {

      $scope.hwchassismaps = Hwchassismap.query();
      $scope.chassises = Chassis.query();
      $scope.mods = Module.query();
      $scope.abc1 ="test" /*$scope.hardwaresetups[0].name;*/
      $scope.hwcmyselect = function(chass1) {
        $scope.abc1 = chass1.modelNo;
      };
      $scope.abc2 ="test" /*$scope.hardwaresetups[0].name;*/
      $scope.hwc2myselect = function(mod) {
        $scope.abc2 = mod.modelNo;
      };

      $scope.hwccreate = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.hwchassismap = Hwchassismap.get({id: id});
        $scope.open(id);
      };

      $scope.delete = function (id) {
        Hwchassismap.delete({id: id},
          function () {
            $scope.hwchassismaps = Hwchassismap.query();
          });
      };

      $scope.save = function (id) {
        if (id) {
          Hwchassismap.update({id: id}, $scope.hwchassismap,
            function () {
              $scope.hwchassismaps = Hwchassismap.query();
              $scope.clear();
            });
        } else {
          Hwchassismap.save($scope.hwchassismap,
            function () {
              $scope.hwchassismaps = Hwchassismap.query();
              $scope.clear();
            });
        }
      };

      $scope.clear = function () {
        $scope.hwchassismap = {
          
          "slotnumber": "",
          
          "id": ""
        };
      };

      $scope.open = function (id) {
        var hwchassismapSave = $modal.open({
          templateUrl: 'hwchassismap-save.html',
          controller: 'HwchassismapSaveController',
          size:'sm',
          windowClass: 'my-modal-popup',
          resolve: {
            hwchassismap: function () {
              return $scope.hwchassismap;
            }
          }
        });

        hwchassismapSave.result.then(function (entity) {
          $scope.hwchassismap = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('HwchassismapSaveController', ['$scope', '$modalInstance', 'hwchassismap',
    function ($scope, $modalInstance, hwchassismap) {
      $scope.hwchassismap = hwchassismap;

      

      $scope.ok = function () {
        $modalInstance.close($scope.hwchassismap);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
