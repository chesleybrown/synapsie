$(document).ready(function() {
	
	function mysqlTimeStampToDate(timestamp) {
		//function parses mysql datetime string and returns javascript Date object
		//input has to be in this format: 2007-06-05 15:26:02
		var regex=/^([0-9]{2,4})-([0-1][0-9])-([0-3][0-9]) (?:([0-2][0-9]):([0-5][0-9]):([0-5][0-9]))?$/;
		var parts=timestamp.replace(regex,"$1 $2 $3 $4 $5 $6").split(' ');
		return new Date(parts[0],parts[1]-1,parts[2],parts[3],parts[4],parts[5]);
	}
	
	/*
	 * Submit Buttons (Solves issue with clicking outside the input but within the visual button)
	 */
	$('.input_button_start, .input_button_end').bind('click', function(e) {
		$(this).parent().find('input[type=submit]').parents('form').trigger('submit');
		$(this).parent().find('input[type=button]').trigger('click');
	});
	$('.input_button_body .icon').bind('click', function(e) {
		$(this).next('input[type=submit]').parents('form').trigger('submit');
		$(this).next('input[type=button]').trigger('click');
	});
	/*
	 * END Submit Buttons
	 */
	
	
	/*
	 * Tag Autocompleter
	 */
	$("#id_tags").fcbkcomplete({
		cache: true,
		complete_text: 'Start typing to see your available tags...',
		filter_case: false,
		filter_hide: true,
		firstselected: true,
		filter_selected: true,
		newel: true,
		onselect: function(item) {
			setupInlineLabels(item);
		},
		onremove: function(item) {
			setupInlineLabels(item);
		}
	});
	/*
	 * END Tag Autocompleter
	 */
	
	
	/*
	 * In-Line Labels
	 */
	var in_field_labels_options = {
		fadeOpacity: 0.5,
		fadeDuration: 350
	};
	$('form .field label').inFieldLabels(in_field_labels_options);
	
	function setupInlineLabels(item) {
		var id_tags_label = $('#id_tags_field label');
		var id_tags_maininput = $('#id_tags_field input.maininput');
		var id_tags_holder = $('#id_tags_field ul.holder');
		var id_tags_select = $('#id_tags');
		var id_tags_label_clone = false;
		
		if (item) {
			id_tags_maininput.bind('blur.setupInFieldLabels', function() {
				var id_tags_selected = id_tags_select.find('option.selected');
				
				if (id_tags_selected.size() == 0) {
					id_tags_maininput.attr('id', 'maininput');
					id_tags_label_clone = id_tags_label.clone(false);
					id_tags_label_clone.insertAfter(id_tags_label);
					id_tags_label.remove();
					
					id_tags_label_clone.css({opacity: 0.0}).show();
					id_tags_label_clone.animate({
						opacity: 1
					}, in_field_labels_options['fadeDuration']);
					
					id_tags_label_clone.inFieldLabels(in_field_labels_options);
				}
				
				$(this).unbind('blur.setupInFieldLabels');
			});
		}
		else {
			id_tags_maininput.attr('id', 'maininput');
			id_tags_label.attr('for', 'maininput');
			id_tags_label.inFieldLabels(in_field_labels_options);
		}
	}
	setupInlineLabels(false);
	/*
	 * END In-Line Labels
	 */
	
	
	/*
	 * Enable ajax for record form
	 */
	$('#record_create_form').ajaxForm({
		success: function(data) {
			
			var new_record = $('#record_blank').clone(true);
			var user_record_list = $('#user_record_list');
			var created = mysqlTimeStampToDate(data['created']);
			var security = '';
			var short_months = [
				'Jan',
				'Feb',
				'Mar',
				'Apr',
				'Jun',
				'Jul',
				'Aug',
				'Sep',
				'Oct',
				'Nov',
				'Dec',
			];
			
			// determine time
			var curr_hour = created.getHours();
			var curr_min = created.getMinutes();
			var am_pm = '';
				
			if (curr_hour < 12) {
				am_pm = 'AM';
			}
			else {
				am_pm = 'PM';
			}
			if (curr_hour == 0) {
				curr_hour = 12;
			}
			if (curr_hour > 12) {
				curr_hour = curr_hour - 12;
			}
			if (curr_min < 10) {
				curr_min = '0' + curr_min;
			}
			
			//determine security
			if (data['personal'] == 1) {
				var security = 'icon_personal';
			}
			else {
				var security = 'icon_shared';
			}
			
			new_record.attr('id', 'record_' + data['id']);
			new_record.css('opacity', 0);
			
			// populate with new record info
			new_record.find('div.security div.icon').addClass(security);
			new_record.find('div.header div.text').text(data['text']);
			new_record.find('div.header div.time').text(curr_hour + ':' + curr_min + am_pm);
			new_record.find('div.date span.month').text(short_months[created.getMonth()]);
			new_record.find('div.date span.day').text(created.getDate());
			new_record.find('div.date span.year').text(created.getFullYear());
			new_record.find('div.header div.menu a.use_record_delete').attr('href', function(index, value) {
				return value + "/" + data['id'];
			});
			
			// tags
			var new_record_tags = $('<ul/>');
			new_record_tags.addClass('tags');
			var new_record_tags_tag = $('<li/>');
			new_record_tags_tag.addClass('tag');
			
			for (var tag in data['tags']) {
				var li_tag = new_record_tags_tag.clone();
				li_tag.text(data['tags'][tag]['name'] + ' x');
				new_record_tags.append(li_tag);
			}
			
			new_record.find('div.footer').append(new_record_tags);
			
			// add new record to DOM
			user_record_list.prepend(new_record);
			
			new_record.animate({
				height: 'toggle'
			}, 'slow', 'linear', function() {
				new_record.animate({
					opacity: 1
				}, 'slow', 'linear');
			});
			
			// clear form
			//$('#id_text').val('');
			
		}
	});
	/*
	 * END Enable ajax for record form
	 */
	
	
	/*
	 * Handle delete action
	 */
	$('a.use_record_delete').bind('click', function(e) {
		var element = $(this);
		var container = element.parents('.record');
		
		container.animate({
			opacity: 0.75
		}, 'fast');
		
		$.ajax({
			type: 'delete',
			url: element.attr('href'),
			success: function() {
				container.animate({
					opacity: 0
				}, 'slow', 'linear', function() {
					container.slideUp('slow', function() {
						container.remove();
					});
				});
			},
			error: function() {
				container.animate({
					opacity: 1
				}, 'fast');
			}
		});
		
		e.preventDefault();
	});
	/*
	 * END Handle delete action
	 */
	
	
	/*
	 * Handle graphs
	 */
	$('table.use_visualize').visualize({
		type: 'pie',
		parseDirection: 'y',
		width: 220,
		height: 220,
		colors: ['#be1e2d','#666699','#92d5ea','#ee8310','#8d10ee','#5a3b16','#26a4ed','#f45a90','#e9e744', '#be1e2d','#666699','#92d5ea','#ee8310','#8d10ee','#5a3b16','#26a4ed','#f45a90','#e9e744', '#be1e2d','#666699','#92d5ea','#ee8310','#8d10ee','#5a3b16','#26a4ed','#f45a90','#e9e744']
	});
	$('div.visualize-info').insertBefore('div.visualize-pie');
	/*
	 * END graphs
	 */
	
	
	//enable elastic textfield for forms
	$('form.record_form textarea').elastic();
	
	//handle switching Personal flag
	$('form.record_form div.use_personal_flag').bind('click', function(e) {
		var element = $(this);
		
		if (element.hasClass('icon_personal')) {
			element.fadeOut('normal', function() {
				element
					.removeClass('icon_personal')
					.addClass('icon_shared')
					.text('Shared')
					.fadeIn('fast');
			});
			element.next('input').val(0);
		}
		else {
			element.fadeOut('normal', function() {
				element
					.removeClass('icon_shared')
					.addClass('icon_personal')
					.text('Personal')
					.fadeIn('fast');
			});
			element.next('input').val(1);
		}
	});
	
});