import sqlite3, sys
from models import *
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
    reverseOrder = False
    screens = []
    for i, team in enumerate(teams):
        screens.append(Menu("Draft for Team #" + str(i+1), availableAthletes(draftingLeague)))

    while drafting:
        for i, team in enumerate(teams):
            if reverseOrder:
                screen = screens[len(teams)-i-1]
            else:
                screen = screens[i]
            screen.display()
            drafting = screen.get_input()
            if not drafting:
                break
            elif drafting != True:
                pass

        reverseOrder = not reverseOrder
        teams.reverse()

    print "Congratulations! You have successfully completed the draft!"
    
    conn.commit()
    conn.close()

def availableAthletes(league):
    takenAthletes = []
    available = []
    for team in league.get_members():
        for athlete in team.get_athletes():
            takenAthletes.append(athlete.id)
    for athlete in Athlete.getAll():
        if athlete.id not in takenAthletes:
            available.append(athlete)

    return available

class Menu(object):
    def __init__(self, title, items):
        self.title = title
        self.items = items
        self.page = 1

    def display(self):
        print self.title
        for i, item in enumerate(self.items[(self.page-1)*15:self.page*15]):
            print str(i + 15*(self.page-1) + 1) + ". " + str(item)

        print "Page", self.page
            
    def get_input(self):
        print "Choices:"
        if self.page > 1 and self.page < len(self.items)/15:
            options = ["Select Athlete", "Last Page", "Next Page"]
        elif self.page > 1:
            options = ["Select Athlete", "Last Page"]
        elif self.page < len(self.items)/15:
            options = ["Select Athlete", "Next Page"]

        options.append("Quit")

        for i, option in enumerate(options):
            print str(i+1) + ". " + option

        choice = input("?") - 1
        if options[choice] == "Next Page":
            self.page += 1
        elif options[choice] == "Last Page":
            self.page -= 1
        elif options[choice] == "Select Athlete":
            athleteChoice = -1
            while athleteChoice < 0 or athleteChoice >= len(self.items):
                athleteChoice = input("Enter athlete number: ")
            return self.items[athleteChoice]
                
        elif options[choice] == "Quit":
            return False

        return True

    def remove_item(self, item):
        self.items.remove(item)

if __name__ == "__main__":
    main()
    
