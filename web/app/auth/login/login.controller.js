"use strict";

/*angular.module('app.auth').controller('loginController', ['$scope', '$state', 'authService', '$uibModalStack', '$rootScope', '$alert', '$translate', '$window', '$location','$http', function($scope, $state, authService, $uibModalStack, $rootScope, $alert, $translate, $window, $location, $http){
*/
    angular.module('app.auth').controller('loginController', ['$scope', '$timeout', '$http', '$state','$rootScope',
    function ($scope, $timeout, $http, $state, $rootScope) {
    var ctrl = this;

    $scope.username = '';
    $scope.password = '';
    //ctrl.loggingIn = false;

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

    $scope.login = function Login(username, password) {
            console.log("login function...")
            console.log($scope.username + " " + $scope.password)
            $http.post('/api/login', { username: $scope.username, password: $scope.password })
                .success(function (response) {
                    // login successful if there's a token in the response
                    console.log(response)
                    if (response.token) {
                        console.log("token " + response.token)

                        $rootScope.$broadcast('user-authenticated',response.token,$scope.username)
                        $state.go('app.home');

                    } else {
                        // show login error.
                    }
                });
        }


    $scope.logout = function Logout() {
            // remove user from local storage and clear http auth header
            $rootScope.$broadcast('user-unauthenticated');
        }
   $scope.register = function register (){
        var req = {
         method: 'POST',
         url: '/api/register',
         headers: {
          'Content-Type' : 'application/json'
         },
         data: { "account"  : $scope.account }
        }

        $http(req).then(function(response){
            console.log(response);
            $state.go('login');
        }, function(error){
            console.log(error);
        });
    };
}]);
