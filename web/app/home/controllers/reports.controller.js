'use strict';

angular.module('app.home').controller('ManageReportsController', ['$scope', '$timeout', '$http','$cookies', function ($scope, $timeout, $http,$cookies) {


    $scope.user=$cookies.get('token');

    $http({
        method : "POST",
        url : "/api/reports"
        }).then(function mySuccess(response) {
            console.log(response.data);
            $scope.reports = response.data;
            /*for (var key in $scope.reports){
                console.log(key + " " + $scope.reports[key][0].user_id)
            }*/
        }, function myError(response) {
            $scope.error = response.statusText;
        });


}]);