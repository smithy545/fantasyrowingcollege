from datetime import datetime, date
from util import getAbbr, pointFormula

class Player:
    def __init__(self, name, team, races=None):
        self.name = name
        self.team = team
        if races == None:
            races = []
        self.races = races

    def __str__(self):
        return str(self.name)
    
    def __unicode__(self):
        return unicode(self.name)

    def getPoints(self, cmaxTable):
        points = 0
        for race in self.races:
            if ("IRA" in race.name) or ("EARC" in race.name):
                #print "Skipping",race.name,"..."
                continue
            
            mytime = race.results[self.team][0]
            if mytime == None:
                continue
            c1 = getcmax(self.team, race.date, cmaxTable)
            t1 = datetime.combine(date.today(),mytime)
            for team, res in race.results.iteritems():
                if team != self.team and res[0]:
                    cmaxdelta = c1 - getcmax(team, race.date, cmaxTable)
                    t2 = datetime.combine(date.today(),res[0])
                    if res[0] > mytime:
                        movdelta = t2 - t1
                        points += pointFormula(cmaxdelta, movdelta.total_seconds())[0]
                    else:
                        movdelta = t1 - t2
                        points += pointFormula(cmaxdelta, movdelta.total_seconds())[1]
        self.points = points
        return points

    def getNumCompetitors(self):
        num = 0
        for race in self.races:
            num += len(race.results.keys()) - 1
        return num

    def getSchema(self, cmaxTable):
        out = {}
        for race in self.races:
            raceschema = []
            for team, res in race.results.iteritems():
                if res[0]:
                    raceschema.append({"team":team,"cmax":getcmax(team, race.date, cmaxTable),"time":res[0],"points":1})
            if out.get(race.date.date()):
                out[race.date.date()].append(raceschema)
            else:
                out[race.date.date()] = [raceschema]
        return out
    
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

def getcmax(team, date, cmaxTable):
    team = getAbbr(team)

    colDate = date
    dates = []
    for key in cmaxTable:
        if key != "min" and colDate >= key:
            dates.append(key)

    if len(dates) == 0:
        colDate = cmaxTable["min"]
    else:
        colDate = max(dates)

    for t in cmaxTable[colDate]:
        if team == t[0]:
            return t[1]

    colDate = cmaxTable["min"]
    for t in cmaxTable[colDate]:
        if team == t[0]:
            return t[1]

    raise NameError("Could not find:"+team)

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
            else:
                race = races.getRace(race)
            
            for row in range(11,20):
                cellval = ws.cell(row=row,column=col).value
                if cellval and not any(cellval == p.name for p in players):
                    players.addPlayer(cellval.strip(), sheet, [race])
                elif cellval:
                    players.getPlayer(cellval.strip()).races.append(race)

    return players


