import sqlite3, Athlete, sys
sys.path.append("sql/")
from helpers import *

class League(object):
    def __init__(self, name, member_ids = []):
        try:
            self.executeSQL("INSERT INTO league (name) VALUES(" + quotify(name) + ");")
            for id in member_ids:
                self.add_member(id)
        except:
            pass
        
        self.name = name
        self.id = self.executeSQL("SELECT id FROM league WHERE name = " + quotify(name) + ";")[0][0]

    def executeSQL(self, command):
        conn = sqlite3.connect("teams.db")
        c = conn.cursor()

        try:
            ret = c.execute(command).fetchall()
        finally:
            conn.commit()
            conn.close()

        return ret

    def add_member(self, team_id):
        self.executeSQL("UPDATE team set league_id = " + str(self.id) + " WHERE id = " + str(team_id))

    def get_members(self):
        return self.executeSQL("SELECT * FROM team JOIN league WHERE team.league_id = league.id AND league.id = " + str(self.id) + ";")
