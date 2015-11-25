import sqlite3, Athlete, sys
sys.path.append("sql/")
from helpers import *

class League(object):
    def __init__(self, name, members = []):
        try:
            self.executeSQL("INSERT INTO league (name) VALUES(" + quotify(name) + ");")
        except:
            print "League already exists. Returning existing league..."

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

    def get_members(self):
        return self.executeSQL("SELECT * FROM team JOIN league WHERE team.league_id = league.id AND league.id = " + str(self.id) + ";")
