import sqlite3, sys
from League import League
from Team import Team
from Athlete import Athlete
sys.path.append("sql/")
from helpers import *


def main():
    conn = sqlite3.connect("teams.db")
    c = conn.cursor()

    league_name = False
    
    while not league_name:
        league_name = raw_input("Enter the name of your league: ")
        if c.execute("SELECT * FROM league WHERE name = " + quotify(league_name) + ";").fetchall():
            draftingLeague = League(league_name)
        else:
            print "League " + league_name + " does not exist..."
            league_name = False

    teamIDs = c.execute("SELECT team.id FROM team JOIN league \
                        WHERE team.league_id = league.id AND \
                        league.id = " + str(draftingLeague.id) + ";").fetchall()
    teams = []
    
    for id in teamIDs:
        teams.append(c.execute("SELECT * FROM team WHERE team.id = " + str(id[0]) + ";").fetchone())

    raw_input("Press enter to start draft...")

    drafting = True
    
    while drafting:
        for team in teams:
            screen = Menu(availableAthletes(draftingLeague))
            screen.display()
            screen.input()
            
        team.reverse()

    print "Congratulations! You have successfully completed the draft!"
    
    conn.commit()
    conn.close()

def availableAthletes(league):
    return False

if __name__ == "__main__":
    main()
    
