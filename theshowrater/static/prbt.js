$(function()
{

  function get_teams(current_team)
  {
    var yearID = $("#yearID").val();
    if (yearID == "Select year") {
      $("#teamID")
        .empty()
        .append("<option>Select team</option>");
      return;  
    }

    $.getJSON('/update.teams?y='+ yearID,
      function(data) {
        var target = $('#teamID');
        target.empty();
        target.append("<option>Select team</option>");
        $.each(data,
           function(key, val) {
             var teamID = val[0];
             var teamname = val[1];
             target.append('<option value="'+teamID+'">'
                           + teamname + '</option>');
             
           });
        target.val(current_team).attr("selected", true);
      });
  };


  function get_prbt_update()
  {
    var target = $('#displayfield pre');
    target.empty();
    target.append("<img src='/static/ajax-loader.gif' />");

    var yearID = $("#yearID").val();
    var teamID = $("#teamID").val();

    $.getJSON('/updates.prbt.json?yearID='+yearID+'&teamID='+teamID,
      function(data)
      {
        $.each(data,
          function(key, val)
          {
            target.empty();
            target.append(val);
          });
      });
  }

  // pre-select the form if a team is loaded.
  if ($("input[name=yearIDcurrent]").length) {
    var ycurrent = $("input[name=yearIDcurrent]").val();
    $("#yearID").val(ycurrent).attr("selected", true);
    var tcurrent = $("input[name=teamIDcurrent]").val();
    get_teams(tcurrent);
  }

  // attach events.
  $("#yearID").change(function() { get_teams(); });
  $("#teamID").change(function() { get_prbt_update(); });

});
