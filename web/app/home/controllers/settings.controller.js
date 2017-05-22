'use strict';

angular.module('app.home').controller('SettingsController', ['$scope', '$timeout', '$http', function ($scope, $timeout, $http) {

    var ctrl = this;
    ctrl.countries = [{name: 'Israel', value: 1}, {name: 'United States', value: 2}];

    $http({
        method : "GET",
        url : "http://127.0.0.1:5000/api/user/settings"
        }).then(function mySucces(response) {
            ctrl.account = response.data;
            ctrl.accountToUpdate = {};
            angular.copy(ctrl.account, ctrl.accountToUpdate);
        }, function myError(response) {
            $scope.error = response.statusText;
        });

    ctrl.updateSettings = function(){
        console.log('update....');
        var req = {
         method: 'POST',
         url: 'http://127.0.0.1:5000/api/user/update',
         headers: {
          'Content-Type' : 'application/json'
         },
         data: { account: ctrl.accountToUpdate }
        }

        $http(req).then(function(response){
            console.log(response);
        }, function(error){
            console.log(error);
        });
    };

    ctrl.cancel = function(){
        // clear all changes and set the account with his current values.
        angular.copy(ctrl.account, ctrl.accountToUpdate);
    };
}]);