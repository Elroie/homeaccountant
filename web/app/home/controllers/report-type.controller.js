'use strict';

angular.module('app.home').controller('ReportTypeController', ['$scope', '$timeout', '$uibModal','$stateParams','$rootScope','$http', function ($scope, $timeout, $uibModal,$stateParams,$rootScope,$http) {


    var ctrl = this;
    var typeid = $stateParams.type;
    $scope.typeid = typeid;
    console.log(typeid)
    //$rootScope.reports
     if (typeid == "Electricity Bill"){
        $scope.report_list = $rootScope.reports['Electricity Bill'];
     }
     else if (typeid == "Water Bill") {
        $scope.report_list = $rootScope.reports['Water Bill'];
     }
     else{
        $scope.report_list = $rootScope.reports['General'];
     }

    $scope.openBill = function (image) {


        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: '/app/home/views/bill.html',
            controller: function ($scope, billUrl) {
                $scope.billUrl = billUrl;

            },
            controllerAs: 'ctrl',
            size: 'lg',
            appendTo: undefined,
            resolve: {
                billUrl: function () {
                    return 'api/bills/' + image
                }
            }
        });

        return modalInstance.result;




    };





}]);