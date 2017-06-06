'use strict';

angular.module('app.auth').service('authService', ['$http', '$state', '$cookies', '$q', '$rootScope', '$interval', function($http, $state, $cookies, $q, $rootScope, $interval){
    var _token = $cookies.get('token');
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
        if($state.current.name == 'login' || $state.current.name == 'register') return;
        _isAuthenticated = false;
        var token = $cookies.get('token');
        $rootScope.$broadcast('user-authenticated', token);
        if (!token) {
            logout();
        }
        else {
            // usersService.getLoggedUser(token).then(
            //     function(user){
            //         createSession(token, user, user.permissions);
            //     },
            //     function(){
            //         logout();
            //     }
            // );
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

        $cookies.remove('token');
        $rootScope.$broadcast('user-unauthenticated');
        $state.go('login');
        q.resolve();

        return q.promise;
    }

    function getToken() {
        return _token;
    }

    function getUser() {
        // return _user || localStorageService.get('currentUser');
    }

    function setUser(user) {
        _user = user;
        // localStorageService.set('currentUser', user);
    }

    function isAuthenticated(){
        return _isAuthenticated;
    }

    // init
    authenticate();

    var authCheck = $interval(authenticate, 500);

    return {
        login: login,
        logout: logout,
        getToken: getToken,
        getUser: getUser,
        authenticate: authenticate,
        isAuthenticated: isAuthenticated,
    };
}]);
