// Everything to be executed after page load.

$(document).ready(function () {
	$(".cards").hide();
    $(".card").hide();
    $("#draftshow").show();
    $(".hsimg").click(function() {
		$(this).parent().next().attr("id","draftshow");
		$(this).parent().attr("id","");
        if ($(this).parent().next().length > 0) {
            $(this).parent().next().show();
        } else {
            $("#draft").hide();
        }
		$(this).parent().hide();
        $('#' + $(this).attr("id").replace('card_draft_','card_')).show();
	});
});

// Everything to be executed after all images, etc.
// have loaded.
/*
$(window).load(function () {

    var $sets = $('.cards');

    // Identify links for layout selection.
    
    var $optionSets = $('#layoutSelect .option-set'),
        $optionLinks = $optionSets.find('a');
    
        
    // Add click handler to layout selection links.

    $optionLinks.click(function(){
      	var $this = $(this);
		setLayout($this);
    });

	function setLayout($this) {
		
		// don't proceed if already selected
        
      	if ( $this.hasClass('selected') ) {
        	return false;
      	}
   
        // otherwise, change selection link and layout

      	var $optionSet = $this.parents('.option-set');
      	$optionSet.find('.selected').removeClass('selected');
      	$this.addClass('selected');
      	var options = {},
        key = $optionSet.attr('data-option-key'),
        value = $this.attr('data-option-value');
      	options[ key ] = value;
      	$container.isotope( options );      
        $.cookie('layout_mode', options[ key ]);
      	return false;
		
	}
	
});*/


