import sqlite3

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

conn.commit()
conn.close()
