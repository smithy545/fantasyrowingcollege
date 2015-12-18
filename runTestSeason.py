from openpyxl import Workbook, load_workbook
from types import *
import datetime

wb = load_workbook('testseason.xlsx')
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

def getTime(t):
    if type(d) == UnicodeType:
        try:
            return datetime.datetime.strptime(d[3:],'%M:%S.%f').time()
        except:
            return t
    else:
        return t

def getDate(d):
    try:
        return d.date()
    except:
        return d


races = {}
rs = wb["Races"]
for r in range(2,24):
    name = rs.cell(row=r, column=1).value
    date = rs.cell(row=r, column=3).value
    races[name] = {"teams":[],
                   "date":date,
                   "results":{"1V8":[],"2V8":[],"3V8":[],"4V8":[],"5V8":[],"1F8":[],"1V4":[]}
                   }
duals = []

for sheet in sheets:
    ws = wb[sheet]
    print sheet
    for col in range(3,21):
        for row in range(1,9):
            d = ws.cell(row=row, column=col).value
            if d:
                date = ""
                if row == 1:
                    date = getDate(d)
                elif row == 2:
                    if d.startswith("v "):
                        versus = d[2:]
                        results = []
                        duals.append({"sheet":sheet,
                                      "teams":versus,
                                      "date":date,
                                      "results":results})
                    else:
                        races[d]["teams"].append(sheet)
                        #races[d]["results"].append(0)
                            

print "\nRaces:"
for race in races:
    if len(races[race]["teams"]) < 5:
        print race, races[race]["teams"]
'''
for dual in duals:
    print dual
'''
