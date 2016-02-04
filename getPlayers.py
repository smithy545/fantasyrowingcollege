from datetime import datetime, date
from calcPoints import *

class Player:
    def __init__(self, name, team, races=None):
        self.name = name
        self.team = team
        if races == None:
            races = []
        self.races = races

    def __str__(self):
        return str(player.name)
    
    def __unicode__(self):
        return unicode(player.name)

    def getPoints(self, cmaxTable):
        points = 0
        for race in self.races:
            mytime = race.results[self.team][0]
            if mytime == None:
                continue
            for team, res in race.results.iteritems():
                if team != self.team and res[0]:
                    #print race.name, team, race.date
                    c1 = getcmax(self.team, race.date, cmaxTable)
                    c2 = getcmax(team, race.date, cmaxTable)
                    t1 = datetime.combine(date.today(),mytime)
                    t2 = datetime.combine(date.today(),res[0])
                    if res[0] > mytime:
                        cmaxdelta = c2 - c1
                        movdelta = t2 - t1
                        points += pointFormula(cmaxdelta, movdelta.total_seconds())[0]
                    else:
                        cmaxdelta = c1 - c2
                        movdelta = t1 - t2
                        points += pointFormula(cmaxdelta, movdelta.total_seconds())[1]
        self.points = points
        return points
    
    def getPointsDetailed(self, cmaxTable):
        points = 0
        for race in self.races:
            print race.name, race.teams
            mytime = race.results[self.team][0]
            if mytime == None:
                continue
            for team, res in race.results.iteritems():
                if team != self.team and res[0]:
                    c1 = getcmax(self.team, race.date, cmaxTable)
                    c2 = getcmax(team, race.date, cmaxTable)
                    t1 = datetime.combine(date.today(),mytime)
                    t2 = datetime.combine(date.today(),res[0])
                    if res[0] > mytime:
                        cmaxdelta = c2 - c1
                        movdelta = t2 - t1
                        print "cmax,mov ",cmaxdelta,movdelta,pointFormula(cmaxdelta, movdelta.total_seconds())
                        points += pointFormula(cmaxdelta, movdelta.total_seconds())[0]
                    else:
                        cmaxdelta = c1 - c2
                        movdelta = t1 - t2
                        print "cmax,mov ",cmaxdelta,movdelta,pointFormula(cmaxdelta, movdelta.total_seconds())
                        points += pointFormula(cmaxdelta, movdelta.total_seconds())[1]
        self.points = points
        return points

class PlayerList:
    def __init__(self):
        self.players = []

    def __iter__(self):
        return iter(self.players)

    def __len__(self):
        return len(self.players)

    def getPlayer(self, name):
        for p in self.players:
            if p.name == name:
                return p
        return None

    def addPlayer(self, name, team, races = None):
        self.players.append(Player(name, team, races))
        self.players.sort(key=lambda x:x.name)

def getPlayers(wb, races, duals, sheets=['Wisconsin',
                          'Brown',
                          'Washington',
                          'Stanford',
                          'Pennsylvania',
                          'Princeton',
                          'BU',
                          'Navy',
                          'Columbia',
                          'California',
                          'Dartmouth',
                          'Holy Cross',
                          'Harvard',
                          'FIT',
                          'Northeastern',
                          'Cornell',
                          'G Washington',
                          'Santa Clara',
                          'OK City',
                          'Oregon State',
                          'Syracuse',
                          'Drexel',
                          'Yale',
                          'Hobart'
                          ]):
    players = PlayerList()

    for sheet in sheets:
        ws = wb[sheet]
        for col in range(3,21):
            race = ws.cell(row=2,column=col).value
            if not race:
                continue
            date = ws.cell(row=1, column=col).value
            if race.startswith("v "):
                for r in duals:
                    if date == r.date and sheet in r.teams and race[2:] in r.teams:
                        race = r
                        break
            elif not race.startswith("IRA"):
                race = races.getRace(race)
            else:
                continue
            
            for row in range(11,20):
                cellval = ws.cell(row=row,column=col).value
                if cellval and not any(cellval == p.name for p in players):
                    players.addPlayer(cellval.strip(), sheet, [race])
                elif cellval:
                    players.getPlayer(cellval.strip()).races.append(race)

    return players
