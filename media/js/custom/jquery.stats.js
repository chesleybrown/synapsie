(function($){
	
	$.fn.stats = function(method, options) {
		
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
				
				// show loading
				$(element).html('<div class="loading"></div>');
				
				if (options.type == 'weekly') {
					
					$.ajax({
						url: '/api/stats.json/weekly/recent',
						success: function(data) {
							
							var stats = data.data.stats;
							
							weeklyData.recent = stats;
							
							element.stats('render', {
								type: options.type,
								data: weeklyData
							});
						}
					});
					
					$.ajax({
						url: '/api/stats.json/weekly/all_time',
						success: function(data) {
							
							var stats = data.data.stats;
							
							weeklyData.all_time = stats;
							
							element.stats('render', {
								type: options.type,
								data: weeklyData
							});
							
						}
					});
					
				}
				else if (options.type == 'monthly') {
					
					$.ajax({
						url: '/api/stats.json/monthly/all_time',
						success: function(data) {
							
							var stats = data.data.stats;
							
							element.stats('render', {
								type: options.type,
								data: stats
							});
						}
					});
					
				}
				else if (options.type == 'yearly') {
					
					$.ajax({
						url: '/api/stats.json/yearly',
						success: function(data) {
							
							var stats = data.data.stats;
							
							element.stats('render', {
								type: options.type,
								data: stats
							});
						}
					});
					
				}
				else if (options.type == 'record_counts') {
					
					$.ajax({
						url: '/api/stats.json/record_counts',
						success: function(data) {
							
							var stats = data.data.stats;
							
							element.stats('render', {
								type: options.type,
								data: stats
							});
						}
					});
					
				}
				else if (options.type == 'tag_counts') {
					
					$.ajax({
						url: '/api/stats.json/tag_counts',
						success: function(data) {
							
							var stats = data.data.stats;
							
							element.stats('render', {
								type: options.type,
								data: stats
							});
						}
					});
					
				}
				else if (options.type == 'top_tags') {
					
					$.ajax({
						url: '/api/tags.json',
						success: function(data) {
							
							var tags = data.data;
							
							element.stats('render', {
								type: options.type,
								data: tags
							});
							
						}
					});
					
				}
				
			},
			'render': function(options) {
				
				// init
				var id = $(element).attr('id');
				
				// remove any current stats
				$(element).html('');
				
				if (options.type == 'weekly' && options.data.recent && options.data.all_time) {
					
					var chartData = new google.visualization.DataTable();
					
					chartData.addColumn('string', 'Weekday');
					chartData.addColumn('number', 'Recently');
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
				else if (options.type == 'monthly') {
					
					var chartData = new google.visualization.DataTable();
					
					chartData.addColumn('string', 'Month');
					chartData.addColumn('number', 'All Time');
					chartData.addRows(options.data.length);
					
					for (i in options.data) {
						chartData.setValue(parseInt(i), 0, options.data[i]['month']);
						chartData.setValue(parseInt(i), 1, options.data[i]['quality']);
					}
					
					if (id) {
						var chart = new google.visualization.LineChart(document.getElementById(id));
						chart.draw(chartData, {
							width: 690,
							height: 250,
							title: 'Quality of Life by Month'
						});
					}
					
				}
				else if (options.type == 'yearly') {
					
					var chartData = new google.visualization.DataTable();
					
					chartData.addColumn('string', 'Year');
					chartData.addColumn('number', 'All Time');
					chartData.addRows(options.data.length);
					
					for (i in options.data) {
						chartData.setValue(parseInt(i), 0, options.data[i]['year'].toString());
						chartData.setValue(parseInt(i), 1, options.data[i]['quality']);
					}
					
					if (id) {
						var chart = new google.visualization.LineChart(document.getElementById(id));
						chart.draw(chartData, {
							width: 690,
							height: 250,
							title: 'Quality of Life by Year'
						});
					}
					
				}
				else if (options.type == 'record_counts') {
					
					var chartData = new google.visualization.DataTable();
					
					chartData.addColumn('string', 'Counts');
					
					var count = 0;
					for (i in options.data) {
						chartData.addColumn('number', i);
						count++;
					}
					
					chartData.addRows(count);
					
					var count = 0;
					for (i in options.data) {
						chartData.setValue(count, 0, i);
						chartData.setValue(count, count+1, options.data[i]);
						count++;
					}
					
					if (id) {
						var chart = new google.visualization.BarChart(document.getElementById(id));
						chart.draw(chartData, {
							width: 690,
							height: 250,
							title: 'Record Counts',
							legend: 'none'
						});
					}
					
				}
				else if (options.type == 'tag_counts') {
					
					var chartData = new google.visualization.DataTable();
					
					chartData.addColumn('string', 'Counts');
					
					var count = 0;
					for (i in options.data) {
						chartData.addColumn('number', i);
						count++;
					}
					
					chartData.addRows(count);
					
					var count = 0;
					for (i in options.data) {
						chartData.setValue(count, 0, i);
						chartData.setValue(count, count+1, options.data[i]);
						count++;
					}
					
					if (id) {
						var chart = new google.visualization.BarChart(document.getElementById(id));
						chart.draw(chartData, {
							width: 690,
							height: 250,
							title: 'Tag Counts',
							legend: 'none'
						});
					}
					
				}
				else if (options.type == 'top_tags') {
					
					var chartData = new google.visualization.DataTable();
					chartData.addColumn('string', 'Tag');
					chartData.addColumn('number', 'Usage');
					chartData.addRows(options.data.length);
					
					for (i in options.data) {
						chartData.setValue(parseInt(i), 0, options.data[i]['name']);
						chartData.setValue(parseInt(i), 1, options.data[i]['count']);
					}
					
					var chart = new google.visualization.PieChart(document.getElementById(id));
					chart.draw(chartData, {
						width: 690,
						height: 340,
						title: 'Top Used Tags'
					});
					
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



/*
 * Stats Menu
 */
function setupStatsMenu(container) {
	$(container).find('div.use_stats_menu').find('ul.menu_items li.menu_item').bind('click', function(e) {
		
		// init
		var menu_item_value = $(this).find('.menu_item_value').text();
		
		// update selected chart
		$('#stats_container').stats('update', {
			type: menu_item_value
		});
		
	});
	
	$(container).find('#stats_container').stats('update', {
		type: 'weekly'
	});
}
setupStatsMenu('body');
/*
 * END Stats Menu
 */