var app=angular.module("app", ["chart.js","ui.grid"])

app.controller("LineCtrl", function ($scope) {

    $scope.labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24];
    $scope.series = ['yesterday', 'today'];
    $scope.data = [
        [65, 59, 80, 81, 56, 55, 40,10,30,20,40,50,60,80,20,19,49,50,30,32,34,64,52,13],
        [28, 48, 40, 19, 86, 27, 90]
    ];
    $scope.onClick = function (points, evt) {
        console.log(points, evt);
    };
});

app.controller("LineCtrl1", function ($scope, $http) {

    $scope.labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24];
    $scope.series = ['yesterday', 'today'];
    $scope.data = [
        [65, 59, 80, 81, 56, 55, 40,10,30,20,40,50,60,80,20,19,49,50,30,32,34,64,52,13],
        [28, 48, 40, 19, 86, 27, 90]
    ];

    //$scope.data = '/data.php';ppppppppppppppppp

    //$http.get('/data.php').
    //    success(function(data, status, headers, config) {
    //        $scope.data = data;
    //    }).
    //    error(function(data, status, headers, config) {
    //        // log error
    //    });
    $scope.onClick = function (points, evt) {
        console.log(points, evt);
    };
});

app.controller("LineCtrl2", function ($scope, $http) {

    $scope.labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24];
    $scope.series = ['yesterday', 'today'];
    $scope.data = [
        [65, 59, 80, 81, 56, 55, 40,10,30,20,40,50,60,80,20,19,49,50,30,32,34,64,52,13],
        [28, 48, 40, 19, 86, 27, 90]
    ];

    //$scope.data = '/data.php';ppppppppppppppppp

    //$http.get('/data.php').
    //    success(function(data, status, headers, config) {
    //        $scope.data = data;
    //    }).
    //    error(function(data, status, headers, config) {
    //        // log error
    //    });
    $scope.onClick = function (points, evt) {
        console.log(points, evt);
    };
});

app.controller('Table1', function($scope) {
    $scope.myData = [{name: "Moroni", age: 50},
        {name: "Tiancum", age: 43},
        {name: "Jacob", age: 27},
        {name: "Nephi", age: 29},
        {name: "Enos", age: 34}];
    $scope.gridOptions = {
        data: 'myData',
        columnDefs: [{field:'name', displayName:'Name'}, {field:'age', displayName:'Age'}]
    };
});
