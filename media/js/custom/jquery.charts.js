(function($){
	
	$.fn.chart = function(method, options) {
		
		// init
		var element = $(this);
		var settings = {
			'test': true
		};
		
		if (options) {
			$.extend(settings, options);
		}
		
		// available methods
		var methods = {
			'update': function(options) {
				
				$.ajax({
					url: '/api/tags.json',
					success: function(data) {
						
						var id = $(element).attr('id');
						var tags = data.data;
						
						// remove any current charts
						$(element).html('');
						
						var chartData = new google.visualization.DataTable();
						chartData.addColumn('string', 'Task');
						chartData.addColumn('number', 'Hours per Day');
						chartData.addRows(tags.length);
						
						for (i in tags) {
							chartData.setValue(parseInt(i), 0, tags[i]['name']);
							chartData.setValue(parseInt(i), 1, tags[i]['count']);
						}
						
						var chart = new google.visualization.PieChart(document.getElementById(id));
						chart.draw(chartData, {
							width: 370,
							height: 280,
							title: 'My Used Tags'
						});
						
					}
				});
				
				$.ajax({
					url: '/api/stats.json/weekly/recent',
					success: function(data) {
						
						var id = $('#chartcontainer2').attr('id');
						var stats = data.data.stats;
						
						// remove any current charts
						$('#chartcontainer2').html('');
						
						var chartData = new google.visualization.DataTable();
						
						chartData.addColumn('string', 'Weekday');
						chartData.addColumn('number', 'Quality');
						chartData.addRows(stats.length);
						
						for (i in stats) {
							chartData.setValue(parseInt(i), 0, stats[i]['weekday']);
							chartData.setValue(parseInt(i), 1, stats[i]['quality']);
						}
						
						var chart = new google.visualization.LineChart(document.getElementById(id));
						chart.draw(chartData, {
							width: 290,
							height: 180,
							title: 'Quality of Life',
							legend: 'none'
						});
						
					}
				});
				
			}
		}
		
		// method calling logic
		if (methods[method]) {
			return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
		}
		else if (typeof method === 'object' || ! method) {
			return methods.init.apply(this, arguments);
		}
		else {
			$.error('Method ' +  method + ' does not exist on jQuery.chart');
		}   
		
		return false;
	};
	
})(jQuery);



$('#chartcontainer').chart('update');