'use strict';

angular.module('app.home').controller('ManageReportsController', ['$scope', '$timeout', '$http', function ($scope, $timeout, $http) {


    $http({
        method : "POST",
        url : "/api/reports"
        }).then(function mySuccess(response) {
            console.log(response.data);
            $scope.reports = response.data;
        }, function myError(response) {
            $scope.error = response.statusText;
        });


}]);