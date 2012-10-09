

$(document).ready(function() {

    function get_teams() {

      var y = $("#yearID").val();
if (y == "Select year") {

$("#teamID").empty().append("<option>Select team</option>").attr('disabled', 'disabled');
return;  
}

        $.getJSON('/update.teams?y='+ y, function(data) {
            var target = $('#teamID');
            target.empty();
            target.append("<option>Select team</option>");
            $.each(data, function(key, val) {
               var teamID = val[0];
               var teamname = val[1];
               target.append('<option value="'+teamID+'">' + teamname + '</option>');

            });
            target.removeAttr('disabled');

            target.change(function() {
                            var teamID = $(this).val();
                            url = "/prbt/"+y+"/"+teamID;
window.location = url;
                          });

    });
  };


  $("#yearID").change(function() {
                 get_teams();
               });

  $('#teamID').attr('disabled', 'disabled');


alert("here");

                    
});


