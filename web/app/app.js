'use strict';

/**
 * @ngdoc overview
 * @name app [smartadminApp]
 * @description
 * # app [smartadminApp]
 *
 * Main module of the application.
 */

angular.module('app', [
    'ngSanitize',
    'ngAnimate',
    'ngCookies',
    'restangular',
    'ui.router',
    'ui.bootstrap',
    'ngFileUpload',

    // Smartadmin Angular Common Module
    'SmartAdmin',

    // App
    'app.auth',

    'app.layout',
    //'app.chat',
    //'app.dashboard',
    //'app.calendar',
    //'app.inbox',
    'app.graphs',
    'app.tables',
    'app.forms',
    'app.ui',
    'app.widgets',
    //'app.maps',
    //'app.appViews',
    //'app.misc',
    'app.smartAdmin',
    //'app.eCommerce'
    'app.home'
])
.config(function ($provide, $httpProvider, RestangularProvider) {


    // Intercept http calls.
    $provide.factory('ErrorHttpInterceptor', function ($q, $rootScope) {
        var errorCounter = 0;
        function notifyError(rejection){
            console.log(rejection);
            $.bigBox({
                title: rejection.status + ' ' + rejection.statusText,
                content: rejection.data,
                color: "#C46A69",
                icon: "fa fa-warning shake animated",
                number: ++errorCounter,
                timeout: 6000
            });

        }

        return {
            // On request failure
            requestError: function (rejection) {
                // show notification
                notifyError(rejection);

                // Return the promise rejection.
                return $q.reject(rejection);
            },

            // On response failure
            responseError: function (rejection) {
                if (rejection.status === 401) {
                    $rootScope.logout();
                }else{
                    // show notification
                    notifyError(rejection);
                }
                // Return the promise rejection.
                return $q.reject(rejection);
            }
        };
    });

    // Add the interceptor to the $httpProvider.
    $httpProvider.interceptors.push('ErrorHttpInterceptor');

    RestangularProvider.setBaseUrl(location.pathname.replace(/[^\/]+?$/, ''));

})
.constant('APP_CONFIG', window.appConfig)

.run(['$rootScope', '$state', '$stateParams','$http','$cookies','$window', 'authService',
function ($rootScope, $state, $stateParams,$http,$cookies,$window, authService) {


    $rootScope.logout = function () {
        authService.logout();
    };

    $rootScope.$state = $state;
    $rootScope.$stateParams = $stateParams;
    //editableOptions.theme = 'bs3';
    //Omer enable below


}]);


