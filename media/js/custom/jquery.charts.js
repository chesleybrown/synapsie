(function($){
	
	$.fn.chart = function(method, options) {
		
		// init
		var element = $(this);
		var settings = {
			type: 'weekly'
		};
		var weeklyData = {
			recent: null,
			all_time: null
		};
		
		if (options) {
			$.extend(settings, options);
		}
		
		// available methods
		var methods = {
			'update': function(options) {
				
				if (options.type == 'tags') {
					
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
					
				}
				else if (options.type == 'weekly') {
					
					$.ajax({
						url: '/api/stats.json/weekly/recent',
						success: function(data) {
							
							var id = $('#chartcontainer2').attr('id');
							var stats = data.data.stats;
							
							weeklyData.recent = stats;
							
							element.chart('render', {
								data: weeklyData
							});
						}
					});
					
					$.ajax({
						url: '/api/stats.json/weekly/all_time',
						success: function(data) {
							
							var id = $('#chartcontainer2').attr('id');
							var stats = data.data.stats;
							
							weeklyData.all_time = stats;
							
							element.chart('render', {
								data: weeklyData
							});
							
						}
					});
					
				}
				
			},
			'render': function(options) {
				
				if (options.data.recent && options.data.all_time) {
					
					var id = $('#chartcontainer2').attr('id');
					
					// remove any current charts
					$('#chartcontainer2').html('');
					
					var chartData = new google.visualization.DataTable();
					
					chartData.addColumn('string', 'Weekday');
					chartData.addColumn('number', 'Recent');
					chartData.addColumn('number', 'All Time');
					chartData.addRows(options.data.recent.length);
					
					for (i in options.data.recent) {
						chartData.setValue(parseInt(i), 0, options.data.recent[i]['weekday']);
						chartData.setValue(parseInt(i), 1, options.data.recent[i]['quality']);
					}
					
					for (i in options.data.all_time) {
						chartData.setValue(parseInt(i), 2, options.data.all_time[i]['quality']);
					}
					
					if (id) {
						var chart = new google.visualization.LineChart(document.getElementById(id));
						chart.draw(chartData, {
							width: 690,
							height: 250,
							title: 'Quality of Life by Weekday'
						});
					}
					
				}
				
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



$('#chartcontainer').chart('update', {
	type: 'weekly'
});