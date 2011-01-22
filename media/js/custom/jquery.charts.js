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
							height: 240,
							title: 'My Used Tags'
						});
						
						/*
						// create canvas
						var r = Raphael(id, 380, 220);
						
						var pie = r.g.piechart(230, 110, 100, results['counts'], {
							legend: results['names'],
							legendpos: "west"
						});
						
						// hover effect
						pie.hover(function () {
							this.sector.stop();
							this.sector.scale(1.1, 1.1, this.cx, this.cy);
							if (this.label) {
								this.label[0].stop();
								this.label[0].scale(1.5);
								this.label[1].attr({"font-weight": 800});
							}
						}, function () {
							this.sector.animate({scale: [1, 1, this.cx, this.cy]}, 1000, "bounce");
							if (this.label) {
								this.label[0].animate({scale: 1}, 500, "bounce");
								this.label[1].attr({"font-weight": 400});
							}
						});
						*/
						
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



//$('#chartcontainer').chart('update');