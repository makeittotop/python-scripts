/*-----------------------------------------------------------------------------------

 	Script - Form Validation and Ajax Comments
 
-----------------------------------------------------------------------------------*/


jQuery(window).load(function($) {	
	
	
	/*---------------------------------------------- 
				  F O R M   V A L I D A T I O N 
	------------------------------------------------*/
		
	jQuery("body").on("click", 'input[type="submit"]', function() {
				
		$form = jQuery(this).parents('form');
		form_action = $form.attr('target');
		form_class = $form.attr('class');
		id = $form.attr('id');
		
		if (form_class == 'checkform') {
			
			var control = true;
			
			$form.find('label.req').each(function(index){
											  
				var name = jQuery(this).attr('for');
				defaultvalue = jQuery(this).html();
				value = $form.find('.'+name).val();
				formtype = $form.find('.'+name).attr('type');
				
				
				if (formtype == 'radio' || formtype == 'checkbox') {
					if (jQuery('.'+name+':checked').length == 0) { jQuery(this).siblings('div').find('.checkfalse').fadeIn(200); control = false;  } 
					else { jQuery(this).siblings('div').find('.checkfalse').fadeOut(200); }
				
				} else if(name == 'email') {
					var re = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/;
					if (!value.match(re)) { 
							$form.find('.'+name).addClass('false'); control = false; 
						} else { 
							$form.find('.'+name).removeClass('false'); 
						}
				} else {
					if (  value == '' || 
						  value == defaultvalue
						  ) 
						{ 
							$form.find('.'+name).addClass('false'); control = false; 
	
						} else { 
							$form.find('.'+name).removeClass('false');
						}
				}
				
			});
			
			
			if (!control) { 
				jQuery("#form-note").fadeIn(200);
				return false; 
			
			} else {
				jQuery("#form-note").fadeOut(200);
				
				if (form_action && form_action !== '') {
					var str = $form.serialize();
					
					   jQuery.ajax({
					   type: "POST",
					   url: form_action,
					   data: str,
					   success: function(msg){
						jQuery("#form-note").html(msg);
						jQuery("#form-note").delay(200).fadeIn(200);
					   }
				});
				return false;
				} else {
				return true;
				}
				
			} // END else {
		
		}
	});
	
	
});  // END jQuery(window).load(function($) {


