'use strict';

angular.module('app.home').controller('ManageReportsController', ['$scope', '$timeout', '$http', function ($scope, $timeout, $http) {


    $http({
        method : "GET",
        url : "http://127.0.0.1:5000/api/reports"
        }).then(function mySuccess(response) {
            console.log(response.data);
            $scope.reports = response.data[0];
        }, function myError(response) {
            $scope.error = response.statusText;
        });


}]);