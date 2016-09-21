'use strict';

angular.module('noviga')
  .controller('HwchaschanmapController', ['$scope', '$modal', 'resolvedHwchaschanmap', 'Hwchaschanmap',
    function ($scope, $modal, resolvedHwchaschanmap, Hwchaschanmap) {

      $scope.hwchaschanmaps = resolvedHwchaschanmap;

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.hwchaschanmap = Hwchaschanmap.get({id: id});
        $scope.open(id);
      };

      $scope.delete = function (id) {
        Hwchaschanmap.delete({id: id},
          function () {
            $scope.hwchaschanmaps = Hwchaschanmap.query();
          });
      };

      $scope.save = function (id) {
        if (id) {
          Hwchaschanmap.update({id: id}, $scope.hwchaschanmap,
            function () {
              $scope.hwchaschanmaps = Hwchaschanmap.query();
              $scope.clear();
            });
        } else {
          Hwchaschanmap.save($scope.hwchaschanmap,
            function () {
              $scope.hwchaschanmaps = Hwchaschanmap.query();
              $scope.clear();
            });
        }
      };

      $scope.clear = function () {
        $scope.hwchaschanmap = {
          
          "channelnumber": "",
          
          "trigger": "",
          
          "id": ""
        };
      };

      $scope.open = function (id) {
        var hwchaschanmapSave = $modal.open({
          templateUrl: 'hwchaschanmap-save.html',
          controller: 'HwchaschanmapSaveController',
          resolve: {
            hwchaschanmap: function () {
              return $scope.hwchaschanmap;
            }
          }
        });

        hwchaschanmapSave.result.then(function (entity) {
          $scope.hwchaschanmap = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('HwchaschanmapSaveController', ['$scope', '$modalInstance', 'hwchaschanmap',
    function ($scope, $modalInstance, hwchaschanmap) {
      $scope.hwchaschanmap = hwchaschanmap;

      

      $scope.ok = function () {
        $modalInstance.close($scope.hwchaschanmap);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
