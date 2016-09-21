'use strict';

angular.module('noviga')
  .controller('DevicetableController', ['$scope', '$modal', 'Devicetable', 'resolvedAjaxItems', '$filter',
    function ($scope, $modal, Devicetable, resolvedAjaxItems, $filter) {


      console.log(resolvedAjaxItems);
      $scope.alldevicetables = resolvedAjaxItems.devices;
      $scope.businesses = resolvedAjaxItems.businesses;
      $scope.chassises = resolvedAjaxItems.chassises,
      $scope.queues = resolvedAjaxItems.queues;
      $scope.activebinessname = 'All';

      $scope.devicetables = $scope.alldevicetables;
      $scope.setActiveBiness = function(business) {
        if (business === 'all') {
          $scope.activebinessname = 'All';
          $scope.devicetables = $scope.alldevicetables;
        } else {
          $scope.activebinessname = business.name;
          $scope.activebinessid = business.id;
          $scope.devicetables = $filter('filter')($scope.alldevicetables, {businessId: business.id});
        }
      };

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.devicetable = $filter('filter')($scope.alldevicetables, {id: id})[0];
        $scope.open(id);
      };

      $scope.delete = function (id) {
        Devicetable.delete({id: id},
          function () {
            var arr = $scope.alldevicetables.map(function(e) {return e.id}).indexOf(id);
            $scope.alldevicetables.splice(arr, 1);
            if ($scope.activebinessname !== 'All') {
              $scope.devicetables = $filter('filter')($scope.alldevicetables, {businessId: $scope.activebinessid});
            } else {
              $scope.devicetables = $scope.alldevicetables;
            };
        });
      };

      $scope.save = function (id) {
        if (id) {
          Devicetable.update({id: id}, $scope.devicetable, function (data) {
            console.log(data);
            var devc = {};
            angular.forEach(data, function(value,key) {
              if(key !== '$promise' && key !== '$resolved') {
                devc[key] = value;
              };
            });
            var ar = $scope.alldevicetables.map(function(e) {return e.id}).indexOf(id);
            $scope.alldevicetables[ar] = devc;

            if ($scope.activebinessname !== 'All') {
              $scope.devicetables = $filter('filter')($scope.alldevicetables, {businessId: $scope.activebinessid});
            } else {
              $scope.devicetables = $scope.alldevicetables;
            }
            
            $scope.clear();
          });
        } else {
          Devicetable.save($scope.devicetable, function (data) {
            console.log(data);
            var devc = {};
            angular.forEach(data, function(value,key) {
              if(key !== '$promise' && key !== '$resolved') {
                devc[key] = value;
              };
            });
            $scope.alldevicetables[$scope.alldevicetables.length] = devc;

            if ($scope.activebinessname !== 'All') {
              $scope.devicetables = $filter('filter')($scope.alldevicetables, {businessId: $scope.activebinessid});
            } else {
              $scope.devicetables = $scope.alldevicetables;
            }
            
            $scope.clear();
          });
        }
      };

      $scope.clear = function () {
        $scope.devicetable = {
          
          "firmwarename": "",
          
          "queueId": $scope.queues[0].id,
          
          "niChassisId": "",

          "businessId": "",
        };
      };

      $scope.open = function (id) {
        var devicetableSave = $modal.open({
          templateUrl: 'devicetable-save.html',
          controller: 'DevicetableSaveController',
          size: 'sm',
          windowClass: 'my-modal-popup',
          resolve: {
            devicetable: function () {
              return $scope.devicetable;
            },
            businesses: function() {
              return $scope.businesses;
            },
            chassises: function() {
              return $scope.chassises;
            },
            queues: function() {
              return $scope.queues;
            }
          }
        });

        devicetableSave.result.then(function (entity) {
          $scope.devicetable = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('DevicetableSaveController', ['$scope', '$modalInstance', 'devicetable', 'businesses', 'chassises',  'queues',
    function ($scope, $modalInstance, devicetable, businesses, chassises, queues) {
      $scope.devicetable = devicetable;
      $scope.businesses = businesses;
      $scope.chassises = chassises;
      $scope.queues = queues;
      

      $scope.ok = function () {
        $modalInstance.close($scope.devicetable);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
