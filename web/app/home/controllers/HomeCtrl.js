'use strict';

angular.module('app.home').controller('HomeController', ['$scope', '$timeout', 'Upload', function ($scope, $timeout, Upload) {


    var ctrl = this;

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

    ctrl.upload = function () {
        ctrl.showWidget = false;
        ctrl.uploadCompleted = false;
        ctrl.inUploadProgress = true;
        $timeout(function(){
            debugger;
            ctrl.showWidget = true;
            Upload.upload({
                // url: 'http://10.0.0.12:5000/api/upload',
                url: 'http://127.0.0.1:5000/api/upload',
                data: {file: ctrl.logoFile}
            }).then(function (resp) {
                ctrl.uploadCompleted = true;
                ctrl.service.image_path = resp.data.image_path;
            }, function (resp) {

            }, function (evt) {
                ctrl.progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
            });
        }, 500);
    };

}]);