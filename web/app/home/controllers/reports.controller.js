'use strict';

angular.module('app.home').controller('ManageReportsController', ['$scope', '$timeout', '$http','$cookies', function ($scope, $timeout, $http,$cookies) {


    $scope.user=$cookies.get('token');

    $http({
        method : "GET",
        url : "/api/reports"
        }).then(function mySuccess(response) {
            console.log(response.data);
            $scope.reports = response.data[0];
        }, function myError(response) {
            $scope.error = response.statusText;
        });


}]);