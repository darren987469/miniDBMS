var webapp = angular.module("webapp",[]);

webapp.controller("QueryCtrl", function($scope, $http){
	// accept query
	//$scope.query = "SELECT * FROM teacher, department WHERE location = L2 AND teacher.did = department.did";
	$scope.submitQuery = function(query) {
		console.log(query);
		if(!query)
			return;
		$http.get("query?query="+query).success(function(data){
			generateTable(data);
		});
	}
});

webapp.controller("TableCtrl",function($scope, $http){
	
	// show specified table
	$scope.showTable = function(table) {
		if (!table)
			return;
		$http.get("/tables?table="+table).success(function(data){
			generateTable(data);
			//console.log(table);
			//console.log(JSON.stringify($scope.data));
		});
	}
	
	// initialize table list
	$http.get("/tables").success(function(data){
		$scope.tables = data;
	});

	// initialize result table (use 'course' table)
	$scope.showTable("course");
});

// generate table with specified json data
	function generateTable(data) {
		var table = "";
		table += '<table class="table table-striped">';
		
		// table head
		table += '<thead>';
		table += '<tr>';
		var keys = Object.keys(data[0]);
		for(var i in keys) {
			table += '<th>';
			table += keys[i];
			table += '</th>';
		}
		table += '</tr>';
		table += '</thead';
		
		// table body
		table += '<tbody>';
		for(var i in data) {
			var row = data[i];
			table += '<tr>';
			for(var j in keys) {
				//console.log(keys[j]);
				//console.log(row[keys[j]]);
				table += '<td>';
				table += row[keys[j]];
				table += '</td>';
			}
			table += '</tr>';
		}
		table += '</tbody>';

		table += '</table>'
		$("#result").html(table);
	}