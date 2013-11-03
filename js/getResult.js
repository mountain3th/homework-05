$(document).ready(function(){
	for(var i = 1;i <= 100;i++){
		if( i % 20 == 0)
			$('#gnumber').children('thead').children('tr').append("<th scope='col'>"+i+"</th>");
		else
			$('#gnumber').children('thead').children('tr').append("<th scope='col'></th>");
		$('#gnumber').children('tbody').children('tr').append("<td></td>");
	}
	function getResult(){

		$.getJSON("http://192.168.1.101:23211",function(result){
			console.log(result);
			var gameNumber = result['goldpoint'].length+1;
			var numberGroupArray = [];
			var goldPointGroup = result['goldpoint'];


			for (var key in result) {
				if (key != 'goldpoint')
					numberGroupArray.push([key,result[key]]);
		    }
		    console.log(numberGroupArray);
		    numberGroupArray.sort(function(a,b){
		    	return  b[1] - a[1];
		    })

		    for(var i = 0;i < goldPointGroup.length;i++){
		    	$('#gnumber').children('tbody').children('tr').children('td:eq(' + i + ')').html(goldPointGroup[i].toFixed(2));
		    }
		    $('#gameNumber').html(gameNumber);
		    $('#userList').children('tbody').html("");
		    for(var i = 0;i <= numberGroupArray.length-1;i++){
		    	$('#userList').children('tbody').append("<tr><td>"+(i+1)+"</td><td>" + numberGroupArray[i][0] +"</td><td>" + numberGroupArray[i][1] +"</td></tr>");
		    }
		});
		$('.visualize').trigger('visualizeRefresh');
	}

	setInterval(getResult,1000);
});
