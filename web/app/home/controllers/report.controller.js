'use strict';

angular.module('app.home').controller('ReportController', ['$scope', '$timeout', 'Upload', '$interval', '$http', function ($scope, $timeout, Upload, $interval, $http) {


    var ctrl = this;

    var pollingInterval = null;

    $scope.billAmount = null;
    $scope.billDate = null;
    $scope.billNote = null;
    $scope.imageId = null;

    var pollLimit = 30;
    var sessionHash = null;

    $scope.wizard1CompleteCallback = function(wizardData){
        // $scope.upload();
        update();

        $.smallBox({
            title: "Congratulations! Smart wizard finished",
            content: "<i class='fa fa-clock-o'></i> <i>1 seconds ago...</i>",
            color: "#5F895F",
            iconSmall: "fa fa-check bounce animated",
            timeout: 4000
        });
    };

    $scope.callbacks = {
        1: function () {
            $scope.upload();
        }
    };

    ctrl.progressPercentage = 0;
    ctrl.logoFile = null;
    ctrl.showWidget = false;
    ctrl.uploadCompleted = false;
    ctrl.inUploadProgress = false;
    ctrl.image_path = null;

    ctrl.logoType = {
        allowedFileType: '.image/*,.jpg,.jpeg,.gif,.png',
        accept: 'image/*',
    };

    $scope.selectFile = function ($files, $file, $newFiles, $duplicateFiles, $invalidFiles, $event) {
        ctrl.image_path = $file.name;
    };

    $scope.upload = function () {
        start();
        ctrl.showWidget = false;
        ctrl.uploadCompleted = false;
        ctrl.inUploadProgress = true;
        $scope.inProgress = true;

        sessionHash = $.now();

        return Upload.upload({
            url: '/api/upload',
            data: {
                file: ctrl.logoFile,
                uniqueId: sessionHash
            }
        }).then(function (resp) {
            ctrl.uploadCompleted = true;
            $scope.inProgress = false;
        }, function (resp) {
            $scope.inProgress = false;
            stop();
        }, function (evt) {
            ctrl.progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
        });
    };

    function poll() {
        if(pollLimit <= 0){
            stop();
            return;
        }

        pollLimit -= 1;

        $scope.billAmount = null;
        $scope.billDate = null;

        $http({
            method : "GET",
            url : "/api/scanned-images",
            params: {status: 'pending', user: 'currentUser', uniqueId: sessionHash}
        }).then(function mySuccess(response) {
            if (!response.data.scanned_images.length) return;

            $scope.imageId = response.data.scanned_images[0].id;
            $scope.billAmount = response.data.scanned_images[0].price;
            $scope.billDate = new Date(response.data.scanned_images[0].to_date);
            stop();
        }, function myError(response) {

        });

    }

    function update() {
        $http({
            method : "PUT",
            url : "/api/scanned-images/" + sessionHash,
            data: {
                billNote: $scope.billNote,
                billAmount: $scope.billAmount,
                billDate: $scope.billDate,
                imageId: $scope.imageId,
            }
        }).then(function mySuccess(response) {

        }, function myError(response) {

        });

    }

    $scope.watingForOcr = false;
    function start() {
        $scope.watingForOcr = true;
        pollingInterval = $interval(poll, 1000);
    }

    function stop() {
        $scope.watingForOcr = false;
        $interval.cancel(pollingInterval);
        pollingInterval = null;
    }
}]);