/*
 * jQuery Sidebar 0.5
 * 
 * Makes it easy to handle adding/removing tags from the sidebar dynamically
 * 
 * @author Chesley Brown
 * 
 */

(function($){
	$.fn.sidebar = function(options, optionName, value)
	{
		// call functions if provided
		switch (options) {
			case 'add_tag':
				return add_tag($(this), optionName);
				break;
			
			case 'update_tag':
				return update_tag($(this), optionName, value);
				break;
			
			case 'remove_tag':
				return remove_tag($(this), optionName);
				break;
		}
		
		// default settings
		var settings = {
			sidebar_tab_used_tags: $('#sidebar_tab_used').find('ul.tags'),
			sidebar_tab_popular_tags: $('#sidebar_tab_popular').find('ul.tags_chart'),
			blank_tag: $('#tags_blank').find('li.tag'),
			blank_popular_tag: $('#popular_tags_blank').find('li.popular_tag')
		};
		
		// merge user provided options
		if (options) {
			$.extend(settings, options);
		}
		
		// init
		var sidebar = $(this);
		$(sidebar).data('sidebar_settings', settings);
		
		// build tag
		function build_tag(sidebar, tag_name) {
			
			//init
			var settings = sidebar.data('sidebar_settings');
			var tag = settings.blank_tag.clone();
			
			// set tag info
			$(tag).hide();
			$(tag).find('a.tag_text').text(tag_name);
			$(tag).find('a.tag_text').attr('href', function(index, attr) {
				return attr + tag_name;
			});
			$(tag).find('a.closebutton').remove();
			
			// tag is ready to show
			return tag;
			
		}
		
		// build popular tag
		function build_popular_tag(sidebar, tag_name) {
			
			//init
			var settings = sidebar.data('sidebar_settings');
			var sidebar_tab_popular_tags = settings.sidebar_tab_popular_tags;
			var popular_tag = settings.blank_popular_tag.clone();
			var tag = false;
			var popular_tag_percent = 100;
			var popular_tag_value = 1;
			var tag_highest = 0;
			
			// build tag
			tag = build_tag(sidebar, tag_name);
			$(tag).show();
			
			// determine width of this tags
			tag_highest = sidebar_tab_popular_tags.find('li:first div.content span.value').text();
			popular_tag_percent = Math.round((parseInt(popular_tag_value) / parseInt(tag_highest)) * 100);
			
			// set popular tag info
			$(popular_tag).hide();
			$(popular_tag).find('div.label ul.tags').html(tag);
			$(popular_tag).find('div.content span.value')
				.css('width', popular_tag_percent + '%')
				.text(popular_tag_value);
			
			// popular tag is ready to show
			return popular_tag;
			
		}
		
		// for finding a tag container by tag_name
		function find_tag(sidebar, tag_name) {
			
			//init
			var settings = sidebar.data('sidebar_settings');
			var sidebar_tab_used_tags = $(settings.sidebar_tab_used_tags);
			var tag = false;
			
			// find tag
			tag = $(sidebar_tab_used_tags).find('li.tag').filter(function(index) {
				if ($(this).find('.tag_text').text() == tag_name) {
					return true;
				}
				return false;
			});
			
			return tag;
			
		}
		
		// for finding a popular tag container by tag_name
		function find_popular_tag(sidebar, popular_tag_name) {
			
			//init
			var settings = sidebar.data('sidebar_settings');
			var sidebar_tab_popular_tags = $(settings.sidebar_tab_popular_tags);
			var popular_tag_tag = false;
			var popular_tag = false;
			
			// find the popular tag
			popular_tag_tag = $(sidebar_tab_popular_tags).find('li.tag').filter(function(index) {
				if ($(this).find('.tag_text').text() == popular_tag_name) {
					return true;
				}
				return false;
			});
			popular_tag = $(popular_tag_tag).parents('li.popular_tag');
			
			return popular_tag;
			
		}
		
		// insert tag (involves sorting)
		function insert_tag(sidebar, tag) {
			
			//init
			var settings = sidebar.data('sidebar_settings');
			var sidebar_tab_used_tags = $(settings.sidebar_tab_used_tags);
			var after_tag = false;
			var already_exists = false;
			
			// determine where to add tag
			$(sidebar_tab_used_tags).find('li').each(function() {
				// abort if tag already exists
				if ($(this).find('a.tag_text').text() == $(tag).find('a.tag_text').text()) {
					already_exists = true;
				}
				else if ($(this).find('a.tag_text').text() < $(tag).find('a.tag_text').text()) {
					after_tag = $(this);
				}
			});
			
			// abort if tag already exists
			if (already_exists) {
				return false;
			}
			
			// can go after a current tag
			if (after_tag) {
				$(after_tag).after(tag);
			}
			
			// can't go after anything... must be first
			else if ($(sidebar_tab_used_tags).children('li').length > 0) {
				$(sidebar_tab_used_tags).prepend(tag);
			}
			
			// nothing it can go after, just append
			else {
				$(sidebar_tab_used_tags).append(tag);
			}
			
			// fade it all fancy
			$(tag).fadeIn('slow');
			
			return true;
			
		}
		
		// insert popular tag
		function insert_popular_tag(sidebar, popular_tag) {
			
			//init
			var settings = sidebar.data('sidebar_settings');
			var sidebar_tab_popular_tags = $(settings.sidebar_tab_popular_tags);
			var popular_tag_name = $(popular_tag).find('div.label ul.tags .tag_text').text();
			var tag_highest = 0;
			var popular_tag_percent = 0;
			var popular_tag_value = 0;
			var current_popular_tag = false;
			var after_tag = false;
			var popular_tag_value = 0;
			
			//see if the popular tag already exists
			$(sidebar_tab_popular_tags).find('li.popular_tag').each(function() {
				if ($(this).find('a.tag_text').text() == $(popular_tag).find('a.tag_text').text()) {
					current_popular_tag = $(this);
				}
			});
			
			// if tag already exists, just increase current counter
			if ($(current_popular_tag).length > 0) {
				
				//increment
				popular_tag_value = $(current_popular_tag).find('div.content span.value');
				popular_tag_value.text(parseInt(popular_tag_value.text()) + 1);
				
				// determine width of this popular tag
				tag_highest = sidebar_tab_popular_tags.find('li:first div.content span.value').text();
				popular_tag_percent = Math.round((parseInt($(popular_tag_value).text()) / parseInt(tag_highest)) * 100);
				
				// set popular tag info
				$(popular_tag_value).css('width', popular_tag_percent + '%');
				
				// forgot the popular tag, we are just going to move around the current one
				popular_tag = current_popular_tag;
				
			}
			
			// get the current popular tag value
			popular_tag_value = parseInt($(popular_tag).find('div.content span.value').text());
			
			// determine where to add popular tag
			$(sidebar_tab_popular_tags).find('li.popular_tag').each(function() {
				var current_popular_tag_value = parseInt($(this).find('div.content span.value').text());
				
				if (current_popular_tag_value > popular_tag_value) {
					after_tag = $(this);
				}
			});
			
			// can go after a current tag
			if (after_tag) {
				$(after_tag).after(popular_tag);
			}
			
			// can't go after anything... must be first
			else if ($(sidebar_tab_popular_tags).children('li.popular_tag').length > 0) {
				$(sidebar_tab_popular_tags).prepend(popular_tag);
			}
			
			// nothing it can go after, just append
			else {
				$(sidebar_tab_popular_tags).append(popular_tag);
			}
			
			// fade it all fancy
			$(popular_tag).fadeIn('slow');
			
			return true;
			
		}
		
		// add new tag (will not add it if it already exists)
		function add_tag(sidebar, tag_name) {
			
			//init
			var settings = sidebar.data('sidebar_settings');
			var sidebar_tab_used_tags = $(settings.sidebar_tab_used_tags);
			var sidebar_tab_popular_tags = $(settings.sidebar_tab_popular_tags);
			var tag = false;
			var popular_tag = false;
			
			// build the tag
			tag = build_tag(sidebar, tag_name);
			
			// build the popular tag container
			popular_tag = build_popular_tag(sidebar, tag_name);
			
			// add tag
			insert_tag(sidebar, tag);
			insert_popular_tag(sidebar, popular_tag);
			
			return true;
			
		}
		
		// update existing tag
		function update_tag(sidebar, old_tag_name, new_tag_name) {
			
			//init
			var settings = sidebar.data('sidebar_settings');
			var sidebar_tab_used_tags = $(settings.sidebar_tab_used_tags);
			var sidebar_tab_popular_tags = $(settings.sidebar_tab_popular_tags);
			var tag = false;
			var new_tag = false;
			var popular_tag_tag = false;
			var popular_tag = false;
			
			// find the tag
			tag = find_tag(sidebar, old_tag_name);
			
			// find the popular tag
			popular_tag = find_popular_tag(sidebar, old_tag_name);
			
			// update the tag
			new_tag = $(tag).clone();
			new_tag.find('a.tag_text').text(new_tag_name);
			new_tag.find('a.tag_text').attr('href', function(index, attr) {
				return attr.replace(/(\/tags\/).*/, '$1' + new_tag_name);
			});
			
			// update the popular tag
			new_popular_tag = $(popular_tag).clone();
			new_popular_tag.find('a.tag_text').text(new_tag_name);
			new_popular_tag.find('a.tag_text').attr('href', function(index, attr) {
				return attr.replace(/(\/tags\/).*/, '$1' + new_tag_name);
			});
			
			// remove old tag
			$(tag).remove();
			$(popular_tag).remove();
			
			// update location of tag (sort)
			insert_tag(sidebar, new_tag);
			insert_popular_tag(sidebar, new_popular_tag);
			
			return true;
			
		}
		
		// remove existing tag
		function remove_tag(sidebar, tag_name) {
			
			//init
			var settings = sidebar.data('sidebar_settings');
			var sidebar_tab_used_tags = $(settings.sidebar_tab_used_tags);
			var sidebar_tab_popular_tags = $(settings.sidebar_tab_popular_tags);
			var tag = false;
			var popular_tag = false;
			
			// find the tag
			tag = find_tag(sidebar, tag_name);
			
			// find the popular tag
			popular_tag = find_popular_tag(sidebar, tag_name);
			
			// remove the tag
			$(tag).fadeOut('slow', function() {
				$(this).remove();
			});
			
			// remove the popular tag
			$(popular_tag).fadeOut('slow', function() {
				$(this).remove();
			});
			
			return true;
			
		}
		
	}
	
})(jQuery); 