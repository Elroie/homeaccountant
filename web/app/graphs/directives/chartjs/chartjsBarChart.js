'use strict';

angular.module('app.graphs').directive('chartjsBarChart',['$http', function ($http) {

    var graphdata;

    return {
        restrict: 'A',
        link: function (scope, element, attributes) {
        $http({
            method : "GET",
            url : "/api/graph/totalexpense"
            }).then(function mySuccess(response) {

                graphdata = response.data;

                var barOptions = {
                    //Boolean - Whether the scale should start at zero, or an order of magnitude down from the lowest value
                    scaleBeginAtZero : true,
                    //Boolean - Whether grid lines are shown across the chart
                    scaleShowGridLines : true,
                    //String - Colour of the grid lines
                    scaleGridLineColor : "rgba(0,0,0,.05)",
                    //Number - Width of the grid lines
                    scaleGridLineWidth : 1,
                    //Boolean - If there is a stroke on each bar
                    barShowStroke : true,
                    //Number - Pixel width of the bar stroke
                    barStrokeWidth : 1,
                    //Number - Spacing between each of the X value sets
                    barValueSpacing : 5,
                    //Number - Spacing between data sets within X values
                    barDatasetSpacing : 1,
                    //Boolean - Re-draw chart on page resize
                    responsive: true,
                    //String - A legend template
                    legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].lineColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"
                }

                var barData = {
                    labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November","December"],
                    datasets: [
                       /* {
                            label: "My First dataset",
                            fillColor: "rgba(220,220,220,0.5)",
                            strokeColor: "rgba(220,220,220,0.8)",
                            highlightFill: "rgba(220,220,220,0.75)",
                            highlightStroke: "rgba(220,220,220,1)",
                            data: [65, 59, 80, 81, 56, 55, 40]
                        },*/
                        {
                            label: "My Second dataset",
                            fillColor: "rgba(151,187,205,0.5)",
                            strokeColor: "rgba(151,187,205,0.8)",
                            highlightFill: "rgba(151,187,205,0.75)",
                            highlightStroke: "rgba(151,187,205,1)",
                       //     data: [graphdata[0], graphdata[1], graphdata[2], graphdata[3], graphdata[4], graphdata[5], graphdata[6],graphdata[7], graphdata[8], graphdata[9], graphdata[10], graphdata[11],]
                            data: graphdata
                        }
                    ]
                };

                var ctx = element[0].getContext("2d");
                new Chart(ctx).Bar(barData, barOptions);
            }, function myError(response) {
               $scope.error = response.statusText;
            });
        }}
}]);