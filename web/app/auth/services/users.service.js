'use strict';

angular.module('app.auth').service('usersService', ['$store', '$http', '$uibModal', function($store, $http, $uibModal){
    var store = $store('user')
        .endpoint('users')
        .timestamps()
        .method.get('getPermissions', 'permissions')
        .count()
        ();

    store.getLoggedUser = function(token) {
        var params = {};
        if(token){
            params.auth_token = token;
        }
        return $http({
            url: '/users/logged_user',
            method: 'GET',
            params: params
        }).then(
            function(data){
                return store.inject(data.data);
            });
    };

    store.getOnlineUsers = function() {
        return $http({
            url: 'users/active_users/count',
            method: 'GET'
        }).then(function (res) {
            return res.data.count;
        });
    };

    store.forceLogout = function (user_id) {
        return $http({
            method: 'GET',
            url: 'auth/force_logout',
            params: {user_id: user_id}
        }).then(function (res) {
            return res.data;
        })
    };

    store.getOnlineUsersList = function() {
        return $http({
            url: 'users/active_users/list',
            method: 'GET'
        }).then(function (res) {
            return res.data;
        });
    };

    store.getPermissionsRoles = function() {
        return $http({
            method: 'GET',
            url: '/users/get-permissions-roles'
        }).then(function(data){
            return data.data;
        })
    };

    store.checkAvailabilityForActiveUsers = function () {
        return $http({
            method: 'GET',
            url: 'users/check-active-users-limit'
        })
    };

    store.updatePermissions = function(data) {
        return $http({
            method: 'POST',
            url: '/sync_permission',
            data: data
        })
    };

    store.getAllAgents = function() {
        return $http({
            method: 'GET',
            url: 'users/get-all-agents'
        }).then(function(data) {
            var agents = data.data.agents;
            var agent = [];
            var i = 0;
            _.each(agents, function(res, key) {
                agent[i++] = {
                    id: key,
                    name: res
                }
            });
            return agent;
        })
    };

    store.getAllInstitutes = function(){
        return $http({
            method: 'GET',
            url: 'users/get-all-institutes'
        }).then(function(data) {
            var institutes = data.data;
            var institute = [];
            var i = 0;
            _.each(institutes, function(res, key) {
                institute[i++] = {
                    id: key,
                    name: res
                }
            });
            return institute;
        })
    };

    store.getUserRoles = function (user_id) {
        return $http({
            method: 'GET',
            url: '/users/user-roles/' + user_id,
        }).then(function(data) {
            return data;
        })
    };

    store.getAgentByUserId = function(user_id){
        return $http({
            method: 'GET',
            url: 'users/user-agents/' + user_id,
        })
    };

    store.getInstitutesByUserId = function(user_id){
        return $http({
            method: 'GET',
            url: 'users/user-institutes/' + user_id,
        })
    };

    store.openNewUser = function (current_project_id) {
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: '/app/modules/settings/templates/new-user.template.html',
            controller: 'newUserController',
            controllerAs: 'ctrl',
            size: 'md',
            appendTo: undefined,
            resolve: {
                current_project_id: function () {
                    return current_project_id;
                }
            }
        });

        return modalInstance.result;
    };

    store.openEditUser = function (user) {
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: '/app/modules/settings/templates/new-user.template.html',
            controller: 'userEditController',
            controllerAs: 'ctrl',
            size: 'md',
            appendTo: undefined,
            resolve: {
                user: function () {
                    return user;
                }
            }
        });

        return modalInstance.result;
    };

    store.openRoles = function () {
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: '/app/modules/settings/templates/user-roles.template.html',
            controller: 'userRolesController',
            controllerAs: 'ctrl',
            size: 'md',
            appendTo: undefined,
        });

        return modalInstance.result;
    };

    store.openPermission = function () {
        var modalInstance = $uibModal.open({
            animation: true,
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: '/app/modules/settings/templates/user-permission.template.html',
            controller: 'userPermissionsController',
            controllerAs: 'ctrl',
            size: 'lg',
            appendTo: undefined,
        });

        return modalInstance.result;
    };


    return store;
}]);
