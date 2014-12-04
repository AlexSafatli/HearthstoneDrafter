// Everything to be executed after page load.

$(document).ready(function () {
  
   // Handle all card hiding.
	$(".cards").hide();
    $(".card").hide();
    $("#draftshow").show();
    $(".hsimg").click(function() {
      // Drafting.
       $("#draftcounter").text(parseInt($("#draftcounter").text())+1);
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

    // Handle card coloring.
    $("#card_collection").children().heatcolor(function(d) {
        return $(this).attr("data-cardcost");
    },{ lightness:0, reverseOrder:true });

});

