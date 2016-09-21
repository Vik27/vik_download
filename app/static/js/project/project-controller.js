'use strict';

angular.module('noviga')
  .controller('ProjectController', ['$filter', '$rootScope', '$scope', '$modal','resolvedAjaxItems', 'binessHwsetup', 'binessProject', 'Project', 'HardwareSetup','runProject', 'runbinessProject',
    function ($filter, $rootScope, $scope, $modal, resolvedAjaxItems, binessHwsetup, binessProject, Project, HardwareSetup, runProject, runbinessProject) {

      console.log(resolvedAjaxItems.hwsetups);
      console.log(resolvedAjaxItems.projects);
      console.log(resolvedAjaxItems.devices);
      // resolvedAjaxItems.$promise.then(function(data) {
      //   $scope.projects = data.projects;
      //   console.log($scope.projects);
      //   $scope.hwsetups = data.hwsetups;
      //   console.log($scope.hwsetups);
      // });

      $scope.allprojects = resolvedAjaxItems.projects;
      $scope.allhwsetups = resolvedAjaxItems.hwsetups;
      $scope.alldevices = resolvedAjaxItems.devices;
      

      $scope.binessSelect = false;
      if ($rootScope.loggedInUser.role === 'Admin') {
        $scope.binessSelect = true;
        $scope.activebusiness = {'name': 'All', 'id': null};
        $scope.editDeleteButton = false;
        $scope.createButton = true;
        $scope.businesses = resolvedAjaxItems.businesses;
        $scope.projects = $scope.allprojects;
        $scope.hwsetups = $scope.allhwsetups;
      } else {
        $scope.projects = $scope.allprojects;
        $scope.hwsetups = $scope.allhwsetups;
        $scope.activebusiness = {id: $rootScope.loggedInUser.businessId};
        $scope.editDeleteButton = true;
        $scope.createButton = false;
      };

      $scope.changeothersetups = function (business) {
        if (business !=="all") {
          $scope.activebusiness = business;
          $scope.projects = $filter('filter')($scope.allprojects, {businessId: business.id});
          var trr = $filter('filter')($scope.alldevices, {businessId: business.id});
          $scope.hwsetups = [];
          angular.forEach(trr, function(value,key) {
            var hw = $filter('filter')($scope.allhwsetups, {deviceId: value.id});
            angular.forEach(hw, function(v,k) {
              $scope.hwsetups.push(v);
            });            
          });
          console.log($scope.hwsetups);
          $scope.editDeleteButton = true;
          $scope.createButton = false;
        } else {
          $scope.projects = $scope.allprojects;
          $scope.activebusiness = {'name': 'All', 'id': null};
          $scope.hwsetups = $scope.allhwsetups;
          $scope.editDeleteButton = false;
          $scope.createButton = true;
        }
      };


      $scope.runthe = function(projectId) {
        if ($rootScope.loggedInUser.role === 'Admin') {
          runProject.get({id: projectId}, function(data) {
            console.log(data.runans);
          });
        } else {
          runbinessProject.get({businessId: $scope.activebusiness.id, id: projectId}, function(data) {
            console.log(data.runans);
          })
        }
      };

      $scope.allowRun = function(project) {
        if (project.status === 'incomplete' || project.status === 'running') {
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
        var project = {};
        angular.forEach($filter('filter')($scope.projects, {id: id})[0], function(value,key) {
          project[key] = value;
        });
        $scope.project = project
        console.log($scope.project);
        $scope.open(id);
      };

      $scope.delete = function (id) {
        if ($rootScope.loggedInUser.role === 'Admin') {
          Project.delete({id: id},
            function () {
              var trr = $scope.allprojects.map(function(e) {return e.id}).indexOf(id);
              console.log(trr);
              $scope.allprojects.splice(trr, 1);
              console.log($scope.allprojects);
              $scope.projects = $filter('filter')($scope.allprojects, {businessId: $scope.activebusiness.id});
          });
        } else {
          binessProject.delete({businessId: $scope.activebusiness.id, id: id},
            function () {
              var trr = $scope.projects.map(function(e) {return e.id}).indexOf(id);
              console.log(trr);
              $scope.projects.splice(trr, 1);
              console.log($scope.projects);
           });
        }
      };

      $scope.save = function (id) {
        if ($rootScope.loggedInUser.role === 'Admin') {
          if (id) {
            var postedData = {'businessId': $scope.activebusiness.id, 'projectsetup': $scope.project};
            Project.update({id: id}, postedData, function (data) {
              var project = {};
              angular.forEach(data, function(value,key) {
                if (key !== '$promise' && key !== '$resolved') {
                  project[key] = value;
                }
              });
              var trr = $scope.allprojects.map(function(e) {return e.id}).indexOf(id);
              $scope.allprojects[trr] = project;
              $scope.projects = $filter('filter')($scope.allprojects, {businessId: $scope.activebusiness.id});
              $scope.clear();
            });
          } else {
            var postedData = {'businessId': $scope.activebusiness.id, 'projectsetup': $scope.project};
            Project.save(postedData, function (data) {
              var project = {};
              angular.forEach(data, function(value,key) {
                if (key !== '$promise' && key !== '$resolved') {
                  project[key] = value;
                }
              });
              console.log(project);
              console.log($scope.allprojects);
              $scope.allprojects[$scope.allprojects.length] = project;
              console.log($scope.allprojects);
              $scope.projects = $filter('filter')($scope.allprojects, {businessId: $scope.activebusiness.id});
              console.log($scope.projects);
              $scope.clear();
            });
          }
        } else {
          if (id) {
            binessProject.update({businessId: $scope.activebusiness.id, id:id}, $scope.project, function (data) {
              var project = {};
              angular.forEach(data, function(value,key) {
                if (key !== '$promise' && key !== '$resolved') {
                  project[key] = value;
                }
              });
              var trr = $scope.projects.map(function(e) {return e.id}).indexOf(id);
              $scope.projects[trr] = project;
              $scope.clear();
            });
          } else {
            binessProject.save({businessId: $scope.activebusiness.id}, $scope.project, function (data) {
              var project = {};
              angular.forEach(data, function(value,key) {
                if (key !== '$promise' && key !== '$resolved') {
                  project[key] = value;
                }
              });
              console.log(project);
              $scope.projects[$scope.projects.length] = project;
              console.log($scope.projects);
              $scope.clear();
            });
          }
        }
      };

      $scope.clear = function () {
        $scope.project = {
          
          "name": "",
          
          "description": "",
          
          "id": "",

          "hwsetupId": $scope.hwsetups[0].id,
        };
      };

      $scope.open = function (id) {
        var projectSave = $modal.open({
          templateUrl: 'project-save.html',
          controller: 'ProjectSaveController',
          size:'sm',
          windowClass: 'my-modal-popup',
          resolve: {
            project: function () {
              return $scope.project;
            },
            hwsetups: function() {
              return $scope.hwsetups;
            }
          }
        });

        projectSave.result.then(function (entity) {
          $scope.project = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('ProjectSaveController', ['$scope', '$modalInstance', 'project', 'hwsetups',
    function ($scope, $modalInstance, project, hwsetups) {
      $scope.project = project;
      $scope.hwsetups = hwsetups;
      console.log(project);

      

      $scope.ok = function () {
        $modalInstance.close($scope.project);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
