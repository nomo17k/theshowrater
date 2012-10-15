import re
import MySQLdb
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest
from pyramid.url import route_url
from pyramid.view import view_config
from pyramid.events import NewRequest
from pyramid.events import subscriber
from theshowutil.driver import find_teams_in_year, find_players_in_team
from theshowutil.playerdata import PlayerData, NoPlayerFoundError


YEARLIST = range(2011, 1869, -1)


def teamlist(y, db):
    res = find_teams_in_year(y, db)
    res = [(o[0], o[2]) for o in res]
    return sorted(res, key=lambda x: x[1])


def prbt_output(yearID, teamID, db):
    pids = find_players_in_team(yearID, teamID, db)
    outs = []
    if len(pids):
        for i, pid in enumerate(pids):
            try:
                pd = PlayerData(pid, currentyear=yearID, yweight={}, db=db)
            except NoPlayerFoundError:
                outs.append('playerID {:s} not found in database'
                            .format(pid))
            if i == 0:
                outs.append(pd.attr.csvheader)
            outs.append(pd.attr.csv)
    else:
        return None
    return '\n'.join(outs)


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
    return {}


@view_config(renderer="json", name="json.get_teams")
def json_get_teams(s, response):
    y = response.GET.get('yearID')
    if y is None:
        return HTTPBadRequest()
    return teamlist(y, response.db)


@view_config(renderer="json", name="json.update_prbt")
def json_update_prbt(s, response):
    yearID = response.GET.get('yearID')
    teamID = response.GET.get('teamID')
    if yearID is None or teamID is None:
        return HTTPBadRequest()
    out = prbt_output(yearID, teamID, response.db)
    if out is None:
        return HTTPBadRequest()
    return (out,)


@view_config(route_name="prbt", renderer="templates/prbt.pt")
def prbt_view(request):
    return {'output': '', 'years': YEARLIST}
