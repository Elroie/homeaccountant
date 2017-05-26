'use strict';

angular.module('app.auth', ['ui.router']);

angular.module('app.auth').factory('xAuthTokenHttpInterceptor', ['$rootScope', '$cookies', function ($rootScope, $cookies) {
    var _token = null;

    $rootScope.$on('user-authenticated', function($e, token){
        _token = token;
        //localStorage.token = token;
        $cookies.put('token', _token);
    });

      if ($cookies.get('token')) {
            _token = $cookies.get('token');
        }
    $rootScope.$on('user-unauthenticated', function(){
        _token = null;
    });

    return {
        request: function (config) {
            if(_token){
                config.headers['token'] = _token;
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
                    templateUrl: 'app/auth/views/login.html',
                    controller: 'loginController',
                    controllerAs: 'loginController',
                }
            },
            data: {
                title: 'Login',
                htmlId: 'extr-page'
            }
        })
        .state('register', {
            url: '/register',
            views: {
                root: {
                    templateUrl: 'app/auth/views/register.html',
                    controller: 'loginController',
                    controllerAs: 'loginController',
                }
            },
            data: {
                title: 'Login',
                htmlId: 'extr-page'
            }
        })
        .state('forgotPassword', {
            url: '/forgot-password',
            views: {
                root: {
                    templateUrl: 'app/auth/views/forgot-password.html',
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
                    templateUrl: 'app/auth/views/lock.html'
                }
            },
            data: {
                title: 'Locked Screen',
                htmlId: 'lock-page'
            }
        })
    ;
}]);
