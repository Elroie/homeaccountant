'use strict';

angular.module('app.home').controller('HomeController', ['$scope', '$timeout', '$http', '$state','$cookies', function ($scope, $timeout, $http, $state,$cookies) {

    $scope.user = $cookies.get('username');
   $http({
        method : "GET",
        url : "/api/note/allnotes"
        }).then(function mySucces(response) {
            console.log(response.data);
            $scope.notes = response.data;
        }, function myError(response) {
            $scope.error = response.statusText;
        });

    $http({
        method : "GET",
        url : "/api/statusbar"
        }).then(function mySucces(response) {
            console.log(response.data);
            $scope.bardata = response.data;
        }, function myError(response) {
            $scope.error = response.statusText;
        });
    $scope.goToSettings=function(){
        $state.go('app.settings');
    };

    $scope.goToReports=function(){
            $state.go('app.reports');
    };
}]);