'use strict';

angular.module('app.home').controller('ReportController', ['$scope', '$timeout', 'Upload', function ($scope, $timeout, Upload) {


    var ctrl = this;

    $scope.wizard1CompleteCallback = function(wizardData){
        // $scope.upload();

        $.smallBox({
            title: "Congratulations! Smart wizard finished",
            content: "<i class='fa fa-clock-o'></i> <i>1 seconds ago...</i>",
            color: "#5F895F",
            iconSmall: "fa fa-check bounce animated",
            timeout: 4000
        });
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
        // resizeObj: {width: 300, height: 100, centerCrop: true},
        postUrl:  '/services/upload-image',
        dimensionsFn: function($file, $width, $height){
            return $width < 12000 || $height < 12000;
        },
        // resizeIfFn: function($file, $width, $height){
        //     return $width > 600 || $height > 300;
        // }
    };

    $scope.upload = function () {
        ctrl.showWidget = false;
        ctrl.uploadCompleted = false;
        ctrl.inUploadProgress = true;
        $scope.inProgress = true;
        $timeout(function(){
            ctrl.showWidget = true;
            Upload.upload({
                // url: 'http://10.0.0.12:5000/api/upload',
                url: '/api/upload',
                data: {
                    file: ctrl.logoFile,
                    // date: ctrl.billDate,
                    // note: ctrl.billNote,
                    // amount: ctrl.billAmount
                }
            }).then(function (resp) {
                ctrl.uploadCompleted = true;
                ctrl.service.image_path = resp.data.image_path;
            }, function (resp) {
                $scope.inProgress = false;
            }, function (evt) {
                ctrl.progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
            });
        }, 500);
    };

}]);