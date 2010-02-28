/* Should be made a simple plugin */

$(document).ready(function() {

	//When page loads...
	$(".use_tabs div.sidebar_tab_container div.sidebar_tab_content").hide(); //Hide all content
	$(".use_tabs ul.sidebar_tabs li:first").addClass("active").show(); //Activate first tab
	$(".use_tabs div.sidebar_tab_container div.sidebar_tab_content:first").show(); //Show first tab content

	//On Click Event
	$(".use_tabs ul.sidebar_tabs li").click(function() {
		
		// init
		var active_class = 'active';
		
		if (!$(this).hasClass(active_class)) {
			$("ul.sidebar_tabs li").removeClass(active_class); //Remove any "active" class
			$(this).addClass(active_class); //Add "active" class to selected tab
			$("div.sidebar_tab_container div.sidebar_tab_content").hide(); //Hide all tab content
	
			var activeTab = $(this).find("a").attr("href"); //Find the href attribute value to identify the active tab + content
			$(activeTab).fadeIn(); //Fade in the active ID content
		}
		
		return false;
	});

});