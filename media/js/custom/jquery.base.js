$(document).ready(function() {
	
	function mysqlTimeStampToDate(timestamp) {
		//function parses mysql datetime string and returns javascript Date object
		//input has to be in this format: 2007-06-05 15:26:02
		var regex=/^([0-9]{2,4})-([0-1][0-9])-([0-3][0-9]) (?:([0-2][0-9]):([0-5][0-9]):([0-5][0-9]))?$/;
		var parts=timestamp.replace(regex,"$1 $2 $3 $4 $5 $6").split(' ');
		return new Date(parts[0],parts[1]-1,parts[2],parts[3],parts[4],parts[5]);
	}
	
	function nl2br(str) {
		var regX = /\n/g ;
		var s = '';
		
		s = new String(str);
		s = s.replace(regX, "<br /> \n");
		return s;
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
	 * Site Search
	 */
	$('#site_search .icon_search').bind('click', function(e) {
		$('#site_search form').submit();
	});
	/*
	 * END Site Search
	 */
	
	
	/*
	 * Time Since (timeago)
	 */
	function setupTimeSince() {
		$('ul.records li.record .use_time_since').each(function(index, element) {
			var date = $(this).prevAll('.datetime').text();
			$(this).text(jQuery.timeago(date));
			
			if ($(this).css('opacity') == 0) {
				$(this).animate({
					opacity: 1
				}, 'slow');
			}
		});
	}
	setupTimeSince();
	setInterval(setupTimeSince, 60000);
	/*
	 * END Time Since (timeago)
	 */
	
	
	/*
	 * Tag Autocompleter
	 */
	$("#id_tags").fcbkcomplete({
		key_codes: [
			0, //tab?
			9, //tab
			13, //enter
			188 //comma
		],
		cache: true,
		complete_text: false,
		filter_case: false,
		filter_hide: true,
		firstselected: true,
		filter_selected: true,
		newel: true,
		allow_duplicates: false,
		onselect: function(item) {
			setupInlineLabels(item);
		},
		onremove: function(item) {
			setupInlineLabels(item);
		}
	});
	$("#id_tags_temp").remove();
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
	$('form.use_inline_labels label').inFieldLabels(in_field_labels_options);
	
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
	 * Build Record
	 */
	function buildRecord(data) {
		
		var new_record = $('#records_blank ul.records li.record').clone(false);
		var new_record_tags = $('#tags_blank ul.tags').clone(false);
		var new_record_tags_tag = $('#tags_blank ul.tags li.tag').clone(false);
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
		
		// add leading zero to day if needed
		var curr_day = created.getDate();
		
		if (curr_day < 10) {
			curr_day = '0' + curr_day;
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
		new_record.find('div.header div.text').html(nl2br(data['text']));
		new_record.find('div.header div.datetime').text(data['created']);
		new_record.find('div.header div.time').text(curr_hour + ':' + curr_min + am_pm);
		new_record.find('div.header div.time_since').text(jQuery.timeago(created));
		new_record.find('div.date span.month').text(short_months[created.getMonth()]);
		new_record.find('div.date span.day').text(curr_day);
		new_record.find('div.date span.year').text(created.getFullYear());
		new_record.find('div.header div.menu a.use_record_delete').attr('href', function(index, value) {
			return value + "/" + data['id'];
		});
		
		// update menu items
		new_record.find('div.menu ul.menu_items li.menu_item').each(function(e) {
			$(this).find('a').attr('href', function(index, attr) {
				return attr.replace(/\/0/, '/' + data['id']);
			});
		});
		setupRecordMenuItems(new_record);
		
		// tags
		new_record_tags.html('');
		for (var tag in data['tags']) {
			var li_tag = new_record_tags_tag.clone();
			
			//tag text
			li_tag.find('a.tag_text')
				.text(data['tags'][tag]['name'])
				.attr('href', function(index, attr) {
					return attr + 'tags/' + data['tags'][tag]['name']
				});
			
			//tag delete
			li_tag.find('a.closebutton').attr('href', function(index, attr) {
				return attr.replace(/\/(0)\/(0)/, '/' + data['tags'][tag]['name'] + '/' + data['id']);
			});
			new_record_tags.append(li_tag);
		}
		setupTags(new_record_tags);
		
		new_record.find('div.footer').append(new_record_tags);
		
		// update sidebar with new tags
		// TO DO
		
		// enable menus for this new record
		$(new_record).find('div.use_record_menu').dropdownMenus({
			parent_block_selector: 'li.record',
			show_effect: function(e) {
				e.parent().find('.security').addClass('hover');
				e.addClass('hover');
			},
			hide_effect: function(e) {
				e.parent().find('.security').removeClass('hover');
				e.removeClass('hover');
			}
		});
		
		// return record
		return new_record;
		
	}
	/*
	 * END Build Record
	 */
	
	
	/*
	 * Enable ajax for record form (make into plugin!)
	 */
	function setupRecordForm() {
		$('#record_create_form').ajaxForm({
			success: function(data) {
				
				//init
				var user_record_list = $('#user_record_list');
				var new_record = buildRecord(data);
				
				// add new record to DOM
				user_record_list.prepend(new_record);
				
				new_record.animate({
					height: 'toggle'
				}, 'slow', 'linear', function() {
					$(this).animate({
						opacity: 1
					}, 'slow', 'linear');
				});
				
				// clear form
				$('#id_text')
					.val('')
					.removeAttr('style')
					.blur();
				$('#id_tags').fcbkcomplete('clear');
				$('#record_form_datetime_reset div.use_record_form_datetime_reset').click();
				
				//done, focus
				$('#id_text').focus();
				
			}
		});
	}
	setupRecordForm();
	/*
	 * END Enable ajax for record form
	 */
	
	
	/*
	 * Handle Record delete action (make into plugin!)
	 */
	function setupRecordMenuItems(container) {
		$(container).find('a.use_record_delete').bind('click', function(e) {
			var element = $(this);
			var menu = $(this).parents('.menu');
			var container = element.parents('.record ');
			var content = container.find('.record_content');
			var delete_confirmation = $('#record_delete_confirmation').find('.delete_confirmation').clone();
			
			//fade out record content
			content.animate({
				opacity: 0.40
			}, 'slow');
			
			//show delete confirmation dialog
			container.block({
				message: delete_confirmation
			});
			
			//setup delete action
			delete_confirmation.find('.delete_action').attr('href', element.attr('href'));
			delete_confirmation.find('.delete_action').bind('click', function(e) {
				//hide delete confirmation dialog
				container.unblock();
				container.block({
					message: ''
				});
				
				$.ajax({
					type: 'delete',
					url: $(this).attr('href'),
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
						content.animate({
							opacity: 1
						}, 'fast');
					}
				});
				
				e.preventDefault();
			});
			
			//setup cancel action
			delete_confirmation.find('.cancel_action').bind('click', function(e) {
				content.animate({
					opacity: 1
				}, 'fast');
				container.unblock();
				
				e.preventDefault();
			});
			
			e.preventDefault();
		});
	}
	setupRecordMenuItems('body');
	/*
	 * END Handle Record delete action
	 */
	
	
	/*
	 * Handle Tag delete action (make into plugin!)
	 */
	function setupTags(container) {
		//single tag delete
		$(container).find('a.use_tag_delete').bind('click', function(e) {
			var element = $(this);
			var container = element.parents('li.tag');
			
			container.animate({
				opacity: 0.5
			}, 'fast');
			
			$.ajax({
				type: 'delete',
				url: element.attr('href'),
				success: function() {
					container.animate({
						opacity: 0
					}, 'slow', 'linear', function() {
						$(this).remove();
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
		
		//all tag delete
		$(container).find('a.use_tag_all_delete').bind('click', function(e) {
			var element = $(this);
			var container = element.parents('li.tag');
			var tag_name = container.find('.tag_text').text();
			var tags = false;
			
			//find all other tags on the page with this name
			tags = $('ul.tags li.tag').filter(function() {
				return $(this).find(".tag_text").text() == tag_name;
			});
			
			tags.animate({
				opacity: 0.5
			}, 'fast');
			
			$.ajax({
				type: 'delete',
				url: element.attr('href'),
				success: function() {
					tags.animate({
						opacity: 0
					}, 'slow', 'linear', function() {
						$(this).remove();
					});
				},
				error: function() {
					tags.animate({
						opacity: 1
					}, 'fast');
				}
			});
			
			e.preventDefault();
		});
	}
	setupTags('body');
	/*
	 * END Handle Tag delete action
	 */
	
	
	/*
	 * Handle Record More
	 */
	function setupRecordMore(container) {
		//single tag delete
		$(container).find('a.use_record_more').bind('click', function(e) {
			var element = $(this);
			var holder = element.parent().parent();
			var user_record_list = $('#user_record_list');
			var loading = holder.find('.loading');
			
			//show loading animation
			element.hide();
			loading.show();
			
			$.ajax({
				type: 'get',
				url: element.attr('href'),
				success: function(data) {
					var message = data.message;
					var records = data.result.records;
					var new_record = false;
					var page = 2;
					
					var matches = element.attr('href').match(/page\/(\d+)/);
					page = parseInt(matches[1]);
					next_page = page+1;
					
					for (key in records) {
						new_record = buildRecord(records[key]);
						user_record_list.append(new_record);
						
						new_record.animate({
							height: 'toggle'
						}, 'slow', 'linear', function() {
							$(this).animate({
								opacity: 1
							}, 'slow', 'linear');
						});
					}
					
					//determine if there are anymore results to find
					if (records.length < data.result.results_per_page) {
						holder.html(data.message.desc);
					}
					else {
						//update page number
						element.attr('href', function(index, attr) {
							return attr.replace(/(page\/)\d+/, '$1' + next_page);
						});
					}
					
				},
				error: function() {
					console.log('error');
				},
				complete: function() {
					loading.hide();
					element.show();
				}
			});
			
			e.preventDefault();
		});
	}
	setupRecordMore('body');
	/*
	 * END Handle Record More
	 */
	
	
	//enable elastic textfield for forms
	$('form.record_form textarea').elastic();
	
	
	/*
	 * Setup Record Menus (dropdowns)
	 */
	$('div.use_record_menu').dropdownMenus({
		parent_block_selector: 'li.record',
		show_effect: function(e) {
			e.parent().find('.security').addClass('hover');
			e.addClass('hover');
		},
		hide_effect: function(e) {
			e.parent().find('.security').removeClass('hover');
			e.removeClass('hover');
		}
	});
	/*
	 * END Setup Record Menus (dropdowns)
	 */
	
	
	/*
	 * Setup Record Form Security Menu (dropdowns)
	 */
	$('form.record_form div.use_form_menu').dropdownMenus({
		show_effect: function(e) {
			e.addClass('hover');
		},
		hide_effect: function(e) {
			e.removeClass('hover');
		}
	});
	
	//this handles when a user selects an option from the security menu
	$('form.record_form div.use_form_menu ul.menu_items li.menu_item').bind('click', function(e) {
		
		//init
		var menu_header = $(this).parents('.form_menu').find('li.menu_header');
		var menu_header_text = menu_header.find('.menu_header_text');
		var menu_header_icon = menu_header.find('.menu_header_icon');
		var menu_item_text = $(this).find('.menu_item_text').text();
		var menu_item_icon = $(this).find('.menu_item_icon');
		var menu_item_value = $(this).find('.menu_item_value').text();
		var input = $(this).parents('.form_menu').next('input');
		
		//change header
		menu_header_text.text(menu_item_text);
		menu_header_icon.attr('class', menu_item_icon.attr('class'));
		menu_header_icon
			.removeClass('menu_item_icon')
			.addClass('menu_header_icon');
		input.val(menu_item_value);
	});
	/*
	 * END Setup Record Form Security Menu (dropdowns)
	 */
	
	
	/*
	 * Setup Record Form Date Picker
	 */
	Date.firstDayOfWeek = 0; //sunday
	$('.use_datepicker')
		.datePicker({
			inline: true,
			startDate: '01/01/1970',
			endDate: (new Date()).asString(),
			previousYear: '',
			previousMonth: '',
			nextYear: '',
			nextMonth: ''
		})
		.bind(
			'dateSelected',
			function(e, selectedDate, $td) {
				var input = $(this).parents('.form_menu').next('input');
				var formated_day = selectedDate.getDate();
				if (formated_day < 10) {
					formated_day = '0' + formated_day;
				}
				var formated_month = selectedDate.getMonth()+1;
				if (formated_month < 10) {
					formated_month = '0' + formated_month;
				}
				
				var formated_date = selectedDate.getMonthName(true) + ' ' + formated_day + ', ' + selectedDate.getFullYear();
				var date = selectedDate.getFullYear() + '-' + formated_month + '-' + formated_day
				
				$(this).parents('.form_menu').find('.menu_header_text').text(formated_date);
				input.val(date);
			}
		);
	/*
	 * END Setup Record Form Date Picker
	 */
	
	
	/*
	 * Setup Record Form Date Time Selection
	 */
	function setupDateTimeSelection() {
		var selections = $('#record_form_date, #record_form_time_hour, #record_form_time_minute, #record_form_time_ampm');
		var datetime_reset = $('#record_form_datetime_reset');
		
		$(selections)
			.find('.menu_item, .menu_item_datepicker')
			.bind('click', function(e) {
				datetime_reset.fadeIn();
				$('#id_datetime_set').val(1);
			});
	}
	setupDateTimeSelection();
	/*
	 * END Record Form Date Time Selection
	 */
	
	/*
	 * Setup Time Selection Auto-Updating (clock)
	 */
	function setupDateTimeAutoUpdate(force_update) {
		var now = new Date();
		var selection_menu_items = $('#record_form_date, #record_form_time_hour, #record_form_time_minute, #record_form_time_ampm')
			.find('.form_menu .menu_items');
		var date = $('#record_form_date');
		var hour = $('#record_form_time_hour');
		var minute = $('#record_form_time_minute');
		var ampm = $('#record_form_time_ampm');
		var datetime_reset = $('#record_form_datetime_reset');
		
		//generate formated date
		var formated_day = now.getDate();
		if (formated_day < 10) {
			formated_day = '0' + formated_day;
		}
		var formated_month = now.getMonth()+1;
		if (formated_month < 10) {
			formated_month = '0' + formated_month;
		}
		var formated_date = now.getMonthName(true) + ' ' + formated_day + ', ' + now.getFullYear();
		var sql_date = now.getFullYear() + '-' + formated_month + '-' + formated_day
		
		//generate hour
		var formated_hour = now.getHours();
		if (formated_hour >= 12){
			if (formated_hour == 12){
				formated_hour = 12;
			}
			else {
				formated_hour = formated_hour-12;
			}
		}
		else if(formated_hour < 12){
			if (formated_hour == 0){
				formated_hour = 12;
			}
		}
		
		//generate minute
		var formated_minute = now.getMinutes();
		if (formated_minute < 10) {
			formated_minute = '0' + formated_minute;
		}
		
		//generate ampm
		var formated_ampm = 'AM';
		if (now.getHours() > 12) {
			formated_ampm = 'PM';
		}
		
		//update selection inputs ONLY if datetime_reset isn't visible
		if (force_update || (!$(selection_menu_items).is(':visible') && $(datetime_reset).is(':hidden'))) {
			$(date).find('.use_datepicker').dpSetSelected(formated_month+'/'+formated_day+'/'+now.getFullYear()); //stupid datepicker
			$(date).find('.menu_header_text').text(formated_date);
			$(date).find('input').val(sql_date);
			
			$(hour).find('.menu_header_text').text(formated_hour);
			$(hour).find('input').val(formated_hour);
			
			$(minute).find('.menu_header_text').text(formated_minute);
			$(minute).find('input').val(formated_minute);
			
			$(ampm).find('.menu_header_text').text(formated_ampm);
			$(ampm).find('input').val(formated_ampm);
			
			$('#id_datetime_set').val(0);
		}
	}
	setupDateTimeAutoUpdate(false);
	setInterval(function() { setupDateTimeAutoUpdate(false); }, 5000);
	/*
	 * END Setup Time Selection Auto-Updating (clock)
	 */
	
	
	/*
	 * Setup DateTime Reset
	 */
	$('div.use_record_form_datetime_reset').bind('click', function(e) {
		setupDateTimeAutoUpdate(true);
		$(this).parent().fadeOut();
	});
	/*
	 * END Setup DateTime Reset
	 */
	
	
	/*
	 * Setup Tag Popular Show All
	 */
	$('a.use_tag_popular_show_all').bind('click', function(e) {
		$('#sidebar_tab_popular').find('ul.tags_chart li').fadeIn('slow');
		
		$(this).remove();
		e.preventDefault();
	});
	/*
	 * END Setup Tag Popular Show All
	 */
	
	
});