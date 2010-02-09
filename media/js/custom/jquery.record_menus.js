/*
 * jQuery RecordMenus 0.6
 * 
 * Add a "Dropdown" menu when you hover over a record
 * 
 * @author Chesley Brown
 * 
 */

(function($){
	$.fn.recordMenus = function(options, optionName, value)
	{
		// call functions if provided
		switch (options) {
			case 'show':
				return show($(this));
				break;
			
			case 'hide':
				return hide($(this));
				break;
		}
		
		// default settings
		var settings = {
			site_master_selector: 'body',
			record_selector: 'li.record',
			menu_selector: 'div.menu',
			menu_header_selector: 'div.menu ul.menu_headers li.menu_header',
			menu_items_selector: 'div.menu ul.menu_items',
			active_class: 'active', // this is applied to both the menu container and the menu header
			show_effect: function(e) {
				e.show();
			},
			hide_effect: function(e) {
				e.hide();
			}
		};
		
		// merge user provided options
		if (options) {
			$.extend(settings, options);
		}
		
		// init
		var records = $(this);
		var site_master = $(settings.site_master_selector);
		
		//save settings to data
		records.data('record_menus_settings', settings);
		
		// clicking outside menu closes all menus that might be open
		site_master.bind('click.recordsMenuMaster', function(e) {
			var container = records;
			
			container.each(function(e) {
				var menu_items = $(this).find(settings.menu_items_selector);
				if (menu_items.is(':visible')) {
					hide($(this));
				}
			});
		});
			
		
		// init the menus
		records.each(function() {
			
			//init
			var container = $(this);
			var menu = container.find(settings.menu_selector);
			var menu_items = container.find(settings.menu_items_selector);
			
			container.hover(
				function(e) {
					show(container);
				},
				function(e) {
					if (menu_items.is(':hidden')) {
						hide(container);
					}
				}
			);
			
			container.bind('click.recordsMenu', function(e) {
				
				/* 
				 * this prevents the menu from complete disappearing if the user
				 * simply clicked outside the menu, but within the same record
				 */
				if (menu_items.is(':visible')) {
					hide_menu(container);
					e.stopPropagation();
				}
				
			});
			
			menu.bind('click.recordsMenu', function(e) {
				toggle_menu(container);
				e.stopPropagation();
			});
			
		});
		
		function show(element) {
			//init
			var settings = element.data('record_menus_settings');
			var menu = element.find(settings.menu_selector);
			
			settings.show_effect(menu);
		}
		
		function hide(element) {
			//init
			var settings = element.data('record_menus_settings');
			var menu = element.find(settings.menu_selector);
			var menu_items = element.find(settings.menu_items_selector);
			
			settings.hide_effect(menu);
			hide_menu(element, settings);
		}
		
		function toggle_menu(element) {
			//init
			var settings = element.data('record_menus_settings');
			var menu_items = element.find(settings.menu_items_selector);
			
			if (menu_items.is(':hidden')) {
				show_menu(element, settings);
			}
			else {
				hide_menu(element, settings);
			}
		}
		
		function show_menu(element) {
			//init
			var settings = element.data('record_menus_settings');
			var menu = element.find(settings.menu_selector);
			var menu_header = element.find(settings.menu_header_selector);
			var menu_items = element.find(settings.menu_items_selector);
			
			//close all other menus
			element.parents('ul.records').find(settings.record_selector).not(element).each(function(e) {
				hide($(this));
			});
			
			menu_items.fadeIn('fast');
			menu.addClass(settings.active_class);
			menu_header.addClass(settings.active_class);
		}
		
		function hide_menu(element) {
			//init
			var settings = element.data('record_menus_settings');
			var menu = element.find(settings.menu_selector);
			var menu_header = element.find(settings.menu_header_selector);
			var menu_items = element.find(settings.menu_items_selector);
			
			menu_items.hide();
			menu.removeClass(settings.active_class);
			menu_header.removeClass(settings.active_class);
		}
		
	}
})(jQuery); 