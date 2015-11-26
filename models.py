import sqlite3, sys
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
        
    def __str__(self):
        return self.name

    def __unicode__(self):
        return unicode(self.name)

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
        return [Team(id=x[0]) for x in self.executeSQL("SELECT team.id FROM team JOIN league WHERE team.league_id = league.id AND league.id = " + str(self.id) + ";")]

class Team(object):
    def __init__(self, name = None, league_id = None, id = -1):
        if id == -1 and name and league_id:
            self.executeSQL("INSERT INTO team (name, league_id) VALUES(" + quotify(name) + ", " + quotify(league_id) + ");")
            self.id = int(self.executeSQL("SELECT id FROM team WHERE team.name = " + quotify(name) + " AND team.league_id = " + quotify(league_id) + ";")[0][0])
            self.name = name
            self.league_id = league_id
        elif id >= 0:
            temp = self.executeSQL("SELECT * FROM team WHERE team.id = " + str(id) + ";")[0]
            self.id = id
            self.name = str(temp[1])
            self.league_id = temp[2]
        else:
            raise ValueError()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return unicode(self.name)
    
    def executeSQL(self, command):
        conn = sqlite3.connect("teams.db")
        c = conn.cursor()

        try:
            ret = c.execute(command).fetchall()
        finally:
            conn.commit()
            conn.close()

        return ret

    def add_athlete(self, athlete_id):
        self.executeSQL("INSERT INTO team_athlete VALUES(" + str(self.id) + "," + str(athlete_id) + ");")

    def get_athletes(self):
        return [x[0] for x in self.executeSQL("SELECT team_athlete.athlete_id FROM team JOIN team_athlete WHERE team.id = team_athlete.team_id;")]

    @staticmethod
    def getAll():
        conn = sqlite3.connect("teams.db")
        c = conn.cursor()

        teams = []

        for team in c.execute("SELECT id FROM team;").fetchall():
            teams.append(Team(id = team[0]))

        return teams

class Athlete(object):
    def __init__(self, id):
        conn = sqlite3.connect("teams.db")
        c = conn.cursor()

        info = c.execute("SELECT * FROM athlete WHERE id = " + str(id) + ";").fetchone()

        self.id = id
        self.first_name = info[1]
        self.last_name = info[2]
        self.height = info[3]
        self.weight = info[4]
        self.hometown = info[5]
        self.high_school = info[6]
        self.school = info[7]
        self.year = info[8]
        self.age = info[9]
        self.major = info[10]
        self.side = info[11]

        conn.close()

    def __str__(self):
        return self.first_name + " " + self.last_name

    def __unicode__(self):
        return unicode(self.first_name) + u" " + unicode(self.last_name)

    @staticmethod
    def getAll():
        conn = sqlite3.connect("teams.db")
        c = conn.cursor()

        athletes = []

        for athlete in c.execute("SELECT id FROM athlete;").fetchall():
            athletes.append(Athlete(athlete[0]))

        return athletes
