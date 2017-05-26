'use strict';

angular.module('app.graphs').directive('chartjsDoughnutChart',['$http', function ($http) {

    var graphdata;

    return {
        restrict: 'A',
        link: function (scope, element, attributes) {
        $http({
            method : "GET",
            url : "http://127.0.0.1:5000/api/graph/getdata"
            }).then(function mySuccess(response) {
                console.log(response.data);
                graphdata = response.data[0];
                console.log(graphdata.electricity_price);

                var doughnutOptions = {
                //Boolean - Whether we should show a stroke on each segment
                segmentShowStroke : true,
                //String - The colour of each segment stroke
                segmentStrokeColor : "#fff",
                //Number - The width of each segment stroke
                segmentStrokeWidth : 2,
                //Number - The percentage of the chart that we cut out of the middle
                percentageInnerCutout : 50, // This is 0 for Pie charts
                //Number - Amount of animation steps
                animationSteps : 100,
                //String - Animation easing effect
                animationEasing : "easeOutBounce",
                //Boolean - Whether we animate the rotation of the Doughnut
                animateRotate : true,
                //Boolean - Whether we animate scaling the Doughnut from the centre
                animateScale : false,
                //Boolean - Re-draw chart on page resize
                responsive: true,
                //String - A legend template
                legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>"
            };

                var doughnutData = [
                    {

                        value: graphdata.electricity_price,
                        color:"rgba(220,220,0,0.5)",
                        highlight: "rgba(220,220,0,0.3)",
                        label: "Electricity"
                    },
                    {
                        value: graphdata.water_price,
                        color: "rgba(151,187,205,1)",
                        highlight: "rgba(151,187,205,0.4)",
                        label: "Water"
                    },
                    {
                        value: graphdata.other_price,
                        color: "rgba(169, 3, 41, 0.7)",
                        highlight: "rgba(169, 3, 41, 0.4)",
                        label: "Other"
                    }
                ];

                // render chart
                var ctx = element[0].getContext("2d");
                new Chart(ctx).Doughnut(doughnutData, doughnutOptions);
            }, function myError(response) {
                $scope.error = response.statusText;
            });
        }}
}]);