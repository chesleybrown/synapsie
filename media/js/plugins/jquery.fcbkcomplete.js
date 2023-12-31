/*
 FCBKcomplete 2.6.2.13
 - Jquery version required: 1.2.x, 1.3.x
 
 Changelog:
 
 - 2.00	new version of fcbkcomplete
 
 - 2.01 fixed bugs & added features
 		fixed filter bug for preadded items
 		focus on the input after selecting tag
 		the element removed pressing backspace when the element is selected
 		input tag in the control has a border in IE7
 		added iterate over each match and apply the plugin separately
 		set focus on the input after selecting tag
 
 - 2.02 fixed fist element selected bug
 		fixed defaultfilter error bug
 
 - 2.5 	removed selected="selected" attribute due ie bug
 		element search algorithm changed
 		better performance fix added
 		fixed many small bugs
 		onselect event added
 		onremove event added
 		
 - 2.6 	ie6/7 support fix added
 		added new public method addItem due request
 		added new options "firstselected" that you can set true/false to select first element on dropdown list
 		autoexpand input element added
 		removeItem bug fixed
 		and many more bug fixed

 - 2.6.1
 		fixed public method to use it $("elem").trigger("addItem",[{"title": "test", "value": "test"}]);
 
 - 2.6.2.1
 		made onselect, onremove take an anonymous function
 		focus on maininput when deleting an item via the click option
 
 - 2.6.2.2
 		add 'clear' option
 		
 - 2.6.2.3
 		added use of .attr instead of get(0).setAttribute which didn't seem to work after a form submit
 		added use of .filter() with function instead of a selector for finding option.val that already exists
 		
 - 2.6.2.4
 		using + 2 for the size instead of + 1 because text was getting cut off in Safari
 	
 - 2.6.2.5
 		added option to disable the default message
 	
 - 2.6.2.6
 		added option to provide keys that would trigger an addItem (instead of just enter/return)
 
 - 2.6.2.7
 		added a wrapper element for the tag text
 
 - 2.6.2.8
 		added option to prevent user from adding the same tag twice
 	
 - 2.6.2.9
 		fixed preSetting up the tags that are already selected on load
 	
 - 2.6.2.10
 		removed complete fadein/fadeout... was just causing issues in my layout
 		added addItemToCache function
 		using addItemToCache function to dynamically add items to the cache if they don't already exist in the cache
 		
 - 2.6.2.11
 		added better value filtering so that it doesn't break if tags contain odd characters
 	
 - 2.6.2.12
 		removed use of fcbk IDs so that we can have multiple on a single page
 		
 - 2.6.2.13
 		only prevent enter if the maininput is empty
 		
 */

/* Coded by: emposha <admin@emposha.com> */
/* Copyright: Emposha.com <http://www.emposha.com/> - Distributed under MIT - Keep this message! */
/*
 * json_url         - url to fetch json object
 * cache       		- use cache
 * height           - maximum number of element shown before scroll will apear
 * newel            - show typed text like a element
 * firstselected	- automaticly select first element from dropdown
 * filter_case      - case sensitive filter
 * filter_selected  - filter selected items from list
 * complete_text    - text for complete page
 * maxshownitems	- maximum numbers that will be shown at dropdown list (less better performance)
 * onselect			- fire event on item select
 * onremove			- fire event on item remove
 * allow_duplicates - boolean to allow the same tag to be added twice in the input
 */
 
jQuery(
    function ($) 
    {
	    $.fn.fcbkcomplete = function (opt) 
	    {
    		return this.each(function()
			{
		        function init()
		        {
		           createFCBK();
	               preSet();
	               addInput(0); 
		        }
	        	
		        function createFCBK()
		        {
					//everthing needs to reside within the fbck container
					$(element).after(container);
					$(container).append(element);
					
					element.hide();
					element.attr("multiple","multiple");
					if (element.attr("name").indexOf("[]") == -1) {
						element.attr("name",element.attr("name")+"[]");
					}
					
					holder = $(document.createElement("ul"));
					holder.attr("class", "holder");
					element.after(holder);
					
					complete = $(document.createElement("div"));
					complete.addClass("facebook-auto");
					
					if (options.complete_text) {
						complete.append('<div class="default">'+ options.complete_text +"</div>");
					}
					
					if (browser_msie) {
						complete.append('<iframe class="ie6fix" scrolling="no" frameborder="0"></iframe>');
						browser_msie_frame = complete.children('.ie6fix');
					}
					
					feed = $("<ul></ul>");
					feed.attr("class", "feed");
					
					complete.prepend(feed);
					holder.after(complete);
					feed.css("width",complete.width());
					
					//save where the holder is
					element.data('fcbkcompleteHolder', holder);
		        }
	        	
		        function preSet()
		        {
		            element.children("option").each( 
		                function(i,option) 
		                {
							option = $(option);
		                    if (option.hasClass("selected") || option.is(':selected'))
		                    {
		                        addItem (option.text(), option.val(), true);
								option.attr("selected","selected");
		                    } 
							else
							{
								option.removeAttr("selected");
							}

							cache.push({
								caption: option.text(),
								value: option.val()
							});
							search_string += "" + (cache.length - 1) + ":" + option.text() + ";";
		                }
		            );
		        }
				
				//public method to add new item
				$(this).bind("addItem", function(event, data)
				{					
					addItem(data.title, data.value);
				});
				
				function addItemToCache(value, caption) {
					
					if (cache) {
						cache.push (
							{
								caption: caption,
								value: value
							}
						);
						search_string += "" + (cache.length - 1) + ":" + value + ";";
					}
					
				}
	        	
		        function addItem (title, value, preadded)
		        {
	                var _item;
                    _item = element.children("option").filter(function(index) {
						return $(this).val() == value;
					});
					var added_already = _item.attr("selected");
					
					if (preadded || (!added_already || options.allow_duplicates)) {
						
		                var li = document.createElement("li");
		                var txt = document.createTextNode(title);
		                var aclose = document.createElement("a");
		                var text_container = $('<span></span>')
		                	.addClass('tag_text')
		                	.text(title);
		                
		                $(li).attr({"class": "bit-box","rel": value});
		                
		                $(li).prepend(text_container);
		                $(aclose).attr({"class": "closebutton","href": "#"});
		                
		                li.appendChild(aclose);
		                holder.append(li);
		                
		                $(aclose).click(
		                    function(){
		                        $(this).parent("li").fadeOut("fast", 
		                            function(){
										removeItem($(this));
										holder.find('input.maininput').focus();
		                            }
		                        );
		                        return false;
		                    }
		                );
		            }
					
	                if (!preadded) 
	                {
	                    $(container).find("li.annoninput").remove();
	                    addInput(1);
						
						if (!added_already || options.allow_duplicates) {
		                    if (_item.length)
		                    {   
								
		                        _item.attr("selected", "selected");
		                        
								if (!_item.hasClass("selected"))
								{
									_item.addClass("selected");
								}
		                    }
		                    else
		                    {
		                        _item = $(document.createElement("option"));
		                        _item.attr("value", value).attr("selected", "selected");
								_item.attr("value", value).addClass("selected");
		                        _item.text(title);
		                        element.append(_item);
		                        
		                        //add new item to cache
		                		addItemToCache(title, title);
		                    }
		                    if (typeof(options.onselect) == 'function')
		                    {
		                    	options.onselect(_item);
		                    }
							else if (options.onselect.length)
							{
								funCall(options.onselect,_item);
							}
						}
	                }
	                
	                holder.children("li.bit-box.deleted").removeClass("deleted");
	                feed.hide();
					browser_msie?browser_msie_frame.hide():'';
	            }
	        	
				function removeItem(item)
				{
					var element_options_filtered = element.children("option").filter(function(index, element) {
						return ($(this).val() == item.attr("rel"));
					});
					
					$(element_options_filtered)
						.removeAttr("selected")
						.removeAttr('class');
					
					if (typeof(options.onremove) == 'function')
					{
						var _item = $(element_options_filtered);
						options.onremove(_item);
					}
					else if (options.onremove.length)
					{
					    var _item = $(element_options_filtered);
						funCall(options.onremove,_item);
					}
					
                    item.remove();
					deleting = 0;
				}
				
		        function addInput(focusme)
		        {
		            var li = $(document.createElement("li"));
	                var input = $(document.createElement("input"));
	                
	                li.attr({"class": "bit-input annoninput"});
	                input.attr({"type": "text","class": "maininput","size": "1"});
	                holder.append(li.append(input));
	                
	                input.focus(
	                    function()
	                    {
	                        complete.show();
	                    }
	                );
	                
	                input.blur(
	                    function()
	                    {
	                        complete.hide();
	                    }
	                );
	                
	                holder.click(
	                    function()
	                    {
	                        input.focus();
				            if (feed.length && input.val().length) 
				            {
					            feed.show();
				            }
				            else 
				            {				
					            feed.hide();
								browser_msie?browser_msie_frame.hide():'';
					            complete.children(".default").show();
				            }
	                    }
	                );
	                
					input.keypress(
	                    function(event)
	                    {
	                    	// only prevent enter if the maininput is empty
	                        if (event.keyCode == 13 && input.val() != ''){
							    return false;
							}
							//auto expand input
							input.attr("size",input.val().length + 2);
	                    }
	                );
					
					input.keydown(
	                    function(event)
	                    {
							//prevent to enter some bad chars when input is empty
							if(event.keyCode == 191)
							{
								event.preventDefault();
								return false;
							}
	                    }
	                );
					
	                input.keyup(
	                    function(event)
	                    {
							var etext = xssPrevent(input.val());
														
							if (event.keyCode == 8 && etext.length == 0)
							{			
								feed.hide();
								browser_msie?browser_msie_frame.hide():'';
								if (holder.children("li.bit-box.deleted").length == 0) 
								{
									holder.children("li.bit-box:last").addClass("deleted");
									return false;
								}
								else 
								{
									if (deleting)
								    {
								        return;
								    }
									deleting = 1;
									holder.children("li.bit-box.deleted").fadeOut("fast", function()
									{
										removeItem($(this));
										return false;
									});
								}
							}
							
	                        if (event.keyCode != 40 && event.keyCode != 38 && etext.length != 0) 
	                        {
	                            counter = 0;
								
	                            if (options.json_url) 
	                            {
	                                if (options.cache && json_cache) 
	                                {
	                                    addMembers(etext);
	                                    bindEvents();
	                                }
	                                else 
	                                {
	                                    $.getJSON(options.json_url + "?tag=" + etext, null, 
	                                        function(data)
	                                        {
	                                            addMembers(etext, data);
	                                            json_cache = true;
	                                            bindEvents();
	                                        }
	                                    );
	                                }
	                            }
	                            else 
	                            {
									addMembers(etext);
	                                bindEvents();
	                            }
	                            complete.children(".default").hide();
								feed.show();
	                        }
	                    }
	                );
					if (focusme)
					{
						setTimeout(function(){
							input.focus();
							complete.children(".default").show();
						},1);
					}
		        }
	        	
				function addMembers(etext, data)
				{
					feed.html('');
					
					if (!options.cache) 
					{
						cache = new Array();
						search_string = "";
					}
					
					addTextItem(etext);
					
					if (data != null && data.length)
					{
						$.each(data, 
	                    	function(i, val)
	                    	{
								cache.push (
									{
										caption: val.caption,
										value: val.value
									}
								);
								search_string += "" + (cache.length - 1) + ":" + val.caption + ";";
							}
						);	
					}
					
					var maximum = options.maxshownitems<cache.length?options.maxshownitems:cache.length;
					var filter = "i";
					if (options.filter_case)
					{
						filter = ""; 
					}
					
					var myregexp, match;
					try {
						myregexp = eval('/(?:^|;)\\s*(\\d+)\\s*:[^;]*?' + etext + '[^;]*/g' + filter);
						match = myregexp.exec(search_string);
					} catch(ex){};
										
					var content = '';
					while (match != null && maximum > 0) 
					{
						var id = match[1];
						var object = cache[id];
						var element_options_filtered = element.children("option").filter(function(index, element) {
							return ($(this).val() == object.value);
						});
						if (options.filter_selected && $(element_options_filtered).hasClass("selected")) 
						{
							//nothing here...
						}
						else 
						{
							content += '<li rel="' + object.value + '">' + itemIllumination(object.caption, etext) + '</li>';
							counter++;
							maximum--;
						}
						match = myregexp.exec(search_string);
					}
					feed.append(content);
					
					if (options.firstselected)
					{
					    focuson = feed.children("li:visible:first");
					    focuson.addClass("auto-focus");
					}
					
					if (counter > options.height) 
	                {
	                    feed.css({"height": (options.height * 24) + "px","overflow": "auto"});
						if (browser_msie)
	                    {
	                        browser_msie_frame.css({"height": (options.height * 24) + "px", "width": feed.width() + "px"}).show();
	                    }
	                }
	                else 
	                {
	                    feed.css("height", "auto");
						if (browser_msie)
	                    {
	                        browser_msie_frame.css({"height": feed.height() + "px", "width": feed.width() + "px"}).show();
	                    }
	                }
				}
				
				function itemIllumination(text, etext)
				{
					if (options.filter_case) 
                    {     
						try {
							eval("var text = text.replace(/(.*)(" + etext + ")(.*)/gi,'$1<em>$2</em>$3');");
						} catch(ex){};
                    }
                    else 
                    {    
						try {
							eval("var text = text.replace(/(.*)(" + etext.toLowerCase() + ")(.*)/gi,'$1<em>$2</em>$3');");
						}catch(ex){};
                    }					
					return text;
				}
	        	
		        function bindFeedEvent() 
		        {		
			        feed.children("li").mouseover(
			            function()
			            {
				            feed.children("li").removeClass("auto-focus");
	                        $(this).addClass("auto-focus");
	                        focuson = $(this);
	                    }
	                );
	        		
			        feed.children("li").mouseout(
			            function()
			            {
	                        $(this).removeClass("auto-focus");
	                        focuson = null;
	                    }
	                );
		        }
	        	
		        function removeFeedEvent() 
		        {       	
			        feed.children("li").unbind("mouseover");	
			        feed.children("li").unbind("mouseout");
			        feed.mousemove(
			            function () 
			            {
				            bindFeedEvent();
				            feed.unbind("mousemove");
			            }
			        );	
		        }
	        	
		        function bindEvents()
		        {
		            var maininput = $(container).find("li.annoninput").children(".maininput");
	       	        bindFeedEvent();      	
	                feed.children("li").unbind("mousedown");
	                feed.children("li").mousedown( 
	                    function()
	                    {
	                        var option = $(this);
	                        addItem(option.text(),option.attr("rel"));
	                        feed.hide();
							browser_msie?browser_msie_frame.hide():'';
	                        complete.hide();
	                    }
	                );
	                
	                maininput.unbind("keydown");
	                maininput.keydown(
	                    function(event)
	                    {		
							if(event.keyCode == 191)
							{								
								event.preventDefault();
								return false;
							}
												
							if (event.keyCode != 8) 
							{
								holder.children("li.bit-box.deleted").removeClass("deleted");
							}
							
	                        if (in_array(event.keyCode, options.key_codes) && checkFocusOn()) 
	                        {
	                            var option = focuson;
	                            addItem(option.text(), option.attr("rel"));
	                            complete.hide();
	                            event.preventDefault();
								focuson = null;
								return false;
	                        }
							
							if (in_array(event.keyCode, options.key_codes) && !checkFocusOn()) 
	                        {
								if (options.newel) 
								{
									var value = xssPrevent($(this).val());
									addItem(value, value);
									complete.hide();
									event.preventDefault();
									focuson = null;
								}
								return false;							
	                        }
	                        
	                        if (event.keyCode == 40) 
	                        {               
					            removeFeedEvent();
	                            if (focuson == null || focuson.length == 0) 
	                            {
	                                focuson = feed.children("li:visible:first");
						            feed.get(0).scrollTop = 0;
	                            }
	                            else 
	                            {
	                                focuson.removeClass("auto-focus");
	                                focuson = focuson.nextAll("li:visible:first");
						            var prev = parseInt(focuson.prevAll("li:visible").length,10);
						            var next = parseInt(focuson.nextAll("li:visible").length,10);
						            if ((prev > Math.round(options.height /2) || next <= Math.round(options.height /2)) && typeof(focuson.get(0)) != "undefined") 
						            {
							            feed.get(0).scrollTop = parseInt(focuson.get(0).scrollHeight,10) * (prev - Math.round(options.height /2));
						            }
	                            }
					            feed.children("li").removeClass("auto-focus");
	                            focuson.addClass("auto-focus");
	                        }
	                        if (event.keyCode == 38) 
	                        {
					            removeFeedEvent();
	                            if (focuson == null || focuson.length == 0) 
	                            {
	                                focuson = feed.children("li:visible:last");
						            feed.get(0).scrollTop = parseInt(focuson.get(0).scrollHeight,10) * (parseInt(feed.children("li:visible").length,10) - Math.round(options.height /2));
	                            }
	                            else 
	                            {
	                                focuson.removeClass("auto-focus");
	                                focuson = focuson.prevAll("li:visible:first");
						            var prev = parseInt(focuson.prevAll("li:visible").length,10);
						            var next = parseInt(focuson.nextAll("li:visible").length,10);
						            if ((next > Math.round(options.height /2) || prev <= Math.round(options.height /2)) && typeof(focuson.get(0)) != "undefined") 
						            {
							            feed.get(0).scrollTop = parseInt(focuson.get(0).scrollHeight,10) * (prev - Math.round(options.height /2));
						            }
	                            }
					            feed.children("li").removeClass("auto-focus");
	                            focuson.addClass("auto-focus");
	                        }													
	                    }
	                );
		        }
	        	
		        function addTextItem(value)
		        {					
	                if (options.newel) 
	                {
	                    feed.children("li[fckb=1]").remove();
	                    if (value.length == 0)
	                    {
	                    	return;
	                    }
	                    var li = $(document.createElement("li"));
	                    li.attr({"rel": value,"fckb": "1"}).html(value);
	                    feed.prepend(li);
				        counter++;
	                } else 
					{
						return;
					}
	            }
	        	
				function funCall(func,item)
				{	
					var _object = "";			
					for(i=0;i < item.get(0).attributes.length;i++)
					{	
						if (item.get(0).attributes[i].nodeValue != null) 
						{
							_object += "\"_" + item.get(0).attributes[i].nodeName + "\": \"" + item.get(0).attributes[i].nodeValue + "\",";
						}
					}
					_object = "{"+ _object + " notinuse: 0}";
					try {
						eval(func + "(" + _object + ")");
					}catch(ex){};
				}
				
				function checkFocusOn()
		        {
		            if (focuson == null)
		            {
		                return false;
		            }
		            if (focuson.length == 0)
		            {
		                return false;
		            }
		            return true;
		        }
				
				function xssPrevent(string)
                {					
                    string = string.replace(/[\"\'][\s]*javascript:(.*)[\"\']/g, "\"\"");
                    string = string.replace(/script(.*)/g, "");    
                    string = string.replace(/eval\((.*)\)/g, "");
                    string = string.replace('/([\x00-\x08,\x0b-\x0c,\x0e-\x19])/', '');
                    return string;
                }
                
                function in_array(needle, stack){
					var a=false;
					for(var i=0;i<stack.length;i++){
						if(needle == stack[i]){
							a=true;
							break;
						}
					}
					return a;
				}
                
                function clear()
                {
					var holder = element.data('fcbkcompleteHolder');
					
					holder.find('li.bit-box').each(function() {
						removeItem($(this));
					});
					
					// call blur when done
					holder.find('input.maininput').blur();
					
					
					//done
					return true;
				}
				
				
				//init
				var element = $(this);
		        var elemid = element.attr("id");
		        var options = element.data('fcbkcompleteOptions');
				
				// call functions if provided
				switch (opt) {
					case 'clear':
						return clear($(this));
						break;
				}
				
		        options = $.extend({
					key_codes: [13],
					json_url: null,
					cache: false,
					height: "10",
					newel: false,
					firstselected: false,
					filter_case: false,
					filter_hide: false,
					complete_text: "Start to type...",
					maxshownitems:  30,
					onselect: "",
					onremove: "",
					allow_duplicates: true
				}, opt);
			        
			    element.data('fcbkcompleteOptions', options);
	        	
		        //system variables
		        var container  		= $('<div></div>').addClass('fcbk_container');
		        var holder     		= null;
		        var feed       		= null;
		        var complete   		= null;
		        var counter    		= 0;
		        var cache      		= new Array();
				var json_cache		= false;
				var search_string	= "";
		        var focuson    		= null;
	        	var deleting		= 0;
				var browser_msie	= "\v"=="v";
				var browser_msie_frame;
				
		        init();

		        return this;
			});
	    };
    }
);