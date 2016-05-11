/*---------------------------------------------- 
		F I X E D   H E A D E R   
------------------------------------------------*/
var headeroverlay = false;
var headerheight = jQuery('header').height();
jQuery( document ).ready(function() {
	
	/* BUGFIX for revolutionslider when header shrinks */
	if (jQuery('.header-overlay').length < 1) {
		jQuery('body').append('<div id="pseudo-header"></div>');
		jQuery('#pseudo-header').css({ 'height':headerheight+'px', 'position':'absolute', 'top':0, 'left':0, 'opacity':0 });
		if (jQuery('.fixed-header').length > 0) {
			jQuery('.page-body').css({ 'margin-top':headerheight+'px'});
		}
	} else {
		headeroverlay = true;
	}
	sizeDownHeader();
});

jQuery( window ).scroll(function() {
	sizeDownHeader();
});

jQuery( window ).resize(function() {
	headerheight = jQuery('header').height();
	if (jQuery('.header-overlay').length < 1 && jQuery( window ).width() < 1023 && jQuery('.wasOverlay').length < 1) {
		jQuery('#pseudo-header').css({ 'height':headerheight+'px', 'position':'absolute', 'top':0, 'left':0, 'opacity':0 });
		if (jQuery('.fixed-header').length > 0) {
			jQuery('.page-body').css({ 'margin-top':headerheight+'px'});
		}
	}
	sizeDownHeader();
});

function sizeDownHeader() {
	
	var scrolltop = 150;
	if (headeroverlay) { 
		scrolltop = 500; 
		if (jQuery(document).scrollTop() > jQuery(window).height()-headerheight && jQuery('.fixed-header').length > 0 ) {
			jQuery('#overlay-logo').fadeOut(0);
			jQuery('header').removeClass("header-overlay"); 
			jQuery('header').addClass("wasOverlay"); // Bugfix for chrome on mobile
			if (jQuery('.header-shown').length < 1) { jQuery('header').css({'top':'-'+headerheight+'px'}); jQuery('header').animate({'top':'0px'}, 600, 'easeInOutQuart'); }; jQuery('header').addClass("header-shown");
		} else if (jQuery('.fixed-header').length > 0) {
			
			if (jQuery('.header-shown').length > 0) { jQuery('header').animate({'top':'-'+headerheight+'px'}, 200, function() {
				jQuery('header').addClass("header-overlay");
				jQuery('header').removeClass("wasOverlay"); // Bugfix for chrome on mobile
				jQuery('header').animate({'top':'0px'}, 600, 'easeInOutQuart');
				jQuery('#overlay-logo').fadeIn(0);
			}); }
				jQuery('header').removeClass("header-shown");
		}
	}
	
		if ( jQuery( window ).width() < 767 ) {
			jQuery('.fixed-header nav#main-nav').fadeOut(0);
			jQuery('.fixed-header nav#menu-controls').fadeOut(0);
			jQuery('.fixed-header .open-responsive-nav').fadeIn(500);
		} else {
			
			if (jQuery(document).scrollTop() > scrolltop && jQuery('.fixed-header').length > 0 ) { 
				if (jQuery('.fixed-header header').hasClass( "smallheader" )) {} else {
					if ( jQuery( window ).width() > 1023 ) {
						if (jQuery('header.no-resize').length < 1) { jQuery('.fixed-header header').addClass("smallheader"); }
						jQuery('.fixed-header .open-responsive-nav').fadeOut(0);
						if (jQuery('.fixed-header nav#menu-controls').length > 0) { 
							jQuery('.fixed-header nav#main-nav').fadeOut(200, function(){ jQuery('nav#menu-controls').fadeIn(200); });
						}
					} else if ( jQuery( window ).width() > 767 ) {
						jQuery('.fixed-header nav#main-nav').fadeOut(0);
						if (jQuery('.fixed-header nav#menu-controls').length > 0) { 
							jQuery('.fixed-header .open-responsive-nav').fadeOut(200, function(){ jQuery('nav#menu-controls').fadeIn(200); });
						}
					} 
				}
			} else if (jQuery('.fixed-header').length > 0) {
				if ( jQuery( window ).width() > 1023 ) {
					jQuery('.fixed-header .open-responsive-nav').fadeOut(0);
					if (jQuery('.fixed-header header').hasClass( "smallheader" )) { jQuery('.fixed-header header').removeClass("smallheader"); }
					if (jQuery('.fixed-header nav#menu-controls').length > 0) { 
						jQuery('.fixed-header nav#menu-controls').fadeOut(200, function(){ jQuery('nav#main-nav').fadeIn(200); });
					}
				} else if ( jQuery( window ).width() > 767 ) {
					jQuery('.fixed-header nav#main-nav').fadeOut(0);
					if (jQuery('.fixed-header nav#menu-controls').length > 0) { 
						jQuery('.fixed-header nav#menu-controls').fadeOut(200, function(){ jQuery('.open-responsive-nav').fadeIn(200); });
					}
				}
			}
		}
}