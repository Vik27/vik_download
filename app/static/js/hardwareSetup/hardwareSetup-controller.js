'use strict';

angular.module('noviga')
  .controller('HardwareSetupController', ['$filter','$scope', '$modal', '$rootScope', 'resolvedAjaxItems',
  'HardwareSetup', 'Channeltemplates', 'Devicetable', 'Channelsetup', 'binessHwsetup',
  'binessChannelsetup', 'binessDevice', 'binessChanneltemps', 'binessHwchaschanmap', 'AcqSettings', 'binessAcqSettings',
  'verifyHwsetup', 'verifybinessHwsetup',
    function ($filter, $scope, $modal, $rootScope, resolvedAjaxItems, HardwareSetup, Channeltemplates,
      Devicetable, Channelsetup, binessHwsetup, binessChannelsetup, binessDevice, binessChanneltemps, binessHwchaschanmap,
      AcqSettings, binessAcqSettings, verifyHwsetup, verifybinessHwsetup) {
      
      console.log(resolvedAjaxItems.chansetups);
      console.log(resolvedAjaxItems.hwsetups);
      console.log(resolvedAjaxItems.businesses);
      $scope.allhardwareSetups = resolvedAjaxItems.hwsetups;
      $scope.chassises = resolvedAjaxItems.chassises;
      $scope.modules = resolvedAjaxItems.modules;
      $scope.modules[$scope.modules.length] = {"id": null, "modelNo": "Empty"};
      $scope.alldevices = resolvedAjaxItems.devices;
      $scope.allbineschantemps = resolvedAjaxItems.chansetups;
      $scope.allbineschantemps[$scope.allbineschantemps.length] = {"id": null, "name": "Empty"};
      $scope.quantities = resolvedAjaxItems.quantities;
      $scope.units = resolvedAjaxItems.units;
      

      $scope.binessSelect = false;
      if ($rootScope.loggedInUser.role === 'Admin') {
        $scope.binessSelect = true;
        $scope.activebusiness = {'name': 'All', 'id': null};
        $scope.createButton = true;
        $scope.businesses = resolvedAjaxItems.businesses;
        $scope.hardwareSetups = $scope.allhardwareSetups;
        $scope.devices = $scope.alldevices;
        $scope.allchantemps = $scope.allbineschantemps;
        // $scope.editDeleteButton = true;
      } else {
        $scope.activebusiness = {id: $rootScope.loggedInUser.businessId};
        console.log($scope.activebusiness);
        $scope.createButton = false;
        $scope.hardwareSetups = $scope.allhardwareSetups;
        $scope.devices = $scope.alldevices;
        $scope.allchantemps = $scope.allbineschantemps;
        // $scope.editDeleteButton = false;
      };

      $scope.changeothersetups = function (business) {
        if (business !=="all") {
          $scope.activebusiness = business;
          $scope.devices = $filter('filter')($scope.alldevices, {businessId: business.id});
          $scope.hardwareSetups = [];
          angular.forEach($scope.devices, function(value,key) {
            var hw = $filter('filter')($scope.allhardwareSetups, {deviceId: value.id});
            angular.forEach(hw, function(value,key) {
              $scope.hardwareSetups.push(value);
            });            
          });
          $scope.allchantemps = $filter('filter')($scope.allbineschantemps, {businessId: business.id});
          $scope.allchantemps[$scope.allchantemps.length] = {'name': 'Empty', 'id': null};
          $scope.createButton = false;
          // $scope.editDeleteButton = false;
        } else {
          $scope.hardwareSetups = $scope.allhardwareSetups;
          $scope.allchantemps = $scope.allbineschantemps;
          $scope.activebusiness = {'name': 'All', 'id': null};
          $scope.devices = $scope.alldevices;
          $scope.createButton = true;
          // $scope.editDeleteButton = true;
        }
      };

      $scope.verify = function(hwsetupId) {
        if ($rootScope.loggedInUser.role === 'Admin') {
          verifyHwsetup.get({id: hwsetupId}, function(data) {
            console.log(data.verification);
          });
        } else {
          verifybinessHwsetup.get({businessId: $scope.activebusiness.id, id: hwsetupId}, function(data) {
            console.log(data.verification);
          })
        }
      };

      $scope.allowVerify = function(hardwareSetup) {
        if (hardwareSetup.status === 'error') {
          return true;
        } else {
          return false;
        };
      };

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        var hwset = {};
        angular.forEach($filter('filter')($scope.hardwareSetups, {id: id})[0], function(value,key) {
          if (key === 'slotdetails') {
            hwset[key] = [];
            angular.forEach(value, function(val,ke) {
              hwset[key][ke] = {};
              angular.forEach(val, function(v,k) {
                hwset[key][ke][k] = v;
              });
            });
          } else {
            hwset[key] = value;
          };
        });
        $scope.hardwareSetup = hwset;
        console.log($scope.hardwareSetup);
        $scope.open(id);
      };

      $scope.delete = function (id) {
        if ($rootScope.loggedInUser.role === 'Admin') {
          HardwareSetup.delete({id: id},
            function () {
              var trr = $scope.allhardwareSetups.map(function(e) {return e.id}).indexOf(id);
              console.log(trr);
              $scope.allhardwareSetups.splice(trr, 1);
              console.log($scope.allhardwareSetups);
              $scope.hardwareSetups = [];
              angular.forEach($scope.devices, function(value,key) {
                var hw = $filter('filter')($scope.allhardwareSetups, {deviceId: value.id});
                angular.forEach(hw, function(value,key) {
                  $scope.hardwareSetups.push(value);
                });            
              });
          });
        } else {
          binessHwsetup.delete({businessId: $scope.activebusiness.id, id: id},
            function () {
              var trr = $scope.hardwareSetups.map(function(e) {return e.id}).indexOf(id);
              console.log(trr);
              $scope.hardwareSetups.splice(trr, 1);
          });
        }
      };

      $scope.save = function (id) {
        if ($rootScope.loggedInUser.role === 'Admin') {
          if (id) {
            HardwareSetup.update({id: id}, $scope.hardwareSetup, function (data) {
              console.log(data);
              var hardwaresetup = {};
              angular.forEach(data, function(value,key) {
                if (key !== '$promise' && key !== '$resolved') {
                  hardwaresetup[key] = value;
                }
              });
              var trr = $scope.allhardwareSetups.map(function(e) {return e.id}).indexOf(id);
              $scope.allhardwareSetups[trr] = hardwaresetup;
              $scope.hardwareSetups = [];
              angular.forEach($scope.devices, function(value,key) {
                var hardware = $filter('filter')($scope.allhardwareSetups, {deviceId: value.id});
                angular.forEach(hardware, function(value,key) {
                  $scope.hardwareSetups.push(value);
                });            
              });
              $scope.clear(); 
            });
          } else {
            HardwareSetup.save($scope.hardwareSetup, function (data) {
              console.log(data);
              var hardwaresetup = {};
              angular.forEach(data, function(value,key) {
                if (key !== '$promise' && key !== '$resolved') {
                  hardwaresetup[key] = value;
                }
              });
              $scope.allhardwareSetups[$scope.allhardwareSetups.length] = hardwaresetup;
              $scope.hardwareSetups = [];
              angular.forEach($scope.devices, function(value,key) {
                var hardware = $filter('filter')($scope.allhardwareSetups, {deviceId: value.id});
                angular.forEach(hardware, function(value,key) {
                  $scope.hardwareSetups.push(value);
                });            
              });
              $scope.clear(); 
            });
          }
        } else {
          if (id) {
            binessHwsetup.update({businessId: $scope.activebusiness.id, id: id}, $scope.hardwareSetup, function (data) {
              console.log(data);
              var hardwaresetup = {};
              angular.forEach(data, function(value,key) {
                if (key !== '$promise' && key !== '$resolved') {
                  hardwaresetup[key] = value;
                }
              });
              var trr = $scope.allhardwareSetups.map(function(e) {return e.id}).indexOf(id);
              $scope.hardwareSetups[trr] = hardwaresetup;
              $scope.clear();
            });
          } else {
            binessHwsetup.save({businessId: $scope.activebusiness.id}, $scope.hardwareSetup, function (data) {
              console.log(data);
              var hardwaresetup = {};
              angular.forEach(data, function(value,key) {
                if (key !== '$promise' && key !== '$resolved') {
                  hardwaresetup[key] = value;
                }
              });
              $scope.hardwareSetups[$scope.hardwareSetups.length] = hardwaresetup;
              $scope.clear(); 
            });
          }
        }
      };

      $scope.clear = function () {
        $scope.hardwareSetup = {
          
          "name": "",
          
          "deviceId": $scope.devices[0].id,

          "slotdetails": []
        };
        var arr = parseInt($scope.devices[0].niChassisId);
        var trr = $scope.chassises.map(function(e) {return e.id});
        var tr = trr.indexOf(arr);
        var activeChassisModelNo = $scope.chassises[tr];
        var arrayLength = parseInt(activeChassisModelNo.maxSlots);
        for (var i = 0; i < arrayLength; i++) {
          $scope.hardwareSetup.slotdetails[i]= {'slotnumber': i+1, 'moduleID' : null, 'samplingrate': null, 'samplingchoose': true};
        }
      };

      $scope.updatesinglechan = function(hwchasmaprow,chansetup) {
        console.log(hwchasmaprow);
        console.log(chansetup.id);

        var arr = $filter('filter')($scope.allhardwareSetups, {id: hwchasmaprow.hwSetupID})[0];
        var brr = $filter('filter')($scope.alldevices, {id: arr.deviceId})[0];
        var crr = $filter('filter')($scope.allbineschantemps, {businessId: brr.businessId});
        var drr = $filter('filter')($scope.modules, {id: hwchasmaprow.moduleID})[0];
        var frr = drr.quantities.map(function(e) {return e.id});
        var irr = [];
        angular.forEach(frr, function(value,key) {
          var grr = $filter('filter')($scope.quantities, {id: value})[0];
          var hrr = grr.units.map(function(e) {return e.id});
          angular.forEach(hrr, function(value,key) {
            irr.push(value);
          });
        });
        $scope.chantemps = [];
        angular.forEach(crr, function(value,key) {
          if (irr.indexOf(value.unitId) !== -1) {
            $scope.chantemps.push(value);
          };
        });
        $scope.chantemps.push({"id": null, "name": "Empty"});

        $scope.chanmaprow= {
          'channelnumber': chansetup.channelnumber,
          'name' : chansetup.name,
          'peakvalue': chansetup.peakvalue,
          'chantempId': chansetup.channelTemplateId,
        };

        $scope.peakVoltRange = drr.peakVoltRange;
        $scope.opensinglechan(hwchasmaprow.hwSetupID,hwchasmaprow.id,chansetup.id);

      };

      $scope.savesinglechan = function (hwsetupId,chasrowId,chansetupId) {
        binessHwchaschanmap.update({businessId: $scope.activebusiness.id, id: chansetupId}, $scope.chanmaprow, function (data) {
          console.log('Let\'s try this!');
          console.log(data.chansetup);
          console.log(data.acqoptions);
          var arr = $scope.allhardwareSetups.map(function(e) {return e.id});
          var br = arr.indexOf(hwsetupId);
          var crr = $filter('filter')($scope.allhardwareSetups, {id: hwsetupId})[0];
          var drr = crr.slotdetails.map(function(e) {return e.id});
          var fr = drr.indexOf(chasrowId);
          var grr = $scope.allhardwareSetups[br].slotdetails[fr].channelsetup.map(function(e) {return e.id});
          var hr = grr.indexOf(chansetupId);
          $scope.allhardwareSetups[br].slotdetails[fr].channelsetup[hr] = data.chansetup;
          $scope.allhardwareSetups[br].acqoptions = data.acqoptions;
          $scope.allhardwareSetups[br].acqstart = data.acqstart;
          $scope.allhardwareSetups[br].acqstop = data.acqstop;
          $scope.allhardwareSetups[br].status = data.hwstatus;
          $scope.hardwareSetups = [];
          angular.forEach($scope.devices, function(value,key) {
            var hardware = $filter('filter')($scope.allhardwareSetups, {deviceId: value.id});
            angular.forEach(hardware, function(value,key) {
              $scope.hardwareSetups.push(value);
            });            
          });
        });
      };

      $scope.opensinglechan = function(hwsetupId,chasrowId,chansetupId) {
        var chantempsave = $modal.open({
          templateUrl: 'channelselect.html',
          controller: 'channelselectController',
          size:'sm',
          windowClass: 'my-modal-popup',
          resolve: {
            chanmaprow: function () {
              return $scope.chanmaprow;
            },
            chantemps: function() {
              return $scope.chantemps;
            },
            peakVoltRange: function() {
              return $scope.peakVoltRange;
            },
            units: function() {
              return $scope.units;
            }
          }
        });

        chantempsave.result.then(function (entity) {
          $scope.chanmaprow = entity;
          console.log($scope.chanmaprow);
          console.log("yay");
          $scope.savesinglechan(hwsetupId,chasrowId,chansetupId);
        });
      };

      $scope.createchan = function (hwchasmaprow) {
        $scope.getchantemps(hwchasmaprow);
      };

      $scope.getchantemps = function(hwchasmaprow) {
        var arr = $filter('filter')($scope.allhardwareSetups, {id: hwchasmaprow.hwSetupID})[0];
        var brr = $filter('filter')($scope.alldevices, {id: arr.deviceId})[0];
        var crr = $filter('filter')($scope.allbineschantemps, {businessId: brr.businessId});
        var drr = $filter('filter')($scope.modules, {id: hwchasmaprow.moduleID})[0];
        var frr = drr.quantities.map(function(e) {return e.id});
        var irr = [];
        angular.forEach(frr, function(value,key) {
          var grr = $filter('filter')($scope.quantities, {id: value})[0];
          var hrr = grr.units.map(function(e) {return e.id});
          angular.forEach(hrr, function(value,key) {
            irr.push(value);
          });
        });
        $scope.chantemps = [];
        angular.forEach(crr, function(value,key) {
          if (irr.indexOf(value.unitId) !== -1) {
            $scope.chantemps.push(value);
          };
        });
        $scope.chantemps.push({"id": null, "name": "Empty"});
        $scope.peakVoltRange = drr.peakVoltRange;
        $scope.clearchan(hwchasmaprow);
        $scope.openchan(hwchasmaprow.id,hwchasmaprow.hwSetupID);
      };

      $scope.clearchan = function (hwchasmaprow) {
        var crr = parseInt(hwchasmaprow.moduleID)
        var drr = $scope.modules.map(function(e) {return e.id});
        var br = drr.indexOf(crr);
        $scope.activeModule = $scope.modules[br];
        var arrayLength = parseInt($scope.activeModule.maxChannels);
        $scope.chanmaprows = [];
        for (var i = 0; i < arrayLength; i++) {
          $scope.chanmaprows[i]= {'channelnumber': i, 'name' : "Channel" + i, 'peakvalue': null, 'chantempId': null, 'peakvaluechoose': true};
        }
      };

      $scope.savechan = function (chasrowId,hwsetupId) {
        $scope.postedData = {'hwchassId': chasrowId, 'chanmaprows': $scope.chanmaprows}
        console.log($scope.postedData);
        binessHwchaschanmap.save({businessId: $scope.activebusiness.id}, $scope.postedData, function (data) {
          console.log('Done, it is!');
          console.log(data.channelsetup);
          console.log(data.acqoptions);
          var arr = $scope.allhardwareSetups.map(function(e) {return e.id});
          var br = arr.indexOf(hwsetupId);
          var crr = $filter('filter')($scope.allhardwareSetups, {id: hwsetupId})[0];
          var drr = crr.slotdetails.map(function(e) {return e.id}) ;
          var fr = drr.indexOf(chasrowId);
          $scope.allhardwareSetups[br].slotdetails[fr].chansetupshow = true;
          $scope.allhardwareSetups[br].slotdetails[fr].channelsetup = data.channelsetup;
          $scope.allhardwareSetups[br].acqoptions = data.acqoptions;
          $scope.allhardwareSetups[br].status = data.hwstatus;
          $scope.hardwareSetups = [];
          angular.forEach($scope.devices, function(value,key) {
            var hardware = $filter('filter')($scope.allhardwareSetups, {deviceId: value.id});
            angular.forEach(hardware, function(value,key) {
              $scope.hardwareSetups.push(value);
            });            
          });
        });
      };

      $scope.openchan = function(chasrowId,hwsetupId) {
        var chanchasmapSave = $modal.open({
          templateUrl: 'chanSetup-save.html',
          controller: 'chanSetupSaveController',
          size:'sm',
          windowClass: 'my-modal-popup',
          resolve: {
            chanmaprows: function () {
              return $scope.chanmaprows;
            },
            chantemps: function() {
              return $scope.chantemps;
            },
            peakVoltRange: function() {
              return $scope.peakVoltRange;
            }
          }
        });

        chanchasmapSave.result.then(function (entity) {
          $scope.chanmaprows = entity;
          console.log($scope.chanmaprows);
          console.log("yay");
          $scope.savechan(chasrowId,hwsetupId);
        });
      };

      $scope.open = function (id) {
        var hardwareSetupSave = $modal.open({
          templateUrl: 'hardwareSetup-save.html',
          controller: 'HardwareSetupSaveController',
          size:'sm',
          windowClass: 'my-modal-popup',
          resolve: {
            hardwareSetup: function () {
              return $scope.hardwareSetup;
            },
            chassises: function() {
              return $scope.chassises;
            },
            modules: function () {
              return $scope.modules;
            },
            devices: function () {
              return $scope.devices;
            }
          }
        });

        hardwareSetupSave.result.then(function (entity) {
          $scope.hardwareSetup = entity;
          console.log("eureka");
          console.log($scope.hardwareSetup);
          $scope.save(id);
        });
      };

      $scope.editacqsettings = function(hwsetupId) {
        $scope.hardwareSetup = $filter('filter')($scope.hardwareSetups, {id: hwsetupId})[0];
        console.log($scope.hardwareSetup.acqoptions);
        $scope.acqoptions = $scope.hardwareSetup.acqoptions;
        var acqstart = {};
        angular.forEach($scope.hardwareSetup.acqstart, function(value,key) {
          if (key==='eventValue') {
            acqstart[key] = {};
            angular.forEach(value, function(v,k) {
              acqstart[key][k] = v;
            });
          } else {
            acqstart[key] = value;
          }
        });
        var acqstop = {};
        angular.forEach($scope.hardwareSetup.acqstop, function(value,key) {
          if (key==='eventValue') {
            acqstop[key] = {};
            angular.forEach(value, function(v,k) {
              acqstop[key][k] = v;
            });
          } else {
            acqstop[key] = value;
          }
        });
        $scope.acqsettings = {'acqstart': acqstart, 'acqstop': acqstop};
        $scope.openEditAcq(hwsetupId);
      };

      $scope.updateAcqSettings = function(hwsetupId) {
        if ($rootScope.loggedInUser.role === 'Admin') {
          AcqSettings.update({hwsetupId: hwsetupId}, $scope.acqsettings, function (data) {
            console.log(data);
            var acqstart = data.acqstart;
            var acqstop = data.acqstop;
            var trr = $scope.allhardwareSetups.map(function(e) {return e.id}).indexOf(hwsetupId);
            $scope.allhardwareSetups[trr].acqstart = acqstart;
            $scope.allhardwareSetups[trr].acqstop = acqstop;
            $scope.allhardwareSetups[trr].status = data.hwstatus;
            $scope.hardwareSetups = [];
            angular.forEach($scope.devices, function(value,key) {
              var hardware = $filter('filter')($scope.allhardwareSetups, {deviceId: value.id});
              angular.forEach(hardware, function(value,key) {
                $scope.hardwareSetups.push(value);
              });            
            });
            // $scope.clear(); 
          })
        } else {
          binessAcqSettings.update({businessId: $scope.activebusiness.id, hwsetupId: hwsetupId}, $scope.acqsettings, function (data) {
            console.log(data);
            var acqstart = data.acqstart;
            var acqstop = data.acqstop;
            var trr = $scope.hardwareSetups.map(function(e) {return e.id}).indexOf(hwsetupId);
            $scope.hardwareSetups[trr].acqstart = acqstart;
            $scope.hardwareSetups[trr].acqstop = acqstop;
          })
        }
      };

      $scope.openEditAcq = function(hwsetupId) {
        var acqSettingSave = $modal.open({
          templateUrl: 'acqSetting-save.html',
          controller: 'acqSettingSaveController',
          size: 'sm',
          windowClass: 'my-modal-popup',
          resolve: {
            acqoptions: function () {
              return $scope.acqoptions;
            },
            acqsettings: function () {
              return $scope.acqsettings;
            },
            hardwareSetup: function () {
              return $scope.hardwareSetup;
            }
          }
        });

        acqSettingSave.result.then(function (entity) {
          $scope.acqsettings = entity;
          console.log("phobia");
          console.log($scope.acqsettings);
          $scope.updateAcqSettings(hwsetupId);
        });
      };
    
    }])
  
  .controller('HardwareSetupSaveController', ['$filter','$scope', '$modalInstance', 'hardwareSetup', 'chassises', 'modules', 'devices',
    function ($filter, $scope, $modalInstance, hardwareSetup, chassises, modules, devices) {
      
      // $scope.hardwareSetup=hardwareSetup;
      $scope.devices = devices;
      $scope.chassises = chassises;
      $scope.modules = modules;


      if (hardwareSetup.name === "") {
        $scope.hardwareSetup = hardwareSetup;
        $scope.devreadonly = false;
      } else {
        $scope.hardwareSetup = hardwareSetup;
        $scope.devreadonly = true;
      }

      $scope.modulechange = function(slotdetail) {
        if (slotdetail.moduleID !== null && slotdetail.moduleID !== 'Empty') {
          slotdetail.samplingchoose = false;
          slotdetail.maxSampling = parseInt($filter('filter')($scope.modules, {id:slotdetail.moduleID})[0].maxSamplingRate);
          console.log(slotdetail.maxSampling);
          slotdetail.minSampling = 100;
          console.log(slotdetail.slotnumber);
          console.log(slotdetail.minSampling);
        } else {
          slotdetail.samplingchoose = true;
          slotdetail.samplingrate = null;
        }
      }

      $scope.deviceChange = function () {
        var brr = parseInt($scope.hardwareSetup.deviceId);
        var drr = $scope.devices.map(function(e) {return e.id});
        var dr = drr.indexOf(brr);
        $scope.activeDevice = devices[dr];
        var arr = parseInt($scope.activeDevice.niChassisId);
        var trr = $scope.chassises.map(function(e) {return e.id});
        var tr = trr.indexOf(arr);
        $scope.activeChassisModelNo = chassises[tr];
        var arrayLength = parseInt($scope.activeChassisModelNo.maxSlots);
        for (var i = 0; i < arrayLength; i++) {
          $scope.hardwareSetup.slotdetails[i]= {'slotnumber': i+1, 'moduleID' : null, 'samplingrate': null, 'samplingchoose': true};
        }
      }
      

      $scope.ok = function () {
        $modalInstance.close($scope.hardwareSetup);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }])

  .controller('chanSetupSaveController', ['$scope', '$filter', '$modalInstance', 'chanmaprows', 'chantemps', 'peakVoltRange',
    function ($scope, $filter, $modalInstance, chanmaprows, chantemps, peakVoltRange) {
      
      $scope.chanmaprows = chanmaprows;
      $scope.chantemps = chantemps;

      $scope.chantempchange = function(chanmaprow) {
        // var arr = $scope.hardwareSetup.slotdetails.map(function(e) {return e.slotnumber}).indexOf(slotnumber);
        if (chanmaprow.chantempId !== null && chanmaprow.chantempId !== 'Empty') {
          chanmaprow.peakvaluechoose = false;
          var arr = ($filter('filter')($scope.chantemps, {id:chanmaprow.chantempId})[0].sensitivity);
          console.log(arr);
          chanmaprow.maxPeakValue = (peakVoltRange*1000.0)/arr;
          console.log(chanmaprow.maxPeakValue);
          chanmaprow.minPeakValue = 0;
          console.log(chanmaprow.minPeakValue);
          chanmaprow.peakvalue = chanmaprow.maxPeakValue;
        } else {
          chanmaprow.peakvaluechoose = true;
          chanmaprow.peakvalue = null;
        }
      }      

      $scope.ok = function () {
        $modalInstance.close($scope.chanmaprows);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }])

  .controller('channelselectController', ['$scope', '$filter', '$modalInstance', 'chanmaprow', 'chantemps', 'peakVoltRange', 'units',
    function ($scope, $filter, $modalInstance, chanmaprow, chantemps, peakVoltRange, units) {
      
      $scope.chanmaprow = chanmaprow;
      $scope.chantemps = chantemps;   
      $scope.units = units;   

      $scope.chantempchange = function() {
        // var arr = $scope.hardwareSetup.slotdetails.map(function(e) {return e.slotnumber}).indexOf(slotnumber);
        if ($scope.chanmaprow.chantempId !== null && $scope.chanmaprow.chantempId !== 'Empty') {
          $scope.chanmaprow.peakvaluechoose = false;
          var arr = ($filter('filter')($scope.chantemps, {id:$scope.chanmaprow.chantempId})[0].sensitivity);
          console.log(arr);
          $scope.chanmaprow.maxPeakValue = (peakVoltRange*1000.0)/arr;
          console.log(chanmaprow.maxPeakValue);
          $scope.chanmaprow.minPeakValue = 0;
          console.log(chanmaprow.minPeakValue);
          $scope.chanmaprow.peakvalue = $scope.chanmaprow.maxPeakValue;
        } else {
          $scope.chanmaprow.peakvaluechoose = true;
          $scope.chanmaprow.peakvalue = null;
        }
      }      

      $scope.ok = function () {
        $modalInstance.close($scope.chanmaprow);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }])


.controller('acqSettingSaveController', ['$scope', '$filter', '$modalInstance', '$timeout', 'acqsettings', 'hardwareSetup', 'acqoptions',
    function ($scope, $filter, $modalInstance, $timeout, acqsettings, hardwareSetup, acqoptions) {
      
      $scope.acqoptions = acqoptions;
      $scope.acqsttings = acqsettings;
      console.log(acqsettings);
      $scope.hardwareSetup = hardwareSetup;

      if (acqoptions.length > 2) {
        var digarr = acqoptions.map(function(e) {return e.name}).indexOf('Digital');
        var levarr = acqoptions.map(function(e) {return e.name}).indexOf('Level-based');
        if (digarr !== -1) {
          var digacqoptions = [];
          angular.forEach(acqoptions[digarr].options, function(value,key) {
            var slot = value.slotId;
            var xx = $filter('filter')(hardwareSetup.slotdetails, {id:slot})[0].slotnumber
            var yy = hardwareSetup.slotdetails.map(function(e) {return e.id}).indexOf(slot);
            console.log(yy);
            var chans = value.corres_chanIds;
            angular.forEach(chans, function(v,k) {
              digacqoptions.push({'name': $filter('filter')(hardwareSetup.slotdetails[yy].channelsetup, {id:v})[0].name,
                'id': v,
                'slotId': 'Slot' + xx
              });
            });
          });
          $scope.digacqoptions = digacqoptions;
        };
        if (levarr !== -1) {
          var levacqoptions = [];
          angular.forEach(acqoptions[levarr].options, function(value,key) {
            var slot = value.slotId;
            var xx = $filter('filter')(hardwareSetup.slotdetails, {id:slot})[0].slotnumber
            var yy = hardwareSetup.slotdetails.map(function(e) {return e.id}).indexOf(slot);
            console.log(yy);
            var chans = value.corres_chanIds;
            angular.forEach(chans, function(v,k) {
              levacqoptions.push({'name': $filter('filter')(hardwareSetup.slotdetails[yy].channelsetup, {id:v})[0].name,
                'peakvalue': $filter('filter')(hardwareSetup.slotdetails[yy].channelsetup, {id:v})[0].peakvalue,
                'id': v,
                'slotId': 'Slot' + xx
              });
            });
          });
          $scope.levacqoptions = levacqoptions;
        };
      }

      $scope.ok = function () {
        if ($scope.acqsttings.acqstart.event === 'Free') {
          $scope.acqsttings.acqstart.eventValue = null
        } else if ($scope.acqsttings.acqstart.event === 'Time-based') {
          var eventValue = $scope.acqsttings.acqstart.eventValue.time
          $scope.acqsttings.acqstart.eventValue = {'time': eventValue};
        } else if ($scope.acqsttings.acqstart.event === 'Digital') {
          var eventValue = {};
          eventValue.digchanmaprowId = $scope.acqsttings.acqstart.eventValue.digchanmaprowId;
          eventValue.digslope = $scope.acqsttings.acqstart.eventValue.digslope;
          $scope.acqsttings.acqstart.eventValue = {'digchanmaprowId': eventValue.digchanmaprowId, 'digslope': eventValue.digslope};
        } else {
          var eventValue = {};
          eventValue.levchanmaprowId = $scope.acqsttings.acqstart.eventValue.levchanmaprowId;
          eventValue.levslope = $scope.acqsttings.acqstart.eventValue.levslope;
          eventValue.threshold = $scope.acqsttings.acqstart.eventValue.threshold;
          $scope.acqsttings.acqstart.eventValue = {
            'levchanmaprowId': eventValue.levchanmaprowId,
            'levslope': eventValue.levslope,
            'threshold': eventValue.threshold
          };
        }
        if ($scope.acqsttings.acqstop.event === 'Free') {
          $scope.acqsttings.acqstop.eventValue = null
        } else if ($scope.acqsttings.acqstop.event === 'Time-based') {
          var eventValue = $scope.acqsttings.acqstop.eventValue.time
          $scope.acqsttings.acqstop.eventValue = {'time': eventValue};
        } else if ($scope.acqsttings.acqstop.event === 'Digital') {
          var eventValue = {};
          eventValue.digchanmaprowId = $scope.acqsttings.acqstop.eventValue.digchanmaprowId;
          eventValue.digslope = $scope.acqsttings.acqstop.eventValue.digslope;
          $scope.acqsttings.acqstop.eventValue = {'digchanmaprowId': eventValue.digchanmaprowId, 'digslope': eventValue.digslope};
        } else {
          var eventValue = {};
          eventValue.levchanmaprowId = $scope.acqsttings.acqstop.eventValue.levchanmaprowId;
          eventValue.levslope = $scope.acqsttings.acqstop.eventValue.levslope;
          eventValue.threshold = $scope.acqsttings.acqstop.eventValue.threshold;
          $scope.acqsttings.acqstop.eventValue = {
            'levchanmaprowId': eventValue.levchanmaprowId,
            'levslope': eventValue.levslope,
            'threshold': eventValue.threshold
          };
        }

        if (($scope.acqsttings.acqstart.event===$scope.acqsttings.acqstop.event) && ($scope.acqsttings.acqstart.event!=='Free')) {
          var flag = 0
          angular.forEach($scope.acqsttings.acqstart.eventValue, function(value,key) {
            if ($scope.acqsttings.acqstop.eventValue[key] === value) {
              flag = flag + 0;
            } else {
              flag = flag + 1;
            };
          })
          if (flag > 0) {
            $modalInstance.close($scope.acqsttings);
          } else {
            $scope.error = true;
            $scope.errorMessage = 'Acquisition start and stop cannot be triggered by the same event. Change either of the two settings!'
            $timeout(function () {
              $scope.error = false;
            },3000);
          }
        } else {
          $modalInstance.close($scope.acqsttings);
        };
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };

      // if (acqsettings.acqstart.event === 'Digital') {
      //   var currentStartIndex = $scope.digacqoptions.map(function(e) {return e.id}).indexOf($scope.acqsttings.acqstart.eventValue.digchanmaprowId);
      //   var stopdigopts = $scope.digacqoptions;
      //   stopdigopts.splice(currentStartIndex,1);
      //   $scope.stopdigopts = stopdigopts;
      // } else {
      //   $scope.stopdigopts = $scope.digacqoptions;
      // };

      // if (acqsettings.acqstop.event === 'Digital') {
      //   var currentStopIndex = $scope.digacqoptions.map(function(e) {return e.id}).indexOf($scope.acqsttings.acqstop.eventValue.digchanmaprowId);
      //   var startdigopts = $scope.digacqoptions;
      //   startdigopts.splice(currentStopIndex,1);
      //   $scope.startdigopts = startdigopts;
      // } else {
      //   $scope.startdigopts = $scope.digacqoptions;
      // };

      // if (acqsettings.acqstart.event === 'Level-based') {
      //   var currentStartIndex = $scope.levacqoptions.map(function(e) {return e.id}).indexOf($scope.acqsttings.acqstart.eventValue.levchanmaprowId);
      //   var stoplevopts = $scope.levacqoptions;
      //   stoplevopts.splice(currentStartIndex,1);
      //   $scope.stoplevopts = stoplevopts;
      // } else {
      //   $scope.stoplevopts = $scope.levacqoptions;
      // };

      // if (acqsettings.acqstop.event === 'Level-based') {
      //   var currentStopIndex = $scope.levacqoptions.map(function(e) {return e.id}).indexOf($scope.acqsttings.acqstop.eventValue.levchanmaprowId);
      //   var startlevopts = $scope.levacqoptions;
      //   startlevopts.splice(currentStopIndex,1);
      //   $scope.startlevopts = startlevopts;
      // } else {
      //   $scope.startlevopts = $scope.levacqoptions;
      // };

      // var currentStartIndex = $scope.levacqoptions.map(function(e) {return e.id}).indexOf($scope.acqsttings.acqstart.eventValue.chanmaprowId);
      // var currentStopIndex = $scope.levacqoptions.map(function(e) {return e.id}).indexOf($scope.acqsttings.acqstop.eventValue.chanmaprowId);
      // $scope.startlevopts = $scope.levacqoptions;
      // $scope.startdigopts = $scope.digacqoptions;
      
    }])


.directive('ngMin', function () {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function (scope, elem, attr, ctrl) {
            scope.$watch(attr.ngMin, function () {
                ctrl.$setViewValue(ctrl.$viewValue);
            });

            var isEmpty = function (value) {
               return angular.isUndefined(value) || value === "" || value === null;
            }

            var minValidator = function (value) {
                var min = scope.$eval(attr.ngMin) || 0;
                if (!isEmpty(value) && value < min) {
                    ctrl.$setValidity('ngMin', false);
                    return undefined;
                } else {
                    ctrl.$setValidity('ngMin', true);
                    return value;
                }
            };

            ctrl.$parsers.push(minValidator);
            ctrl.$formatters.push(minValidator);
        }
    };
})

.directive('ngMax', function () {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function (scope, elem, attr, ctrl) {
            scope.$watch(attr.ngMax, function () {
                ctrl.$setViewValue(ctrl.$viewValue);
            });

            var isEmpty = function (value) {
               return angular.isUndefined(value) || value === "" || value === null;
            }

            var maxValidator = function (value) {
                var max = scope.$eval(attr.ngMax) || Infinity;
                if (!isEmpty(value) && value > max) {
                    ctrl.$setValidity('ngMax', false);
                    return undefined;
                } else {
                    ctrl.$setValidity('ngMax', true);
                    return value;
                }
            };

            ctrl.$parsers.push(maxValidator);
            ctrl.$formatters.push(maxValidator);
        }
    };
})

.directive('ngSamp', function () {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function (scope, elem, attr, ctrl) {
            scope.$watch(attr.ngSamp, function () {
                ctrl.$setViewValue(ctrl.$viewValue);
            });

            var isEmpty = function (value) {
               return angular.isUndefined(value) || value === "" || value === null;
            }

            var maxValidator = function (value) {
                var samp = scope.$eval(attr.ngSamp) || Infinity;
                
                if (!isEmpty(value)) {
                  var arr = (value%100);
                  var brr = value/samp;
                  if ((arr === 0) && ((brr & (brr-1)) === 0)) {
                    ctrl.$setValidity('ngSamp', true);
                    return value;
                  } else {
                    ctrl.$setValidity('ngSamp', false);
                    return undefined;
                  }
                } else {
                    ctrl.$setValidity('ngSamp', true);
                    return value;
                }
            };

            ctrl.$parsers.push(maxValidator);
            ctrl.$formatters.push(maxValidator);
        }
    };
})


  // .directive('chanDropdown', function() {
  //   return {
  //     restrict: 'E',
  //     scope:{
  //       mod: '=module',
  //       chaschanmap: '=chaschanmapId',
  //     },
  //     replace: true,
  //     templateUrl: 'channelselect.html',
  //     // link: function (scope, element, attribute) {

  //     // },
  //     controller: function ($scope, Channeltemplates) {
  //       console.log($scope.mod);
  //       console.log($scope.chaschanmap);
  //       Channeltemplates.query({id: 1}, function (data) {
  //         $scope.chantemps = data;
  //       });
  //     },
  //   };
  // })
