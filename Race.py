import operator

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
        return sorted(self.results.items())            
