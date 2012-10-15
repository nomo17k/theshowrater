$(function() {

var update_team_list = function(yearID, teamID_target, teamID_current)
{
  if (yearID.match(/^\d{4}$/)) {
    $.getJSON('/json.get_teams?yearID=' + yearID,
              function(data) {
                var t = $(teamID_target);
                t.empty();
                t.append("<option>Select team</option>");
                $.each(data,
                       function(key, val) {
                         var teamID = val[0];
                         var teamname = val[1];
                         t.append('<option value="'+ teamID +'">'
                                  + teamname + '</option>');
                         
                       });
                t.val(teamID_current).attr("selected", true);
                t.removeAttr('disabled');
              });
  }
  else {
    $(teamID_target)
      .attr('disabled', 'disabled')
      .empty()
      .append("<option>Select team</option>");
    return;  
  }
};


var get_prbt_update = function()
{
  var target = $('#displayfield pre');
  target.empty();
  target.append("<img src='/static/ajax-loader.gif' />");

  var yearID = $("#yearID").val();
  var teamID = $("#teamID").val();

  $.getJSON('/json.update_prbt?yearID='+yearID+'&teamID='+teamID,
            function(data)
            {
              $.each(data,
                     function(key, val)
                     {
                       target.empty();
                       target.append(val);
                     });
            });
};

    
$("#yearID")
      .change(function()
              {
                var yearID = $("#yearID").val();
                update_team_list(yearID, $("#teamID"));
              });

$("#teamID")
      .change(function() { get_prbt_update(); });

});
