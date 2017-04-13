'use strict';

angular.module('app.auth').service('authService', ['$http', '$state', '$cookies', '$q', '$rootScope', 'usersService', 'localStorageService', 'DS', function($http, $state, $cookies, $q, $rootScope, usersService, localStorageService, DS){
    var _token = null;
    var _user = null;
    var _permissions = null;

    var _isAuthenticated = false;

    const rememer_me_days = 1000 * 60 * 60 * 24 * 7; // 7 days

    function createSession(token, user, permissions) {
        _token = token;
        setUser(user);
        _permissions = permissions;

        var expires = new Date();
        expires.setTime((new Date()).getTime() + rememer_me_days);
        $cookies.put('token', _token, {
            expires: expires,
        });

        _isAuthenticated = true;
        $rootScope.$broadcast('user-authenticated', _token);
    }

    function authenticate() {
        _isAuthenticated = false;
        var token = $cookies.get('token');
        $rootScope.$broadcast('user-authenticated', token);
        if (!token) {
            logout();
        }
        else {
            usersService.getLoggedUser(token).then(
                function(user){
                    createSession(token, user, user.permissions);
                },
                function(){
                    logout();
                }
            );
        }
    }

    /**
     * Login
     */
    function login(username, password) {
        var q = $q.defer();
        $http({
            url: 'auth',
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            data: {
                username: username,
                password: password,
            },
        }).then(
            function(data){
                // createSession(data.data.token, data.data.user, data.data.permissions);
                usersService.getLoggedUser(data.data.token).then(
                    function(user){
                        createSession(data.data.token, user, user.permissions);
                        q.resolve();
                    },
                    function(){
                        q.reject(data);
                        logout();
                    }
                );
            },
            function(data){
                q.reject(data);
            }
        );
        return q.promise;
    }

    /**
     * Logout
     */
    function logout(){
        var q = $q.defer();
        $http({
            url: 'auth',
            method: 'DELETE'
        }).then(
            function(data){
                _token = null;
                _isAuthenticated = false;

                $cookies.remove('token', _token);
                $cookies.remove('laravel_session', _token);
                setUser(null);
                _permissions = null;
                $cookies.remove('permissions', _permissions);
                $rootScope.$broadcast('user-unauthenticated');
                $state.go('login');
                DS.clear();
                q.resolve();
            },
            function(data){
                q.reject(data);
            }
        );
        return q.promise;
    }

    function getToken() {
        return _token;
    }

    function getUser() {
        return _user || localStorageService.get('currentUser');
    }

    function setUser(user) {
        _user = user;
        localStorageService.set('currentUser', user);
    }

    function isAllowed(permissions) {
        return _.isEmpty(permissions) || (!_.isEmpty(_user) && !_.isEmpty(_permissions) && _.intersection(permissions, _permissions).length);
    }

    function isAuthenticated(){
        return _isAuthenticated;
    }

    function can(permission) {
        if (!permission) return false;

        if (_.indexOf(_permissions, permission) != -1) return true;

        return false;
    }

    function resetPassword(data) {
        return $http({
            url: 'reset-password',
            method: 'POST',
            data: data
        }).then(function (res) {
            return res.data;
        })
    }

    $rootScope.$on('$stateChangeStart', function($e, state){
        if (!isAllowed(state.permissions)) {
            $e.preventDefault();
            $state.go('login');
        }
    });

    // init
    authenticate();

    return {
        login: login,
        logout: logout,
        getToken: getToken,
        getUser: getUser,
        isAllowed: isAllowed,
        can: can,
        authenticate: authenticate,
        isAuthenticated: isAuthenticated,
        resetPassword: resetPassword
    };
}]);
