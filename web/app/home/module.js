"use strict";


angular.module('app.home', ['ui.router'])
.config(function ($stateProvider) {

    $stateProvider
        .state('app.home', {
            url: '/home',
            data: {
                title: 'Blank'
            },
            views: {
                "content@app": {
                    templateUrl: 'app/home/views/home.html',
                    controller: 'HomeController',
                    controllerAs: 'ctrl'
                }
            }
        })
        .state('app.upload', {
            url: '/upload',
            data: {
                title: 'New Report'
            },
            views: {
                "content@app": {
                    templateUrl: 'app/home/views/upload.html',
                    controller: 'ReportController',
                    controllerAs: 'ctrl'
                }
            }
        })
        .state('app.statistics', {
            url: '/statistics',
            data: {
                title: 'Statistics'
            },
            views: {
                "content@app": {
                    templateUrl: 'app/home/views/statistics.html',
                    controller: 'StatisticsController',
                    controllerAs: 'ctrl'
                }
            }
        })
        .state('app.reports', {
            url: '/reports',
            data: {
                title: 'Manage Reports'
            },
            views: {
                "content@app": {
                    templateUrl: 'app/home/views/reports.html',
                    controller: 'ManageReportsController',
                    controllerAs: 'ctrl'
                }
            }
        })
        .state('app.settings', {
            url: '/settings',
            data: {
                title: 'Settings'
            },
            views: {
                "content@app": {
                    templateUrl: 'app/home/views/settings.html',
                    controller: 'SettingsController',
                    controllerAs: 'ctrl'
                }
            }
        })
        .state('app.about', {
            url: '/about',
            data: {
                title: 'Contact Us'
            },
            views: {
                "content@app": {
                    templateUrl: 'app/home/views/about.html',
                    controller: 'AboutController',
                    controllerAs: 'ctrl'
                }
            }
        })
        .state('app.report_type', {
            url: '/reports-list',
            data: {
                title: 'Electricity Reports'
            },
            views: {
                "content@app": {
                    templateUrl: 'app/home/views/report-type.html',
                    controller: 'ReportTypeController',
                    controllerAs: 'ctrl'
                }
            }
        })
});
