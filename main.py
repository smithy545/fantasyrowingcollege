from openpyxl import Workbook, load_workbook
from Races import getRaces
from Players import getPlayers
from util import *

def main():
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

    wb = load_workbook('data/2015 Spring Season.xlsx')

    races, duals = getRaces(wb)
    players = getPlayers(wb, races, duals)

    # Print out race info and whatnot
    print "\nRaces:"
    for race in races:
        print race.name
        for team, results in race.results.iteritems():
            print team
            if results[0]:
                print results[0].strftime("%M:%S.%f")
        print ""

    # Print out dual info and whatnot
    print "\nDuals"
    for dual in duals:
        print dual.teams[0]+" v "+dual.teams[1]
        for team, res in dual.results.iteritems():
            if res[0]:
                print "V8:",res[0].strftime("%M:%S.%f")
        print ""


    # Generate player rankings and output them to "Player Rankings-generated.xlsx"
    cmax = generateCMAX()

    wbout = Workbook()
    ws1 = wbout.active
    ws1.title = "Player Rankings"

    outplayers = []
    for player in players:
        points = player.getPoints(cmax)
        outplayers.append([player.team, player.name, points, points/len(player.races)])

    for i, p in enumerate(outplayers):
        for j, e in enumerate(p):
            ws1.cell(row = i+1, column=j+1, value=e)
        print p
    wbout.save(filename = "data/Player Rankings-generated.xlsx")


if __name__=="__main__":
    main()

