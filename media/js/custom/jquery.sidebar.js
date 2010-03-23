/*
 * jQuery Sidebar 0.3
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
			sidebar_tab_popular_tags: $('#sidebar_tab_popular').find('ul.tags'),
			blank_tag: $('#tags_blank').find('li.tag')
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
			tag.hide();
			tag.find('a.tag_text').text(tag_name);
			tag.find('a.tag_text').attr('href', function(index, attr) {
				return attr + tag_name;
			});
			tag.find('a.closebutton').remove();
			
			// tag is ready to show
			return tag;
			
		}
		
		// insert tag (involves sorting)
		function insert_tag(sidebar, tag) {
			
			//init
			var settings = sidebar.data('sidebar_settings');
			var sidebar_tab_used_tags = $(settings.sidebar_tab_used_tags);
			var after_tag = false;
			var already_exists = false;
			
			// add tag
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
		
		// add new tag (will not add it if it already exists)
		function add_tag(sidebar, tag_name) {
			
			//init
			var settings = sidebar.data('sidebar_settings');
			var sidebar_tab_used_tags = $(settings.sidebar_tab_used_tags);
			var sidebar_tab_popular_tags = $(settings.sidebar_tab_popular_tags);
			var tag = false;
			
			// build the tag
			tag = build_tag(sidebar, tag_name);
			
			// only add tag if it isn't already there.
			if ($(sidebar_tab_used_tags).find('li.tag .tag_text:contains("' + tag.text() + '")').length > 0) {
				return false;
			}
			
			// add tag
			insert_tag(sidebar, tag);
			
			//sidebar_tab_popular_tags.append(tag);
			
			return true;
			
		}
		
		// update existing tag
		function update_tag(sidebar, old_tag_name, new_tag_name) {
			
			//init
			var settings = sidebar.data('sidebar_settings');
			var sidebar_tab_used_tags = $(settings.sidebar_tab_used_tags);
			var sidebar_tab_popular_tags = $(settings.sidebar_tab_popular_tags);
			var tag = false;
			
			// find the tag
			tag = $(sidebar_tab_used_tags).find('li.tag').filter(function(index) {
				if ($(this).find('.tag_text').text() == old_tag_name) {
					return true;
				}
				return false;
			});
			
			// update the tag
			new_tag = $(tag).clone();
			new_tag
				.find('a.tag_text').text(new_tag_name)
				.find('a.tag_text').attr('href', function(index, attr) {
					return attr.replace(/(tags\/)(.*)/, '$1' + new_tag_name);
				});
			
			// remove old tag
			$(tag).remove();
			
			// update location of tag (sort)
			insert_tag(sidebar, new_tag);
			
			return true;
			
		}
		
		// remove existing tag
		function remove_tag(sidebar, tag_name) {
			
			//init
			var settings = sidebar.data('sidebar_settings');
			var sidebar_tab_used_tags = $(settings.sidebar_tab_used_tags);
			var sidebar_tab_popular_tags = $(settings.sidebar_tab_popular_tags);
			var tag = false;
			
			// find the tag
			tag = $(sidebar_tab_used_tags).find('li.tag').filter(function(index) {
				if ($(this).find('.tag_text').text() == tag_name) {
					return true;
				}
				return false;
			});
			
			// remove the tag
			if (tag.length > 0) {
				tag.fadeOut('slow', function() {
					$(this).remove();
				});
			}
			
			return true;
			
		}
		
	}
	
})(jQuery); 