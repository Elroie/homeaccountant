"use strict";

/*angular.module('app.auth').controller('loginController', ['$scope', '$state', 'authService', '$uibModalStack', '$rootScope', '$alert', '$translate', '$window', '$location','$http', function($scope, $state, authService, $uibModalStack, $rootScope, $alert, $translate, $window, $location, $http){
*/
    angular.module('app.auth').controller('loginController', ['$scope', '$timeout', '$http', function ($scope, $timeout, $http) {
    var ctrl = this;

    /*ctrl.username = '';
    ctrl.password = '';
    ctrl.loggingIn = false;*/

    $scope.account = {username:'',
    password:'',
    firstName:'',
    lastName: '',
    email:'',
    phone:'',
    country:'',
    city:'',
    address:'',
    homeType:'',
    homeSize:'',
    income:'',
    residence:''};


    /*$rootScope.$on('$locationChangeStart', function () {
        var openedModal = $uibModalStack.getTop();
        if (openedModal) {
            $uibModalStack.dismiss(openedModal.key);
        }
    });*/

   /* ctrl.login = function(){
        if (ctrl.loggingIn) return;
        ctrl.loggingIn = true;
        authService.login(ctrl.email, ctrl.password).then(
            function(data){
                $state.go('app.home');
                ctrl.loggingIn = false;
            },
            function(data){
                ctrl.loggingIn = false;
                $alert.error(data.data.message);
            }
        );
    };*/

    /*
    ctrl.resetInProgress = false;
    ctrl.resetPassword = function (form) {
        if(form.$invalid) return;
        ctrl.resetInProgress = true;
        authService.resetPassword({email: ctrl.email}).then(function (res) {
            ctrl.resetInProgress = false;
            if(res.send) {
                $alert.info($translate.instant('layout.reset_password.is_send')).then(function () {
                    $location.path('/');
                })

            } else {
                $alert.info(res.code);
            }
        }, function (res) {
            ctrl.resetInProgress = false;
            $alert.info(res.data.message);
        })
    };
    */

   $scope.register = function register (){
        var req = {
         method: 'POST',
         url: 'http://127.0.0.1:5000/api/register',
         headers: {
          'Content-Type' : 'application/json'
         },
         data: { "account"  : $scope.account }
        }

        $http(req).then(function(response){
            console.log(response);
        }, function(error){
            console.log(error);
        });
    };
}]);
