'use strict';

angular.module('app.events').service('eventsService', ['$store', function($store){
    return $store('event')
        .endpoint('events')
        .timestamp('timestamp')
    ();
}]);
