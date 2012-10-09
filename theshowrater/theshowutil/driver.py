from . import lahmandb


def find_teams_in_year(year, db=lahmandb):
    c = db.cursor()
    sql = "SELECT teamID, lgID, name FROM Teams WHERE yearID = %(year)s"
    c.execute(sql, {'year': year})
    return c.fetchall()


def find_players_in_team(year, team, db=lahmandb):
    params = {'team': str(team), 'year': int(year)}
    pids = []
    sql = ("SELECT playerID FROM Appearances"
           "  WHERE teamID = %(team)s AND yearID = %(year)s"
           "  ORDER BY G_p DESC, G_all DESC")
    c = db.cursor()
    c.execute(sql, params)
    return [o[0] for o in c.fetchall()]
