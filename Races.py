import operator

class Race:
    def __init__(self, name, date, teams=None, results=None):
        self.name = name
        self.date = date
        if results is None:
            results = {}
        self.results = results
        if teams is None:
            teams = []
        self.teams = teams

    def getDatestring(self):
        return self.date.strftime("%Y-%m-%d")

    def getRacestring(self, result):
        return result.strftime("%M:%S.%f")

    def addResult(self, team, result):
        self.results[team] = result

    def addTeam(self, team):
        self.teams.append(team)

    def getWinner(self):
        fastest = None
        for team, res in self.results.iteritems():
            if fastest == None or fastest[1] > res[0]:
                fastest = [team, res[0]]

        return fastest[0]

    def getOrdered(self):
        raise Exception("I'm too lazy to code a sorting algorithm")

class RaceList:
    def __init__(self, races=None):
        if races is None:
            races = []
        self.races = []

    def __iter__(self):
        return iter(self.races)

    def __str__(self):
        out = ""
        for race in self.races:
            out += race.name+"\n"
        return out

    def __getitem__(self,index):
        return self.races[index]

    def addRace(self, race):
        self.races.append(race)
        self.races.sort(key=lambda x:x.getDatestring())

    def getRace(self, racename):
        for race in self.races:
            if race.name == racename:
                return race

    def addTeamTo(self, racename, team):
        for race in self.races:
            if race.name == racename:
                race.addTeam(team)

    def addResultTo(self, racename, team, results):
        for race in self.races:
            if race.name == racename:
                race.addResult(team, results)            

def getRaces(wb, sheets = ['Wisconsin',
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
    races = RaceList()
    duals = RaceList()
    rs = wb["Races"]
    for r in range(2,23):
        if r:
            name = rs.cell(row=r, column=1).value
            date = rs.cell(row=r, column=3).value
            races.addRace(Race(name, date))

    for sheet in sheets:
        ws = wb[sheet]
        for col in range(3,21):
            race = ws.cell(row=2, column=col).value
            if not race:
                continue
            date = ws.cell(row=1, column=col).value
            res = []
            for i in range(3,10):
                res.append(ws.cell(row=i, column=col).value)
            if race.startswith("v "):
                notexists = True
                for dual in duals:
                    if sheet in dual.teams and race[2:] in dual.teams and date == dual.date:
                        dual.addResult(sheet, res)
                        notexists = False
                if notexists:
                    duals.addRace(Race(sheet+" v "+race[2:],date,teams=[sheet, race[2:]],results={sheet:res}))
            else:
                races.addTeamTo(race, sheet)
                races.addResultTo(race, sheet, res)


    return (races, duals)
