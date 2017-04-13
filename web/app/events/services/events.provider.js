'use strict';

angular.module('app.events').provider('$events', [function(){
    // var listeners = {};

    // function emit(event) {

    // }

    // function listen(event, callback) {
    //     listeners[event]
    //     listeners[event].push(callback);       
    // }
    var _config = {
        pollingInterval: 10000,
    };

    return {
        setConfig: function(config) {
            _config = angular.extend(_config, config);
        },
        $get: ['eventsService', '$rootScope', '$interval', function(eventsService, $rootScope, $interval){            
            var last_event_id = null;

            var pollingInterval = null;

            function poll() {
                eventsService.findAll({limit: 10, id__gt: last_event_id}, {bypassCache: true}).then(function(events){
                    _.each(events, function(event){
                        var namespace = event.name.substr(0, event.name.indexOf('.')) + '.*';
                        $rootScope.$broadcast(namespace, event.payload);
                        $rootScope.$broadcast(event.name, event.payload);
                        last_event_id = event.id;
                    });
                });
            }

            function start() {
                if (last_event_id) {
                    pollingInterval = $interval(poll, _config.pollingInterval);
                }
                else {
                    eventsService.findAll({limit: 1, sort: 'DESC'}, {bypassCache: true}).then(function(events){
                        if (events.length) {
                            last_event_id = events[0].id;
                        }
                        pollingInterval = $interval(poll, _config.pollingInterval);
                    });
                }
            }

            function stop() { 
                $interval.cancel(pollingInterval);
                pollingInterval = null;
            }

            $rootScope.$on('user-authenticated', function(){
                start();
            });

            $rootScope.$on('user-unauthenticated', function(){
                stop();
            });

            return {
                // emit: emit,
                // listen: listen,
            };
        }],
    };
}]);
