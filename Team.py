import sqlite3, sys
sys.path.append("sql/")
from helpers import *

class Team(object):
    def __init__(self, name, league_id):
        self.name = name
        self.league_id = league_id
        self.athletes = []

        self.executeSQL("INSERT INTO team (name, league_id) VALUES(" + quotify(self.name) + ", " + str(league_id) + ");")
        
    def executeSQL(self, command):
        conn = sqlite3.connect("teams.db")
        c = conn.cursor()

        try:
            ret = c.execute(command).fetchall()
        finally:
            conn.commit()
            conn.close()

        return ret
