'use strict';

angular.module('app.home').controller('HomeController', ['$scope', '$timeout', '$http', function ($scope, $timeout, $http) {

   $http({
        method : "GET",
        url : "http://127.0.0.1:5000/api/note/allnotes"
        }).then(function mySucces(response) {
            console.log(response.data);
            $scope.notes = response.data;
        }, function myError(response) {
            $scope.error = response.statusText;
        });


}]);