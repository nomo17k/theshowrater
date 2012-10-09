import re
import MySQLdb
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest
from pyramid.url import route_url
from pyramid.view import view_config
from pyramid.events import NewRequest
from pyramid.events import subscriber
from theshowutil.driver import find_teams_in_year, find_players_in_team
from theshowutil.playerdata import PlayerData


YEARLIST = range(2011, 1869, -1)

def teamlist(y, db):
    res = find_teams_in_year(y, db)
    res = [(o[0], o[2]) for o in res]
    return res
    

@subscriber(NewRequest)
def new_request_subscriber(event):
    request = event.request
    settings = request.registry.settings
    request.db = MySQLdb.connect(**settings['db'])
    request.add_finished_callback(close_db_connection)


def close_db_connection(request):
    request.db.close()


@view_config(route_name="home", renderer="templates/home.pt")
def home_view(request):
    return {'years': YEARLIST}


@view_config(renderer="json", name="update.teams")
def update_teams_view(s, response):
    y = response.GET.get('y')
    if y is None:
        return HTTPBadRequest()
    return teamlist(y, response.db)


@view_config(route_name="prbt", renderer="templates/prbt.pt")
def prbt_view(request):
    d = request.matchdict
    matchobj = re.match(r"^[\w][\w\d][\w\d]$", d['teamID'])
    if matchobj:
        teamID = matchobj.group()
    else:
        return HTTPBadRequest()
    matchobj = re.match(r"^[12][089]\d\d$", d['yearID'])
    if matchobj:
        yearID = matchobj.group()
    else:
        return HTTPBadRequest()

    pids = find_players_in_team(yearID, teamID, db=request.db)
    if len(pids):
        outs = []
        for i, pid in enumerate(pids):
            pd = PlayerData(pid, currentyear=yearID, yweight={}, db=request.db)
            if i == 0:
                outs.append(pd.attr.csvheader)
            outs.append(pd.attr.csv)
        out = '\n'.join(outs)
    else:
        return HTTPBadRequest()

    #teams = [(o[0], o[2]) for o in teamlist(yearID, request.db)]

    return {'output': out, 'yearID': yearID, 'teamName': teamID,
            'years': YEARLIST, 'teamID': teamID}#, 'teams': teams}
