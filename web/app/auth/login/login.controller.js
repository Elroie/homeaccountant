"use strict";

angular.module('app.auth').controller('loginController', ['$scope', '$state', 'authService', '$uibModalStack', '$rootScope', '$alert', '$translate', '$window', '$location', function($scope, $state, authService, $uibModalStack, $rootScope, $alert, $translate, $window, $location){
    var ctrl = this;

    ctrl.email = '';
    ctrl.password = '';

    ctrl.loggingIn = false;

    $rootScope.$on('$locationChangeStart', function () {
        var openedModal = $uibModalStack.getTop();
        if (openedModal) {
            $uibModalStack.dismiss(openedModal.key);
        }
    });

    ctrl.login = function(){
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
    };

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
}]);
