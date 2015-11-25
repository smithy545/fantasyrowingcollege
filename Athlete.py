import sqlite3

class Athlete(object):
    def __init__(self, id):
        conn = sqlite3.connect("roster_files/athletes.db")
        c = conn.cursor()

        info = c.execute("SELECT * FROM athlete WHERE id = " + str(id) + ";").fetchall()

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
