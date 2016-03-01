# A basic command line implementation of a drafting system

import sqlite3, sys, os
from models import *
from types import *
sys.path.append("sql/")
from helpers import *


def main():
    conn = sqlite3.connect("teams.db")
    c = conn.cursor()

    league_name = False

    
    while not league_name:
        for i, league in enumerate(c.execute("SELECT name FROM league;").fetchall()):
            print str(i+1) + ". " + league[0]
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

    for team_id in teamIDs:
        teams.append(Team(id = team_id[0]))

    screen = Menu("Available Athletes:", availableAthletes(draftingLeague))
    drafting = True
    turn = 1
    while drafting and turn <= 24:
        for i, team in enumerate(teams):
            os.system("cls")
            print "Turn #" + str(turn)
            print str(team) + "'s Turn"
            while drafting == True:
                screen.display()
                drafting = screen.get_input()
                
            if drafting:
                team.add_athlete(drafting.id)
                drafting = True
            else:
                break
        turn += 1
        teams.reverse()

    print "Congratulations! You have successfully completed the draft!"
    
    conn.commit()
    conn.close()

def availableAthletes(league):
    takenAthletes = []
    available = []
    for team in league.get_members():
        for athlete in team.get_athletes():
            takenAthletes.append(athlete)
    for athlete in Athlete.getAll():
        if athlete.id not in takenAthletes:
            available.append(athlete)

    return available

class Menu(object):
    def __init__(self, title, items, items_per_page = 15):
        self.title = title
        self.items = items
        self.page = 1
        self.ipp = items_per_page

    def display(self):
        print self.title
        for i, item in enumerate(self.items[(self.page-1)*self.ipp:self.page*self.ipp]):
            print unicode(i + self.ipp*(self.page-1) + 1) + u". " + unicode(item)

        print "Page", self.page
            
    def get_input(self):
        print "Choices:"
        if self.page > 1 and self.page <= len(self.items)/self.ipp:
            options = ["Next Page", "Last Page", "View Athlete", "Select Athlete", ]
        elif self.page > 1:
            options = ["Last Page", "View Athlete", "Select Athlete"]
        elif self.page < len(self.items)/15:
            options = ["Next Page", "View Athlete", "Select Athlete"]

        options.append("Quit")

        for i, option in enumerate(options):
            print str(i+1) + ". " + option

        choice = -1
        while choice < 0 or choice >= len(options):
            try:
                choice = input("?") - 1
            except:
                print "Invalid Input"
        
        if options[choice] == "Next Page":
            self.page += 1
        elif options[choice] == "Last Page":
            self.page -= 1
        elif options[choice] == "View Athlete":
            athleteChoice = -1
            while athleteChoice <= 0 or athleteChoice >= len(self.items):
                try:
                    athleteChoice = input("Enter athlete number: ")
                except:
                    print "Invalid Input"
            temp = self.items[athleteChoice-1].getInfo()
            print temp[1], temp[2]
            print "University:", temp[7]
            if temp[3]:
                print "Height(in): ", temp[3]
            if temp[4]:
                print "Weight(lbs): ", temp[4]
            if temp[5]:
                print "Hometown: ", temp[5]
            raw_input("Press enter to return...")
            
        elif options[choice] == "Select Athlete":
            self.page = 1
            athleteChoice = -1
            while athleteChoice <= 0 or athleteChoice >= len(self.items):
                try:
                    athleteChoice = input("Enter athlete number: ")
                except:
                    print "Invalid Input"
            temp = self.items[athleteChoice-1]
            del self.items[athleteChoice-1]
            return temp
        elif options[choice] == "Quit":
            return False

        return True

    def remove_item(self, item):
        self.items.remove(item)

if __name__ == "__main__":
    main()
    
