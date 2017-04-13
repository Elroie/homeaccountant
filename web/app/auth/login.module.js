'use strict';

angular.module('app.auth', ['ui.router']);

angular.module('app.auth').factory('xAuthTokenHttpInterceptor', ['$rootScope', function ($rootScope) {
    var _token = null;

    $rootScope.$on('user-authenticated', function($e, token){
        _token = token;
    });

    $rootScope.$on('user-unauthenticated', function(){
        _token = null;
    });

    return {
        request: function (config) {
            if(_token){
                config.headers['X-Auth-Token'] = _token;
            }

            return config;
        }
    };
}]);

angular.module('app.auth').config(['$stateProvider', '$httpProvider', function($stateProvider, $httpProvider){
    $httpProvider.interceptors.push('xAuthTokenHttpInterceptor');
    $stateProvider
        .state('login', {
            url: '/login',
            views: {
                root: {
                    templateUrl: 'smart/app/auth/views/login.html',
                    controller: 'loginController',
                    controllerAs: 'loginController',
                }
            },
            data: {
                title: 'Login',
                htmlId: 'extr-page'
            },
            resolve: {
                srcipts: function(lazyScript){
                    return lazyScript.register([
                        'smart/build/vendor.ui.js'
                    ]);
                }
            }
        })
        .state('forgotPassword', {
            url: '/forgot-password',
            views: {
                root: {
                    templateUrl: 'smart/app/auth/views/forgot-password.html',
                    controller: 'loginController',
                    controllerAs: 'ctrl'
                }
            },
            data: {
                title: 'Forgot Password',
                htmlId: 'extr-page'
            }
        })
        .state('lock', {
            url: '/lock',
            views: {
                root: {
                    templateUrl: 'smart/app/auth/views/lock.html'
                }
            },
            data: {
                title: 'Locked Screen',
                htmlId: 'lock-page'
            }
        })
    ;
}]);