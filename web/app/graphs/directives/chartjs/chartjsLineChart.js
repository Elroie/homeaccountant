'use strict';

angular.module('app.graphs').directive('chartjsLineChart', ['$http', function ($http) {

    var graphdata;

    return {
        restrict: 'A',
        link: function (scope, element, attributes) {
        $http({
            method : "GET",
            url : "/api/graph/getdata"
            }).then(function mySuccess(response) {

                graphdata = response.data;

                // LINE CHART
                // ref: http://www.chartjs.org/docs/#line-chart-introduction
                var lineOptions = {
                    ///Boolean - Whether grid lines are shown across the chart
                    scaleShowGridLines : true,
                    //String - Colour of the grid lines
                    scaleGridLineColor : "rgba(0,0,0,.05)",
                    //Number - Width of the grid lines
                    scaleGridLineWidth : 1,
                    //Boolean - Whether the line is curved between points
                    bezierCurve : true,
                    //Number - Tension of the bezier curve between points
                    bezierCurveTension : 0.4,
                    //Boolean - Whether to show a dot for each point
                    pointDot : true,
                    //Number - Radius of each point dot in pixels
                    pointDotRadius : 4,
                    //Number - Pixel width of point dot stroke
                    pointDotStrokeWidth : 1,
                    //Number - amount extra to add to the radius to cater for hit detection outside the drawn point
                    pointHitDetectionRadius : 20,
                    //Boolean - Whether to show a stroke for datasets
                    datasetStroke : true,
                    //Number - Pixel width of dataset stroke
                    datasetStrokeWidth : 2,
                    //Boolean - Whether to fill the dataset with a colour
                    datasetFill : true,
                    //Boolean - Re-draw chart on page resize
                    responsive: true,
                    //String - A legend template
                    legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].lineColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"
                };

                var lineData = { labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November","December"],
                    datasets: [
                        {
                            label: "Electricity",
                            fillColor: "rgba(220,220,0,0.2)",
                            strokeColor: "rgba(220,220,0,1)",
                            pointColor: "rgba(220,220,0,1)",
                            pointStrokeColor: "#fff",
                            pointHighlightFill: "#fff",
                            pointHighlightStroke: "rgba(220,220,0,1)",
                            data: [graphdata[0].electricity_price, graphdata[1].electricity_price, graphdata[2].electricity_price, graphdata[3].electricity_price, graphdata[4].electricity_price, graphdata[5].electricity_price, graphdata[6].electricity_price,graphdata[7].electricity_price,graphdata[8].electricity_price,graphdata[9].electricity_price,graphdata[10].electricity_price,graphdata[11].electricity_price]
                        },
                        {
                            label: "Water",
                            fillColor: "rgba(151,187,205,0.2)",
                            strokeColor: "rgba(151,187,205,1)",
                            pointColor: "rgba(151,187,205,1)",
                            pointStrokeColor: "#fff",
                            pointHighlightFill: "#fff",
                            pointHighlightStroke: "rgba(151,187,205,1)",
                            data: [graphdata[0].water_price, graphdata[1].water_price, graphdata[2].water_price, graphdata[3].water_price, graphdata[4].water_price, graphdata[5].water_price, graphdata[6].water_price,graphdata[7].water_price,graphdata[8].water_price,graphdata[9].water_price,graphdata[10].water_price,graphdata[11].water_price]
                        },
                        {
                            label: "Other",
                            fillColor: "rgba(169, 3, 41,0.2)",
                            strokeColor: "rgba(169, 3, 41,1)",
                            pointColor: "rgba(169, 3, 41,1)",
                            pointStrokeColor: "#fff",
                            pointHighlightFill: "#fff",
                            pointHighlightStroke: "rgba(169, 3, 41,1)",
                            data: [graphdata[0].other_price, graphdata[1].other_price, graphdata[2].other_price, graphdata[3].other_price, graphdata[4].other_price, graphdata[5].other_price, graphdata[6].other_price, graphdata[7].other_price,graphdata[8].other_price,graphdata[9].other_price,graphdata[10].other_price,graphdata[11].other_price]
                        }
                    ]
                };

                var ctx = element[0].getContext("2d");
                var myNewChart = new Chart(ctx).Line(lineData, lineOptions);

            }, function myError(response) {
               $scope.error = response.statusText;
            });

        }
    }
}]);