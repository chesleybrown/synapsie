$(document).ready(function() {
	
	function mysqlTimeStampToDate(datetimestamp) {
		//function parses mysql datetime string and returns javascript Date object
		//input has to be in this format: 2007-06-05 15:26:02
		var regex=/^([0-9]{2,4})-([0-1][0-9])-([0-3][0-9]) (?:([0-2][0-9]):([0-5][0-9]):([0-5][0-9]))?$/;
		var parts=datetimestamp.replace(regex,"$1 $2 $3 $4 $5 $6").split(' ');
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
	function setupButtons(container) {
		$(container).find('.input_button_start, .input_button_end').bind('click', function(e) {
			var parent = $(this).parent();
			
			if ($(parent).find('input[type=submit]').is(':enabled')) {
				$(parent).find('input[type=submit]').parents('form').trigger('submit');
			}
			
			if ($(parent).find('input[type=button]').is(':enabled')) {
				$(parent).find('input[type=button]').trigger('click');
			}
		});
		$(container).find('.input_button_body .icon').bind('click', function(e) {
			if ($(this).next('input[type=submit]').is(':enabled')) {
				$(this).next('input[type=submit]').parents('form').trigger('submit');
			}
			
			if ($(this).next('input[type=button]').is(':enabled')) {
				$(this).next('input[type=button]').trigger('click');
			}
		});
	}
	setupButtons('body');
	/*
	 * END Submit Buttons
	 */
	
	
	/*
	 * Login Form
	 */
	function setupLoginForm(container) {
		$(container).find('#login').find('input[name=username], input[name=password]').ezpz_hint({
			hintClass: 'default',
			hintName: 'input_label'
		});
		$(container).find('#login').find('label[for=username]').click(function() {
			$(this).next('input').focus();
		});
	}
	setupLoginForm('body');
	/*
	 * END Login Form
	 */
	
	/*
	 * Site Gritter Site Messages
	 */
	function setupSiteMessages() {
		var messages = $.gritterExtend.parse();
		$.gritterExtend.adds(messages);
	}
	setupSiteMessages();
	/*
	 * END Gritter Site Messages
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
	 * Sidebar
	 */
	$('#site_sidebar').sidebar();
	/*
	 * END Sidebar
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
	function setupAutocompleter(container) {
		
		// setup autocomplete
		$(container).each(function() {
			
			// init
			var element = $(this);
			
			$(element).find("select.tags").fcbkcomplete({
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
					
					$('#record_edit_form_popup form, #record_add_tags_form_popup form').each(function() {
						
						// update the edit record autocompleter list
						var form = $(this);
						var new_edit_select_tags = $(element).find('select.tags').clone();
						var edit_select_tags = $(form).find('select.tags');
						
						// deselect anything that may already be selected
						$(new_edit_select_tags).find('option')
							.removeAttr('class')
							.attr('selected', false);
						
						$(new_edit_select_tags)
							.attr('id', $(edit_select_tags).attr('id'))
							.attr('name', $(edit_select_tags).attr('name'));
						$(form).find('select.tags').replaceWith(new_edit_select_tags);
						
					});
				},
				onremove: function(item) {
					setupInlineLabels(item);
				}
			});
			$(element).find("input.tags_temp").remove();
			
			// focus effect for autocomplete input
			$(element).find('input.maininput').live('focus', function() {
				$(this).parents('ul.holder').addClass('focus');
			});
			$(element).find('input.maininput').live('blur', function() {
				$(this).parents('ul.holder').removeClass('focus');
			});
			
		});
	}
	setupAutocompleter('#record_create_form, #record_search_form');
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
		$('#record_create_form, #record_search_form').each(function() {
			
			// init
			var id_tags_label = $(this).find('div.tag_field label');
			var id_tags_maininput = $(this).find('div.tag_field input.maininput');
			var id_tags_holder = $(this).find('div.tag_field ul.holder');
			var id_tags_select = $(this).find('select.tags');
			var id_tags_label_clone = false;
			
			// hide label if items are selected on load
			var id_tags_selected = $(id_tags_select).find('option:selected');
			if ($(id_tags_selected).size() > 0) {
				id_tags_label.hide();
			}
			
			if (item) {
				$(id_tags_maininput).bind('blur.setupInFieldLabels', function() {
					var id_tags_selected = $(id_tags_select).find('option:selected');
					
					if ($(id_tags_selected).size() == 0) {
						$(id_tags_maininput).attr('id', 'maininput');
						id_tags_label_clone = $(id_tags_label).clone(false);
						$(id_tags_label_clone).insertAfter(id_tags_label);
						$(id_tags_label).remove();
						
						$(id_tags_label_clone).css({opacity: 0.0}).show();
						$(id_tags_label_clone).animate({
							opacity: 1
						}, in_field_labels_options['fadeDuration']);
						
						$(id_tags_label_clone).inFieldLabels(in_field_labels_options);
					}
					
					$(this).unbind('blur.setupInFieldLabels');
				});
			}
			else {
				$(id_tags_maininput).attr('id', 'maininput');
				$(id_tags_label).attr('for', 'maininput');
				$(id_tags_label).inFieldLabels(in_field_labels_options);
			}
			
		});
	}
	setupInlineLabels(false);
	/*
	 * END In-Line Labels
	 */
	
	
	/*
	 * Build Record
	 */
	function buildRecord(data, is_new) {
		
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
			'May',
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
			var security_text = 'Pesonal';
		}
		else {
			var security = 'icon_shared';
			var security_text = 'Shared';
		}
		
		new_record.attr('id', 'record_' + data['id']);
		new_record.css('opacity', 0);
		
		// populate with new record info
		new_record.find('div.security div.icon').addClass(security);
		new_record.find('div.security span.security_text').text(security_text);
		new_record.find('div.personal').text(data['personal']);
		new_record.find('div.header div.text').html(nl2br(data['text']));
		new_record.find('div.header div.datetime').text(data['created']);
		new_record.find('div.header div.time').text(curr_hour + ':' + curr_min + am_pm);
		new_record.find('div.header div.time_since').text(jQuery.timeago(created));
		new_record.find('div.date span.month').text(short_months[created.getMonth()]);
		new_record.find('div.date span.day').text(curr_day);
		new_record.find('div.date span.year').text(created.getFullYear());
		
		// update menu items
		$(new_record).find('div.menu ul.menu_items li.menu_item').each(function(e) {
			$(this).find('a').attr('href', function(index, attr) {
				return attr.replace(/\/0/, '/' + data['id']);
			});
		});
		setupRecordMenuItems(new_record);
		
		// update add_tag action
		$(new_record).find('a.use_record_add_tags').attr('href', function(index, attr) {
			return attr.replace(/\/0/, '/' + data['id']);
		});
		setupRecordAddTags(new_record);
		
		// update add_tags action
		$(new_record).find('div.add_tag').bind('click', function(e) {
			$(this).find('a').attr('href', function(index, attr) {
				return attr.replace(/\/0/, '/' + data['id']);
			});
		});
		
		// tags
		$(new_record_tags).html('');
		for (var tag in data['tags']) {
			var li_tag = new_record_tags_tag.clone();
			
			//tag text
			li_tag.find('a.tag_text')
				.text(data['tags'][tag]['name'])
				.attr('href', function(index, attr) {
					return attr.replace(/(\/tags\/)/, '$1' + escape(data['tags'][tag]['name']));
				});
			
			//tag delete
			li_tag.find('a.closebutton').attr('href', function(index, attr) {
				return attr.replace(/\/(0)\/(0)/, '/' + escape(data['tags'][tag]['name']) + '/' + data['id']);
			});
			new_record_tags.append(li_tag);
		}
		setupTags(new_record_tags);
		
		new_record.find('div.footer').append(new_record_tags);
		
		if (is_new) {
			// update sidebar with new tags
			$(new_record_tags).find('li').each(function() {
				$('#site_sidebar').sidebar('add_tag', $(this).find('a.tag_text').text());
			});
		}
		
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
			beforeSubmit: function(arr, form, options) {
				
				// show loading and disable form submit to prevent accidental double-post
				$(form).find('.loading').fadeIn('fast');
				$(form).find('input[type=submit]').attr('disabled', true);
				$(form).find('.input_button_wrapper').addClass('disabled');
				$(form).block({
					message: ''
				});
				
			},
			success: function(data, status_text, form) {
				
				// init
				var user_record_list = $('#user_record_list');
				var message = data.message;
				var record_data = data.data;
				var new_record = false;
				var record_text = $(form).find('textarea.text');
				var select_tags = false;
				
				
				// created successfully
				if (message['status'] == 201) {
					
					// add new record to DOM
					new_record = buildRecord(record_data, true);
					user_record_list.prepend(new_record);
					
					new_record.animate({
						height: 'toggle'
					}, 'slow', 'linear', function() {
						$(this).animate({
							opacity: 1
						}, 'slow', 'linear');
					});
					
					// clear form
					$(record_text)
						.val('')
						.removeAttr('style')
						.blur();
					$(form).find('select.tags').fcbkcomplete('clear');
					$(form).find('div.use_record_form_datetime_reset').trigger('click');
					
					//done, focus
					$(record_text).focus();
					
				}
				
				// something went wrong
				else {
					$.gritterExtend.add(data.message);
				}
				
				// always fade out loading and enable form again
				$(form).find('.loading').fadeOut('slow');
				$(form).find('input[type=submit]').attr('disabled', false);
				$(form).find('.input_button_wrapper').removeClass('disabled');
				$(form).unblock();
				
			}
		});
	}
	setupRecordForm();
	/*
	 * END Enable ajax for record form
	 */
	
	
	/*
	 * Handle Record menu actions (make into plugin!)
	 */
	function setupRecordMenuItems(container) {
		$(container).find('a.use_record_edit').bind('click', function(e) {
			
			var element = $(this);
			var menu = $(this).parents('.menu');
			var holder = $(element).parents('.record ');
			var content = $(holder).find('.record_content');
			var popup = $('#record_edit_form_popup').find('.popup').clone();
			var form = $(popup).find('form');
			var edit_action = $(form).find('input[type=submit]');
			
			// displayed record
			var record_contents = {
				datetime: $(content).find('div.datetime'),
				text: $(content).find('.text'),
				tags: $(content).find('ul.tags'),
				personal: $(content).find('.personal'),
				security: $(content).find('.security'),
				footer: $(content).find('div.footer'),
				datetime: $(content).find('div.datetime'),
				time: $(content).find('div.time'),
				time_since: $(content).find('div.time_since'),
				date: {
					month: $(content).find('div.date span.month'),
					day: $(content).find('div.date span.day'),
					year: $(content).find('div.date span.year')
				}
			};
			
			// inputs
			var record_inputs = {
				text: $(form).find('textarea[name$=-text]'),
				tags: $(form).find('select.tags'),
				personal: $(form).find('input[name$=-personal]'),
				security: $(form).find('div.security_dropdown')
			};
			
			// enable buttons and other stuff in edit form
			setupButtons(form);
			setupFormDropdownMenus(form);
			setupDatePicker(form);
			setupDateTimeSelection(form);
			setupDateTime(form, true, $(record_contents.datetime).text());
			setupDateTimeReset(form, record_contents.datetime);
			
			// set selections for dropdowns
			$(record_inputs.security).dropdownMenus('select', $(record_contents.personal).text());
			
			// fade out record content
			$(content).animate({
				opacity: 0.40
			}, 'slow');
			
			// show edit record dialog
			$(holder).block({
				message: $(popup)
			});
			
			// populate edit form
			$(record_inputs.text).focus();
			$(form).attr('action', $(element).attr('href'));
			
			// need to replace breaks with line breaks and then strip any remaining html
			var record_contents_clone = $(record_contents.text).clone();
			$(record_contents_clone).html(function(index, html) {
				return html.replace(/(\n)/g, "").replace(/(<br>|<br \/>)/g, "\n");
			});
			$(record_inputs.text).val($(record_contents_clone).text());
			
			$(record_inputs.personal).val($(record_contents.personal).text());
			
			// set current selected tags
			var tag_names = [];
			$(record_contents.tags).find('li.tag').each(function() {
				tag_names.push($(this).find('.tag_text').text());
			});
			$(record_inputs.tags).find('option').each(function() {
				for (tag_name in tag_names) {
					if (tag_names[tag_name] == $(this).val()) {
						$(this).attr('selected', true);
					}
				}
				
			});
			
			// enable autocompleter (this will auto-populate the selected tags now)
			setupAutocompleter(form);
			
			// enable elastic textarea
			$(form).find('textarea.use_elastic').elastic();
				
			$(form).ajaxForm({
				beforeSubmit: function(arr, form, options) {
					
					// hide edit confirmation dialog
					$(container).unblock();
					$(container).block({
						message: ''
					});
					
				},
				success: function(data) {
				
					// init
					var message = data.message;
					var record = data.data;
					
					// updated successfully
					if (message.status == 200) {
						
						/******************make into record plugin********************/
						
						//update record on screen
						$(record_contents.text).html(nl2br(record.text));
						$(record_contents.personal).text(record.personal);
						
						var created = mysqlTimeStampToDate(record.created);
						var short_months = [
							'Jan',
							'Feb',
							'Mar',
							'Apr',
							'May',
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
						
						$(record_contents.datetime).text(record.created);
						$(record_contents.time).text(curr_hour + ':' + curr_min + am_pm);
						$(record_contents.time_since).text(jQuery.timeago(created));
						$(record_contents.date.month).text(short_months[created.getMonth()]);
						$(record_contents.date.day).text(curr_day);
						$(record_contents.date.year).text(created.getFullYear());
						
						//determine security
						if (record.personal == 1) {
							var security = 'icon_personal';
						}
						else {
							var security = 'icon_shared';
						}
						
						$(record_contents.security).find('div.icon')
							.attr('class', 'icon')
							.addClass(security);
						
						var new_record_tags = $('#tags_blank ul.tags').clone(false);
						var new_record_tags_tag = $('#tags_blank ul.tags li.tag').clone(false);
						
						new_record_tags.html('');
						for (var tag in record.tags) {
							var li_tag = $(new_record_tags_tag).clone();
							
							//tag text
							$(li_tag).find('a.tag_text')
								.text(record.tags[tag].name)
								.attr('href', function(index, attr) {
									return attr.replace(/(\/tags\/)/, '$1' + escape(record.tags[tag].name));
								});
							
							//tag delete
							$(li_tag).find('a.closebutton').attr('href', function(index, attr) {
								return attr.replace(/\/(0)\/(0)/, '/' + escape(record.tags[tag].name) + '/' + record.id);
							});
							$(new_record_tags).append(li_tag);
						}
						setupTags(new_record_tags);
						$(record_contents.footer)
							.html('')
							.append(new_record_tags);
						
						/****************************************************/
						
					}
					
					// something went wrong
					else {
						$.gritterExtend.add(data.message);
					}
					
					//always unblock when done
					$(container).unblock();
					$(content).animate({
						opacity: 1
					}, 'fast');
					
				}
			});
			
			// setup cancel action
			$(popup).find('.cancel_action, .popup_close').bind('click', function(e) {
				content.animate({
					opacity: 1
				}, 'fast');
				$(holder).unblock();
				
				e.preventDefault();
			});
			
			e.preventDefault();
		});
		
		
		$(container).find('a.use_record_delete').bind('click', function(e) {
			var element = $(this);
			var menu = $(this).parents('.menu');
			var holder = $(element).parents('.record ');
			var content = $(holder).find('.record_content');
			var popup = $('#record_delete_confirmation').find('.popup').clone();
			
			//fade out record content
			$(content).animate({
				opacity: 0.40
			}, 'slow');
			
			//show delete confirmation dialog
			$(holder).block({
				message: $(popup)
			});
			
			//setup delete action
			$(popup).find('.delete_action').attr('href', element.attr('href'));
			$(popup).find('.delete_action').bind('click', function(e) {
				//hide delete confirmation dialog
				$(holder).unblock();
				$(holder).block({
					message: ''
				});
				
				$.ajax({
					type: 'delete',
					url: $(this).attr('href'),
					success: function(data) {
					
						//init
						var message = data.message;
						
						//created successfully
						if (message['status'] == 204) {
							
							$(holder).animate({
								opacity: 0
							}, 'slow', 'linear', function() {
								$(holder).slideUp('slow', function() {
									$(holder).remove();
								});
							});
							
						}
						
						//something went wrong
						else {
							$.gritterExtend.add(data.message);
							
							content.animate({
								opacity: 1
							}, 'fast');
						}
						
					},
					error: function() {
						content.animate({
							opacity: 1
						}, 'fast');
					},
					complete: function() {
						$(container).unblock();
					}
				});
				
				e.preventDefault();
			});
			
			//setup cancel action
			$(popup).find('.cancel_action, .popup_close').bind('click', function(e) {
				content.animate({
					opacity: 1
				}, 'fast');
				$(holder).unblock();
				
				e.preventDefault();
			});
			
			e.preventDefault();
		});
	}
	setupRecordMenuItems('body');
	/*
	 * END Handle Record menu actions
	 */
	
	
	/*
	 * Handle Record Add Tags actions
	 */
	function setupRecordAddTags(container) {
		$(container).find('a.use_record_add_tags').bind('click', function(e) {
			
			var element = $(this);
			var holder = $(element).parents('li.record ');
			var content = $(holder).find('div.record_content');
			var popup = $('#record_add_tags_form_popup').find('.popup').clone();
			var form = $(popup).find('form');
			
			// displayed record
			var record_contents = {
				tags: $(content).find('div.footer ul.tags'),
				footer: $(content).find('div.footer')
			};
			
			// inputs
			var record_inputs = {
				tags: $(form).find('select.tags')
			};
			
			// enable buttons
			setupButtons(form);
			
			// fade out record content
			$(content).animate({
				opacity: 0.40
			}, 'slow');
			
			// show edit record dialog
			$(holder).block({
				message: $(popup)
			});
			
			// set current selected tags
			var tag_names = [];
			$(record_contents.tags).find('li.tag').each(function() {
				tag_names.push($(this).find('.tag_text').text());
			});
			$(record_inputs.tags).find('option').each(function() {
				
				for (tag_name in tag_names) {
					if (tag_names[tag_name] == $(this).val()) {
						$(this).attr('selected', true);
					}
				}
				
			});
			
			// enable autocompleter (this will auto-populate the selected tags now)
			setupAutocompleter(form);
			
			// populate edit form
			$(record_inputs.tags).parents('.fcbk_container').find('input.maininput').focus();
			$(form).attr('action', $(element).attr('href'));
				
			$(form).ajaxForm({
				beforeSubmit: function(arr, form, options) {
					
					// hide edit confirmation dialog
					$(container).unblock();
					$(container).block({
						message: ''
					});
					
				},
				success: function(data) {
				
					// init
					var message = data.message;
					var record = data.data;
					
					// updated successfully
					if (message.status == 200) {
						
						/******************make into record plugin********************/
						
						//update record on screen
						var new_record_tags = $('#tags_blank ul.tags').clone(false);
						var new_record_tags_tag = $('#tags_blank ul.tags li.tag').clone(false);
						
						$(new_record_tags).html('');
						for (var tag in record.tags) {
							var li_tag = $(new_record_tags_tag).clone();
							
							//tag text
							$(li_tag).find('a.tag_text')
								.text(record.tags[tag].name)
								.attr('href', function(index, attr) {
									return attr.replace(/(\/tags\/)/, '$1' + escape(record.tags[tag].name));
								});
							
							//tag delete
							$(li_tag).find('a.closebutton').attr('href', function(index, attr) {
								return attr.replace(/\/(0)\/(0)/, '/' + escape(record.tags[tag].name) + '/' + record.id);
							});
							$(new_record_tags).append(li_tag);
						}
						setupTags(new_record_tags);
						$(record_contents.footer)
							.html('')
							.append(new_record_tags);
						
						/****************************************************/
						
					}
					
					// something went wrong
					else {
						$.gritterExtend.add(data.message);
					}
					
					//always unblock when done
					$(container).unblock();
					$(content).animate({
						opacity: 1
					}, 'fast');
					
				}
			});
			
			// setup cancel action
			$(popup).find('.cancel_action, .popup_close').bind('click', function(e) {
				content.animate({
					opacity: 1
				}, 'fast');
				$(holder).unblock();
				
				e.preventDefault();
			});
			
			e.preventDefault();
		});
	}
	setupRecordAddTags('body');
	/*
	 * END Record Add Tags actions
	 */
	
	
	/*
	 * Handle Tag delete action (make into plugin!)
	 */
	function setupTagMenuItems(container) {
		$(container).find('a.use_tag_edit').bind('click', function(e) {
			var element = $(this);
			var menu = $(this).parents('.menu');
			var container = $(element).parents('li ');
			var content = $(container).find('.container');
			var popup = $('#tag_edit_form').find('.popup').clone();
			var form = $(popup).find('form');
			var edit_action = $(popup).find('.edit_action');
			var cancel_action = $(popup).find('.cancel_action, .popup_close');
			
			//get edit info
			var tag_name = $(container).find('.name');
			var old_tag_name_text = $(container).find('.name').text(); //so we know what the old value is later
			
			//get edit form inputs
			var tag_name_input = $(form).find('input[name="name"]');
			
			//fill in edit form
			$(form).attr('action', $(element).attr('href'));
			$(tag_name_input).val($(tag_name).text());
			
			//fade out record content
			$(content).animate({
				opacity: 0.40
			}, 'slow');
			
			//show edit confirmation dialog
			$(container).block({
				message: $(popup)
			});
			
			// fix buttons in edit form
			setupButtons(form);
			
			//focus on tag name input
			$(tag_name_input).focus();
			
			$(form).ajaxForm({
				beforeSubmit: function(arr, form, options) {
					
					//hide edit confirmation dialog
					$(container).unblock();
					$(container).block({
						message: ''
					});
					
				},
				success: function(data) {
				
					//init
					var message = data.message;
					var tag = data.data;
					
					//updated successfully
					if (message['status'] == 200) {
						
						//update the displayed tag/href
						tag_name.text(tag.name);
						tag_name.attr('href', function(index, attr) {
							return attr.replace(/(\/tags\/)(.*)$/, '$1' + escape(tag.name));
						});
						
						//update edit href
						$(element).attr('href', function(index, attr) {
							return attr.replace(/(\/api\/tags.json\/)(.*)$/, '$1' + escape(tag.name));
						});
						
						$(content).animate({
							opacity: 1
						}, 'fast');
						
						//update sidebar
						$('#site_sidebar').sidebar('update_tag', old_tag_name_text, tag.name);
						
						//update delete action
						$(container).find('a.use_tag_all_delete').attr('href', function(index, attr) {
							return attr.replace(/(\/api\/tags.json\/)(.*)$/, '$1' + escape(tag.name));
						});
						
					}
					
					//something went wrong
					else {
						$.gritterExtend.add(data.message);
						
						$(content).animate({
							opacity: 1
						}, 'fast');
					}
					
				},
				error: function() {
					$(content).animate({
						opacity: 1
					}, 'fast');
				},
				complete: function() {
					$(container).unblock();
				}
			});
			
			//setup cancel action
			$(cancel_action).bind('click', function(e) {
				$(content).animate({
					opacity: 1
				}, 'fast');
				$(container).unblock();
				
				e.preventDefault();
			});
			
			e.preventDefault();
		});
		
		$(container).find('a.use_tag_all_delete').bind('click', function(e) {
			var element = $(this);
			var menu = $(this).parents('.menu');
			var container = $(element).parents('li ');
			var content = $(container).find('.container');
			var popup = $('#tag_all_delete_confirmation').find('.popup').clone();
			
			//fade out record content
			$(content).animate({
				opacity: 0.40
			}, 'slow');
			
			//show delete confirmation dialog
			$(container).block({
				message: $(popup)
			});
			
			//setup delete action
			$(popup).find('.delete_action').attr('href', $(element).attr('href'));
			$(popup).find('.delete_action').bind('click', function(e) {
				//hide delete confirmation dialog
				$(container).unblock();
				$(container).block({
					message: ''
				});
				
				$.ajax({
					type: 'delete',
					url: $(this).attr('href'),
					success: function(data) {
					
						//init
						var message = data.message;
						
						//deleted successfully
						if (message['status'] == 204) {
							
							$(container).animate({
								opacity: 0
							}, 'slow', 'linear', function() {
								$(container).slideUp('slow', function() {
									$(container).remove();
								});
							});
							
							//update sidebar
							$('#site_sidebar').sidebar('remove_tag', data.data.name);
							
						}
						
						//something went wrong
						else {
							$.gritterExtend.add(data.message);
							
							content.animate({
								opacity: 1
							}, 'fast');
						}
						
					},
					error: function() {
						content.animate({
							opacity: 1
						}, 'fast');
					},
					complete: function() {
						$(container).unblock();
					}
				});
				
				e.preventDefault();
			});
			
			//setup cancel action
			$(popup).find('.cancel_action, .popup_close').bind('click', function(e) {
				content.animate({
					opacity: 1
				}, 'fast');
				container.unblock();
				
				e.preventDefault();
			});
			
			e.preventDefault();
		});
	}
	setupTagMenuItems('body');
	/*
	 * END Handle Tag delete action
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
					var records = data.data.records;
					var new_record = false;
					var page = 2;
					
					//success
					if (message.status == 200) {
						
						var matches = element.attr('href').match(/page\/(\d+)/);
						page = parseInt(matches[1]);
						next_page = page+1;
						
						for (key in records) {
							new_record = buildRecord(records[key], false);
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
						if (records.length < data.data.results_per_page) {
							holder.html(data.message.text);
						}
						else {
							//update page number
							element.attr('href', function(index, attr) {
								return attr.replace(/(page\/)\d+/, '$1' + next_page);
							});
						}
						
					}
					
					//something went wrong
					else {
						$.gritterExtend.add(data.message);
					}
					
				},
				error: function() {
					
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
	$('textarea.use_elastic').elastic();
	
	
	/*
	 * Setup Record/Tag Menus (dropdowns)
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
	$('div.use_tag_menu').dropdownMenus({
		parent_block_selector: 'li.tag',
		show_effect: function(e) {
			e.addClass('hover');
		},
		hide_effect: function(e) {
			e.removeClass('hover');
		}
	});
	/*
	 * END Setup Record/Tag Menus (dropdowns)
	 */
	
	
	/*
	 * Setup Record Form Dropdown Menus
	 */
	function setupFormDropdownMenus(container) {
		$(container).find('div.use_form_menu').dropdownMenus({
			show_effect: function(e) {
				e.addClass('hover');
			},
			hide_effect: function(e) {
				e.removeClass('hover');
			}
		});
		
		//this handles when a user selects an option from a dropdown menu
		$(container).find('div.use_form_menu ul.menu_items li.menu_item').bind('click', function(e) {
			
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
	}
	setupFormDropdownMenus('form.record_form');
	/*
	 * END Setup Record Form Dropdown Menus
	 */
	
	
	/*
	 * Setup Record Form Date Picker
	 */
	function setupDatePicker(container) {
		Date.firstDayOfWeek = 0; //sunday
		$(container).find('.use_datepicker')
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
	}
	setupDatePicker('form.record_form');
	/*
	 * END Setup Record Form Date Picker
	 */
	
	
	/*
	 * Setup Record Form Date Time Selection
	 */
	function setupDateTimeSelection(container) {
		
		$(container).each(function() {
			
			var selections = $(this).find('div.record_form_date, div.record_form_time_hour, div.record_form_time_minute, div.record_form_time_ampm');
			var datetime_reset = $(this).find('div.record_form_datetime_reset');
			
			$(selections)
				.find('.menu_item, .menu_item_datepicker')
				.bind('click', function(e) {
					$(datetime_reset).fadeIn();
					$(this).find('input[name=datetime_set]').val(1);
				});
			
		});
		
	}
	setupDateTimeSelection('#record_create_form');
	/*
	 * END Record Form Date Time Selection
	 */
	
	
	/*
	 * Setup DateTime Selection Auto-Updating (clock)
	 */
	function setupDateTime(container, force_update, datetimestamp) {
		
		$(container).each(function() {
			
			// init
			var now = new Date();
			if (datetimestamp) {
				var now = mysqlTimeStampToDate(datetimestamp);
			}
			
			var selection_menu_items = $(this).find('div.record_form_date, div.record_form_time_hour, div.record_form_time_minute, div.record_form_time_ampm')
				.find('.form_menu .menu_items');
			var date = $(this).find('div.record_form_date');
			var hour = $(this).find('div.record_form_time_hour');
			var minute = $(this).find('div.record_form_time_minute');
			var ampm = $(this).find('div.record_form_time_ampm');
			var datetime_reset = $(this).find('div.record_form_datetime_reset');
			
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
			if (formated_hour < 10) {
				formated_hour = '0' + formated_hour;
			}
			
			//generate minute
			var formated_minute = now.getMinutes();
			if (formated_minute < 10) {
				formated_minute = '0' + formated_minute;
			}
			
			//generate ampm
			var formated_ampm = 'PM';
			if (now.getHours() < 12) {
				formated_ampm = 'AM';
			}
			
			//update selection inputs ONLY if datetime_reset isn't visible
			if (force_update || (!$(selection_menu_items).is(':visible') && $(datetime_reset).is(':hidden'))) {
				$(date).find('.use_datepicker').dpSetSelected(formated_day+'/'+formated_month+'/'+now.getFullYear()); //stupid datepicker
				$(date).find('.menu_header_text').text(formated_date);
				$(date).find('input').val(sql_date);
				
				$(hour).find('.menu_header_text').text(formated_hour);
				$(hour).find('input').val(formated_hour);
				
				$(minute).find('.menu_header_text').text(formated_minute);
				$(minute).find('input').val(formated_minute);
				
				$(ampm).find('.menu_header_text').text(formated_ampm);
				$(ampm).find('input').val(formated_ampm);
				
				$(datetime_reset).find('input').val(0);
			}
		});
		
	}
	setupDateTime('#record_create_form', false, false);
	setInterval(function() { setupDateTime('#record_create_form', false, false); }, 5000);
	/*
	 * END Setup DateTime Selection Auto-Updating (clock)
	 */
	
	
	/*
	 * Setup DateTime Reset
	 */
	function setupDateTimeReset(container, datetime_container) {
		$(container).find('div.use_record_form_datetime_reset').bind('click', function(e) {
			// init
			var datetime = false;
			if (datetime_container) {
				datetime = $(datetime_container).text();
			}
			
			setupDateTime(container, true, datetime);
			$(this).parent().fadeOut();
		});
	}
	setupDateTimeReset('#record_create_form');
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