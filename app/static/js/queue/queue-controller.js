'use strict';

angular.module('noviga')
  .controller('QueueController', ['$scope', '$modal', 'Queue', 'resolvedAjaxItems', '$filter',
    function ($scope, $modal, Queue, resolvedAjaxItems, $filter) {


      console.log(resolvedAjaxItems);
      $scope.businesses = resolvedAjaxItems.businesses;
      $scope.allqueues = resolvedAjaxItems.queues;
      $scope.activebinessname = 'All';

      $scope.queues = $scope.allqueues;
      $scope.setActiveBiness = function(business) {
        if (business === 'all') {
          $scope.activebinessname = 'All';
          $scope.queues = $scope.allqueues;
        } else {
          $scope.activebinessname = business.name;
          $scope.activebinessid = business.id;
          $scope.queues = $filter('filter')($scope.allqueues, {businessId: business.id});
        }
      };

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.queue = $filter('filter')($scope.allqueues, {id: id})[0];
        $scope.open(id);
      };

      $scope.delete = function (id) {
        Queue.delete({id: id},
          function () {
            var arr = $scope.allqueues.map(function(e) {return e.id}).indexOf(id);
            $scope.allqueues.splice(arr, 1);
            if ($scope.activebinessname !== 'All') {
              $scope.queues = $filter('filter')($scope.allqueues, {businessId: $scope.activebinessid});
            } else {
              $scope.queues = $scope.allqueues;
            };
        });
      };

      $scope.save = function (id) {
        if (id) {
          Queue.update({id: id}, $scope.queue, function (data) {
            console.log(data);
            var que = {};
            angular.forEach(data, function(value,key) {
              if(key !== '$promise' && key !== '$resolved') {
                que[key] = value;
              };
            });
            var ar = $scope.allqueues.map(function(e) {return e.id}).indexOf(id);
            $scope.allqueues[ar] = que;

            if ($scope.activebinessname !== 'All') {
              $scope.queues = $filter('filter')($scope.allqueues, {businessId: $scope.activebinessid});
            } else {
              $scope.queues = $scope.allqueues;
            }
            
            $scope.clear();
          });
        } else {
          Queue.save($scope.queue, function (data) {
            console.log(data);
            var que = {};
            angular.forEach(data, function(value,key) {
              if(key !== '$promise' && key !== '$resolved') {
                que[key] = value;
              };
            });
            $scope.allqueues[$scope.allqueues.length] = que;

            if ($scope.activebinessname !== 'All') {
              $scope.queues = $filter('filter')($scope.allqueues, {businessId: $scope.activebinessid});
            } else {
              $scope.queues = $scope.allqueues;
            }
            
            $scope.clear();
          });
        }
      };

      $scope.clear = function () {
        $scope.queue = {
          
          "queuename": "",

          "businessId": "",
        };
      };

      $scope.open = function (id) {
        var queueSave = $modal.open({
          templateUrl: 'queue-save.html',
          controller: 'QueueSaveController',
          size: 'sm',
          windowClass: 'my-modal-popup',
          resolve: {
            businesses: function() {
              return $scope.businesses;
            },
            queue: function() {
              return $scope.queue;
            }
          }
        });

        queueSave.result.then(function (entity) {
          $scope.queue = entity;
          console.log($scope.queue);
          $scope.save(id);
        });
      };
    }])
  .controller('QueueSaveController', ['$scope', '$modalInstance', 'businesses',  'queue',
    function ($scope, $modalInstance, businesses, queue) {
      $scope.businesses = businesses;
      $scope.queue = queue;
      

      $scope.ok = function () {
        $modalInstance.close($scope.queue);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
