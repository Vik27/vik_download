'use strict';

angular.module('noviga')
  .controller('ChannelsetupController', ['$scope', '$filter', '$modal', '$rootScope', 'Channelsetup', 'binessChannelsetup', 'resolvedAjaxItems',
    function ($scope, $filter, $modal, $rootScope, Channelsetup, binessChannelsetup, resolvedAjaxItems) {

      console.log(resolvedAjaxItems.chansetups);
      $scope.allchannelsetups = resolvedAjaxItems.chansetups;
      $scope.quantities = resolvedAjaxItems.quantities;

      $scope.binessSelect = false;
      if ($rootScope.loggedInUser.role === 'Admin') {
        $scope.binessSelect = true;
        $scope.activebusiness = {'name': 'All', 'id': ""};
        $scope.createButton = true;
        $scope.editDeleteButton = true;
        $scope.channelsetups = $scope.allchannelsetups;
        $scope.businesses = resolvedAjaxItems.businesses;
      } else {
        $scope.channelsetups = $scope.allchannelsetups;
        $scope.activebusiness = {id: $rootScope.loggedInUser.businessId};
        $scope.createButton = false;
        $scope.editDeleteButton = false;
      };

      $scope.changeothersetups = function (business) {
        if (business !=="all") {
          $scope.activebusiness = business;
          $scope.channelsetups = $filter('filter')($scope.allchannelsetups, {businessId: business.id});
          $scope.createButton = false;
          $scope.editDeleteButton = false;
        } else {
          $scope.channelsetups = $scope.allchannelsetups;
          $scope.activebusiness = {'name': 'All', 'id': null};
          $scope.createButton = true;
          $scope.editDeleteButton = true;
        }
      };

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        var chanset = {};
        angular.forEach($filter('filter')($scope.allchannelsetups, {id: id})[0], function(value,key) {
          chanset[key] = value;
        });
        $scope.channelsetup = chanset;
        console.log($scope.channelsetup);
        $scope.open(id);
      };

      $scope.delete = function (id) {
        if ($rootScope.loggedInUser.role === 'Admin') {
          binessChannelsetup.delete({businessId: $scope.activebusiness.id, id: id},
            function () {
              var trr = $scope.allchannelsetups.map(function(e) {return e.id}).indexOf(id);
              console.log(trr);
              $scope.allchannelsetups.splice(trr, 1);
              console.log($scope.allchannelsetups);
              $scope.channelsetups = $filter('filter')($scope.allchannelsetups, {businessId: $scope.activebusiness.id});
          });
        } else {
          binessChannelsetup.delete({businessId: $scope.activebusiness.id, id: id},
            function () {
              var trr = $scope.channelsetups.map(function(e) {return e.id}).indexOf(id);
              console.log(trr);
              $scope.channelsetups.splice(trr, 1);
              console.log($scope.channelsetups);
           });
        }
      };

      $scope.save = function (id) {
        if ($rootScope.loggedInUser.role === 'Admin') {
          if (id) {
            binessChannelsetup.update({businessId:$scope.activebusiness.id, id: id}, $scope.channelsetup,
              function (data) {
                console.log(data);
                var channelsetup = {};
                angular.forEach(data, function(value,key) {
                  if (key !== '$promise' && key !== '$resolved') {
                    channelsetup[key] = value;
                  }
                });
                var trr = $scope.allchannelsetups.map(function(e) {return e.id}).indexOf(id);
                $scope.allchannelsetups[trr] =channelsetup;
                $scope.channelsetups = $filter('filter')($scope.allchannelsetups, {businessId: $scope.activebusiness.id});
                // $scope.channelsetups = binessChannelsetup.query({businessId: $scope.activebusiness.id});
                // $scope.allchannelsetups[$scope.allchannelsetups.length] = $scope.channelsetup;
                $scope.clear();
            });
          } else {
            binessChannelsetup.save({businessId: $scope.activebusiness.id}, $scope.channelsetup,
              function (data) {
                console.log(data);
                var channelsetup = {};
                angular.forEach(data, function(value,key) {
                  if (key !== '$promise' && key !== '$resolved') {
                    channelsetup[key] = value;
                  }
                });
                $scope.allchannelsetups[$scope.allchannelsetups.length] = channelsetup;
                $scope.channelsetups = $filter('filter')($scope.allchannelsetups, {businessId: $scope.activebusiness.id});
                $scope.clear();
            });
          }
        } else {
          if (id) {
            binessChannelsetup.update({businessId:$scope.activebusiness.id, id: id}, $scope.channelsetup,
              function (data) {
                var trr = $scope.allchannelsetups.map(function(e) {return e.id}).indexOf(id);
                $scope.channelsetups[trr] = $scope.channelsetup;
                // $scope.channelsetups = binessChannelsetup.query({businessId: $scope.activebusiness.id});
                // $scope.allchannelsetups[$scope.allchannelsetups.length] = $scope.channelsetup;
                $scope.clear();
            });
          } else {
            binessChannelsetup.save({businessId: $scope.activebusiness.id}, $scope.channelsetup,
              function (data) {
                console.log(data);
                var channelsetup = {};
                angular.forEach(data, function(value,key) {
                  if (key !== '$promise' && key !== '$resolved') {
                    channelsetup[key] = value;
                  }
                });
                $scope.channelsetups[$scope.channelsetups.length] = channelsetup;
                $scope.clear();
            });
          }
        }
      };

      $scope.clear = function () {
        $scope.channelsetup = {
          
          "name": "",
          
          "sensitivity": "",
          
          "id": "",

          "quantityId": "",

          "unitId": "",

        };
      };

      $scope.open = function (id) {
        var channelsetupSave = $modal.open({
          templateUrl: 'channelsetup-save.html',
          controller: 'ChannelsetupSaveController',
          size:'sm',
          windowClass: 'my-modal-popup',
          resolve: {
            channelsetup: function () {
              return $scope.channelsetup;
            },
            quantities: function() {
              return $scope.quantities;
            }
          }
        });

        channelsetupSave.result.then(function (entity) {
          $scope.channelsetup = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('ChannelsetupSaveController', ['$scope', '$modalInstance', 'channelsetup', 'quantities', '$filter',
    function ($scope, $modalInstance, channelsetup, quantities, $filter) {
      $scope.channelsetup = channelsetup;
      $scope.quantities = quantities;

      if ($scope.channelsetup.quantityId !== "") {
        $scope.quantity = $filter('filter')(quantities, {id:$scope.channelsetup.quantityId})[0];
      } else {
        $scope.quantity = quantities[0];
        $scope.channelsetup.quantityId = quantities[0].id;
        $scope.channelsetup.unitId = quantities[0].units[0].id;
      }

      $scope.quantchange = function() {
        var brr = parseInt($scope.channelsetup.quantityId);
        var trr = $scope.quantities.map(function(e) {return e.id});
        var tr = trr.indexOf(brr);
        $scope.quantity = quantities[tr];
        $scope.channelsetup.unitId = $scope.quantity.units[0].id;
      };

      $scope.ok = function () {
        $modalInstance.close($scope.channelsetup);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
