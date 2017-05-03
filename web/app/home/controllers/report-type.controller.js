'use strict';

angular.module('app.home').controller('ReportTypeController', ['$scope', '$timeout', '$uibModal', function ($scope, $timeout, $uibModal) {


    var ctrl = this;



    $scope.openBill = function (billId) {

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
                    return 'http://127.0.0.1:8888/resources/test1.jpg'
                }
            }
        });

        return modalInstance.result;


    };



}]);