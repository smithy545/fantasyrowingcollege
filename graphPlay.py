import plotly.plotly as py
import plotly.graph_objs as go
from runTestSeason import getRaces
from elo_files.elo_compare import *
import datetime

races, duals = getRaces()

sheets = ['Wisconsin',
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
          ]

elos = {}
for sheet in sheets:
    elos[sheet] = [(900, datetime.datetime(2015,3,20))]

tdelta = 0
for dual in duals:
    if dual["results"][0][0]:
        res0 = datetime.datetime.combine(datetime.date.today(),dual["results"][0][0])
        res1 = datetime.datetime.combine(datetime.date.today(),dual["results"][1][0])
        team0 = dual["teams"][0]
        team1 = dual["teams"][1]
    if res0 and res1:
        if res0 > res1:
            tdelta = (res0-res1).total_seconds()
            elo0,elo1 = elos[team0][-1][0],elos[team1][-1][0]
            elo1,elo0 = eloCompare(elo1,elo0,tdelta)
            elos[team0].append((elo0,dual["date"]))
            elos[team1].append((elo1,dual["date"]))
            print team1 + u" over " + team0 + u" by " + unicode(tdelta) + u"s"
        else:
            tdelta = (res1-res0).total_seconds()
            elo0,elo1 = elos[team0][-1][0],elos[team1][-1][0]
            elo0,elo1 = eloCompare(elo0,elo1,tdelta)
            elos[team0].append((elo0,dual["date"]))
            elos[team1].append((elo1,dual["date"]))
            print team0 + u" over " + team1 + u" by " + unicode(tdelta) + u"s"

data = []
for team in elos:
    x = [i[1] for i in elos[team]]
    y = [i[0] for i in elos[team]]
    data.append(go.Scatter(x = x, y = y, mode = 'lines',name = team))

    
py.plot(data, filename='scatter-mode')
