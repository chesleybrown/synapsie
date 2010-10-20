/*
 * Extend Gritter for jQuery
 * http://www.boedesign.com/
 *
 * Copyright (c) 2010 Chesley Brown
 * Dual licensed under the MIT and GPL licenses.
 *
 * Date: March 20, 2010
 * Version: 0.2
 */

(function($){
 	
	/**
	* Set it up as an object under the jQuery namespace
	*/
	$.gritterExtend = {};
	
	/**
	* Set up global options that the user can over-ride
	*/
	$.gritterExtend.options = {
		success_image: '/site_media/media/img/icons/luna-grey-icons/48x48/accept.png',
		created_image: '/site_media/media/img/icons/luna-grey-icons/48x48/add.png',
		deleted_image: '/site_media/media/img/icons/luna-grey-icons/48x48/delete.png',
		error_image: '/site_media/media/img/icons/luna-grey-icons/48x48/remove.png',
		info_image: '/site_media/media/img/icons/luna-grey-icons/48x48/info.png'
	}
	
	/**
	* Add a gritter notification to the screen
	* @see Gritter#add();
	*/
	$.gritterExtend.add = function(params){
		return GritterExtend.add(params || {});
	}
	$.gritterExtend.adds = function(messages){
		return GritterExtend.adds(messages || []);
	}
	$.gritterExtend.parse = function(){
		return GritterExtend.parse();
	}
	
	var GritterExtend = {
		
		// Public - options to over-ride with $.gritterExtend.options in "add"
		success_image: '',
		created_image: '',
		deleted_image: '',
		error_image: '',
		info_image: '',
		messages_container: $('#site_messages'),
		
		add: function(params) {
			
			//init
			var gritter_title = params['title'];
			var gritter_text = params['text'];
			var gritter_image = false;
			var gritter_sticky = params['sticky'];
			var kind = params['kind']
			
			//merge user provided options
			for(opt in $.gritterExtend.options){
				this[opt] = $.gritterExtend.options[opt];
			}
			
			//determine image by notice type
			if (kind == 'success') {
				gritter_image = this.success_image;
			}
			else if (kind == 'created') {
				gritter_image = this.created_image;
			}
			else if (kind == 'deleted') {
				gritter_image = this.deleted_image;
			}
			else if (kind == 'error') {
				gritter_image = this.error_image;
			}
			else if (kind == 'info') {
				gritter_image = this.info_image;
			}
			
			$.gritter.add({
				title: gritter_title,
				text: gritter_text,
				image: gritter_image,
				sticky: gritter_sticky
			});
			
		},
		
		// makes it simple to add an array of messages
		adds: function(messages) {
			for (message in messages) {
				$.gritterExtend.add(messages[message]);
			}
			
			return true;
		},
		
		parse: function() {
			
			//init
			var messages = [];
			
			//merge user provided options
			for(opt in $.gritterExtend.options){
				this[opt] = $.gritterExtend.options[opt];
			}
			
			$(this.messages_container).find('li.message').each(function() {
				
				//init
				var message = {
					'status': '',
					'title': '',
					'text': '',
					'sticky': false,
					'king': ''
				};
				
				message['status'] = parseInt($(this).find('.status').text());
				message['title'] = $(this).find('.title').text();
				message['text'] = $(this).find('.text').text();
				message['sticky'] = ($(this).find('.sticky').text() != 'False');
				message['kind'] = $(this).find('.kind').text();
				
				//append to messages array
				messages.push(message);
			});
			
			return messages;
			
		}
		
	}
	
})(jQuery);