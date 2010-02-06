/* Record Menu (should be made a plugin) */

$(document).ready(function() {
	
	/*
	$('ul.records li.record').each(function(e) {
		//init
		var record = $(this);
		var menu = $(this).find('div.menu');
		var menu_header = $(this).find('div.menu ul.menu_headers li.menu_header');
		var menu_items = menu.find('ul.menu_items');
		
		record.hover(
			function(e) {
				if (menu_items.is(':hidden')) {
					menu.show();
				}
			},
			function(e) {
				if (menu_items.is(':hidden')) {
					menu.hide();
				}
			}
		);
		
		menu.bind('click', function(e) {
			
			if (menu_items.is(':hidden')) {
				$('#site_master').show();
				menu_items.show();
				menu_header.addClass('active');
			}
			else {
				menu_header.removeClass('active');
				menu_items.hide();
				$('#site_master').hide();
			}
		});
	});
	*/

});