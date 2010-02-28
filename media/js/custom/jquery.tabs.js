/* Should be made a simple plugin */

$(document).ready(function() {

	//When page loads...
	$(".use_tabs").each(function() {
		$(this).find("div.tab_container div.tab_content").hide(); //Hide all content
		$(this).find("ul.tabs li:first").addClass("active").show(); //Activate first tab
		$(this).find("div.tab_container div.tab_content:first").show(); //Show first tab content
	});

	//On Click Event
	$(".use_tabs ul.tabs li").click(function(e) {
		
		// init
		var active_class = 'active';
		var tab_headers = $(this).parent('ul');
		
		if (!$(this).hasClass(active_class)) {
			tab_headers.find("li").removeClass(active_class); //Remove any "active" class
			$(this).addClass(active_class); //Add "active" class to selected tab
			tab_headers.siblings('div.tab_container').find("div.tab_content").hide(); //Hide all tab content
	
			var activeTab = $(this).find("a").attr("href"); //Find the href attribute value to identify the active tab + content
			$(activeTab).fadeIn(); //Fade in the active ID content
		}
		
		return e.preventDefault();
	});

});