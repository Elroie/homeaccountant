'use strict';

angular.module('app.home').controller('AboutController', ['$scope', '$timeout', '$http', function ($scope, $timeout, $http) {


   var ctrl = this;
   $http({
        method : "GET",
        url : "http://127.0.0.1:5000/api/note/allnotes"
        }).then(function mySucces(response) {
            console.log(response);
            ctrl.notes = response.data;
        }, function myError(response) {
            $scope.error = response.statusText;
        });


}]);