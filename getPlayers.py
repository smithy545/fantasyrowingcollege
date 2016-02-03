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

    def getPoints(self):
        points = 0
        for race in self.races:
            order = race.getOrdered()
            index = -1
            for i, team in enumerate(order):
                if team[0] == self.team:
                    index = i
                    break
            i = 0
            while i < index:
                points += 

class PlayerList:
    def __init__(self):
        self.players = []

    def __iter__(self):
        return iter(self.players)

    def getPlayer(self, name):
        for p in self.players:
            if p.name == name:
                return p
        return None

    def addPlayer(self, name, team, races = None):
        self.players.append(Player(name, team, races))
        self.players.sort(key=lambda x:x.name)

def getPlayers(wb, sheets=['Wisconsin',
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
            for row in range(11,20):
                cellval = ws.cell(row=row,column=col).value
                if cellval and not any(cellval == p.name for p in players):
                    players.addPlayer(cellval.strip(), sheet, [race])
                elif cellval:
                    players.getPlayer(cellval.strip()).races.append(race)

    return players
