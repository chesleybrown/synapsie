$(document).ready(function() {
	
	/*
	 * Facebook Login
	 */
	function setupFacebookLogin(container) {
		$(container).find('div.use_facebook_login').delay(500).animate({
			opacity: 1,
			bottom: '+=10'
		}, 'slow');
	}
	setupFacebookLogin('body');
	/*
	 * END Facebook Login
	 */
	
	/*
	 * Facebook Logout
	 */
	function setupFacebookLogout(container) {
		$(container).find('a.use_facebook_logout').bind('click', function(e) {
			var logout_url = $(this).attr('href');
			
			// determine if user is logged in via facebook
			FB.getLoginStatus(function(response) {
				
				// if user is logged in via facebook
				if (response.session) {
					FB.logout(function(response) {
						window.location = logout_url;
					});
				}
				
				// user is not logged in via facebook, default redirect
				else {
					window.location = logout_url;
				}
			});
			
			// prevent default action
			return false;
		});
	}
	setupFacebookLogout('body');
	/*
	 * END Facebook Logout
	 */
	 
});