// Everything to be executed after page load. 
var mana;
Chart.defaults.global.scaleFontFamily = 
  "'Franklin Gothic Medium', 'Franklin Gothic', 'ITC Franklin Gothic', Arial, sans-serif";
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
      var cardToShow = $('#' + $(this).attr("id").replace('card_draft_','card_')),
         manaCost = parseInt(cardToShow.attr("data-cardcost")),
         manaCategory;
      if (manaCost >= 7) manaCategory = 7;
      else manaCategory = manaCost;
      mana.datasets[0].bars[manaCategory].value++; mana.update();
      cardToShow.attr("src",$(this).attr("src")).show();
    });

  // Handle card coloring.
  $("#card_collection .card").heatcolor(function(d) {
    return $(this).attr("data-cardcost");
  },{ lightness:0, reverseOrder:true });

  // Tooltips for card hovering.
  $(".hsimg").hover(cardTooltip,function() { $(".tooltip").hide(); })
    .mousemove(cardTooltip);

  // Event handling for popup.
  $("#arenabutton").click(modepopup);
  $(".popup .popupbutton").click(modeselect);
  $(".popup ")
  $(".popup button").click(modedone);

  // Mana curve.
  var canvas = $("#manacurve").get(0).getContext("2d");
  mana = new Chart(canvas).Bar({
    labels:["0","1","2","3","4","5","6","7+"],
    datasets:[{label:"Curve",data:[0,0,0,0,0,0,0,0]}]
  },{});

});

// Card tooltips.

function cardTooltip(e) {


  var mousex = e.pageX + 20, mousey = e.pageY + 20, card = $(this);
  var hp_def = '<div class="cardDef">' + card.attr('data-carddef') + '</div>';
  if (parseInt(card.attr('data-carddef')) == 0 && parseInt(card.attr('data-cardatk')) == 0)
    hp_def = '';
  else if (parseInt(card.attr('data-cardatk')) != 0)
    hp_def += '<div class="cardAttack">' + card.attr('data-cardatk') + '</div>';
  var tooltipText = "<h3>" + card.attr('data-cardname') + "</h3>" + hp_def +
    '<div class="cardCost">' + card.attr('data-cardcost') + '</div>' +
    card.attr('data-cardtext') + '</br></br>' + 
    "<strong>Faction</strong>: " + card.attr('data-cardfaction');
  $(".tooltip").show().html(tooltipText).css({'left':mousex,'top':mousey});

}

// Popup management.

function optionsSelected() {

  var $modeID = $(".pselected").attr("id");
  var $modeOptClass = ".".concat($modeID.concat("_opt"));
  if ($($modeOptClass).length) return $(".poptselected").length;
  return true;

}

function modepopup() {

  $(".popup").show();

} 

function modeselect() {

  if ($(this).hasClass("pmode")) {
    var $modeID = $(this).attr("id");
    var $modeDescID = "#".concat($modeID.concat("_desc"));
    var $modeOptClass = ".".concat($modeID.concat("_opt"));
    $(".poption").hide();
    $(".pdesc").hide();
    $($modeDescID).show();
    $($modeOptClass).show();
    $(".popup .popupbutton").css("background-color","").removeClass("pselected");
    $(this).css("background-color","black").addClass("pselected");
  } else {
    $(".poption").removeClass("poptselected").css("background-color","");
    $(this).addClass("poptselected").css("background-color","black");
    $("#mgopt").attr("value",$(this).attr("id"));
  }

}

function modedone() {

  if ($(".pselected").length && optionsSelected()) {
    $("#arenabutton").html($(".pselected").html());
    $("#mgmode").attr("value",$(".pselected").attr("id"));
    $(".popup").hide();
  } else {
    $("#phelp").html("<em>You must select all required options!</em>");
  }

}