import sqlite3, sys
sys.path.append("sql/")
from helpers import *

conn = sqlite3.connect("teams.db")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS league (
                id INTEGER PRIMARY KEY,
                name text UNIQUE
                );'''
          )

c.execute('''CREATE TABLE IF NOT EXISTS team (
                id INTEGER PRIMARY KEY,
                name text,
                league_id INTEGER,
                FOREIGN KEY(league_id) REFERENCES league(id));'''
          )

c.execute('''CREATE TABLE IF NOT EXISTS team_athlete (
                team_id INTEGER,
                athlete_id INTEGER,
                FOREIGN KEY(athlete_id) REFERENCES athlete(id),
                FOREIGN KEY(team_id) REFERENCES team(id));'''
          )

c.execute('''CREATE TABLE IF NOT EXISTS athlete (
                id INTEGER PRIMARY KEY,
                first_name text,
                last_name text,
                height real,
                weight integer,
                hometown text,
                high_school text,
                team text,
                year text,
                age integer,
                major text,
                side text)''')

conn2 = sqlite3.connect("roster_files/athletes.db")
c2 = conn2.cursor()

try:
    for athlete in c2.execute("SELECT * FROM athlete;").fetchall():
        athlete = [quotify(x) for x in athlete]
        c.execute(u"INSERT INTO athlete VALUES(" + u','.join(athlete) + u");")
    conn.commit()
finally:
    conn.close()
    conn2.close()
