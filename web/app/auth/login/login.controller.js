"use strict";

/*angular.module('app.auth').controller('loginController', ['$scope', '$state', 'authService', '$uibModalStack', '$rootScope', '$alert', '$translate', '$window', '$location','$http', function($scope, $state, authService, $uibModalStack, $rootScope, $alert, $translate, $window, $location, $http){
*/
    angular.module('app.auth').controller('loginController', ['$scope', '$timeout', '$http', '$state',
    function ($scope, $timeout, $http, $state) {
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
            $http.post('http://127.0.0.1:5000/api/login', { username: $scope.username, password: $scope.password })
                .success(function (response) {
                    // login successful if there's a token in the response
                    console.log(response)
                    if (response.token) {
                        console.log("token " + response.token)
                        //testing the token

                     /*var req = {
                     method: 'POST',
                     url: 'http://127.0.0.1:5000/api/test',
                     headers: {
                      'Content-Type' : 'application/json',
                      'token': response.token
                     }

                    }

                    $http(req).then(function(response){
                        console.log(response);
                    }, function(error){
                        console.log(error);
                    });*/
                        // store username and token in local storage to keep user logged in between page refreshes
//                        localStorage.currentUser = { username: $scope.username, token: response.token };
                        localStorage.setItem('currentUser', { username: $scope.username, token:response.token });
                        console.log(localStorage.getItem('currentUser').token);
//                        localStorage.currentUser = { username: $scope.username, token:response.token };
//                        console.log(localStorage.currentUser.username + " "+localStorage.currentUser.token );
//                        localStorage.user = { username: $scope.username, token: response.token };

                        // add jwt token to auth header for all requests made by the $http service
                        $http.defaults.headers.common.Authorization = 'Bearer ' + response.token;

                        //$state.go('app.home');

                    } else {
                        // show login error.
                    }
                });
        }


    $scope.logout = function Logout() {
            // remove user from local storage and clear http auth header
            delete $localStorage.currentUser;
            $http.defaults.headers.common.Authorization = '';
        }
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
