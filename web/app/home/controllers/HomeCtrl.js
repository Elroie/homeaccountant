'use strict';

angular.module('app.home').controller('HomeController', ['$scope', '$timeout', '$http', '$state', function ($scope, $timeout, $http, $state) {

   $http({
        method : "GET",
        url : "http://127.0.0.1:5000/api/note/allnotes"
        }).then(function mySucces(response) {
            console.log(response.data);
            $scope.notes = response.data;
        }, function myError(response) {
            $scope.error = response.statusText;
        });

    $http({
        method : "GET",
        url : "http://127.0.0.1:5000/api/statusbar"
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