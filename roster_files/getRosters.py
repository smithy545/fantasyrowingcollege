# Scrapes all the athletes from the rosters of 24 ira schools

from bs4 import BeautifulSoup
from types import *
import os, re, sqlite3

def yearShortToLong(year):
    longName = {"FR":"Freshman","SO":"Sophomore","JR":"Junior","SR":"Senior",
                "1Fr.":"Freshman","3So.":"Sophomore","4RSo.":"Sophomore","5Jr.":"Junior","7Sr.":"Senior",
                "Fr.":"Freshman","So.":"Sophomore","Jr.":"Junior","Sr.":"Senior",
                "2019":"Freshman","2018":"Sophomore","2017":"Junior","2016":"Senior"
                }
    return longName.get(str(year))

def toInches(feetin):
    if re.match(r'(\d-\d)+|(\d\'\d")+|(\d\'\d)+', feetin):
        return unicode(12*int(feetin.split("-")[0]) + int(feetin.split("-")[1]))
    return feetin

def getParentheses(s):
    if len(s.split("(")) == 1:
        return [s.split("(")[0].strip(), ""]
    return [s.split("(")[0].strip(), s.split("(")[1].strip()[0:-1].strip()]

def getSlash(s):
    if len(s.split("/")) == 1:
        return [s.split("/")[0].strip(), ""]
    return [s.split("/")[0].strip(), s.split("/")[1].strip()]

def Brown(soup):
    return soup.find("div", "roster").table.tbody

def BrownSanitize(data):
    info = {}
    info["link"] = data[0]
    info["first_name"] = data[1].split(" ")[0]
    info["last_name"] = data[1].split(" ")[1]
    info["year"] = data[2]
    info["hometown"] = data[3].split("/")[0].strip()
    info["high_school"] = data[3].split("/")[1].strip()
    return info

def BU(soup):
    return soup.find("table", id="sortable_roster").tbody

def BUSanitize(data):
    info = {}
    info["link"] = data[1]
    info["first_name"] = data[0].split(" ")[1].title()
    info["last_name"] = data[0].split(" ")[0].title()
    info["year"] = yearShortToLong(data[4])
    info["hometown"] = data[8]
    info["high_school"] = data[9]
    info["height"] = toInches(data[6])
    info["weight"] = data[7]
    return info

def California(soup):
    return soup.find("table", id="roster-list-table").tbody

def CaliforniaSanitize(data):
    info = {}
    info["link"] = data[1]
    info["first_name"] = data[2][:len(data[2])/2].split(" ")[1]
    info["last_name"] = data[2].split(" ")[0]
    info["year"] = yearShortToLong(data[4])
    info["hometown"] = getParentheses(data[5])[0]
    info["height"] = toInches(data[3])
    return info

def Columbia(soup):
    return soup.find("table", id="roster-table").tbody

def ColumbiaSanitize(data):
    info = {}
    i = 0
    if data[0].startswith("http://"):
        info["link"] = data[0]
        i = 1
    info["first_name"] = data[i][:len(data[i])/2].split(" ")[1]
    info["last_name"] = data[i].split(" ")[0]
    info["year"] = yearShortToLong(data[i + 3])
    info["hometown"] = getParentheses(data[i + 4])[0]
    info["height"] = toInches(data[i + 2])
    return info

def Cornell(soup):
    return soup.find("table", id="ctl00_cplhMainContent_dgrdRoster").tbody

def CornellSanitize(data):
    info = {}
    info["link"] = data[1]
    info["first_name"] = data[2].split(" ")[0]
    info["last_name"] = data[2].split(" ")[1]
    info["year"] = yearShortToLong(data[3])
    info["hometown"] = data[4]
    return info

def Dartmouth(soup):
    return soup.find("table", id="roster-table").tbody

def DartmouthSanitize(data):
    info = {}
    i = 0
    if data[0].startswith("http://"):
        info["link"] = data[0]
        i = 1
    info["first_name"] = data[i][:len(data[i])/2].split(" ")[1]
    info["last_name"] = data[i].split(" ")[0]
    info["year"] = yearShortToLong(data[i + 2])
    info["hometown"] = getParentheses(data[i + 3])[0]
    return info

def Drexel(soup):
    return soup.find("table", id="ctl00_cplhMainContent_dgrdRoster").tbody

def DrexelSanitize(data):
    info = {}
    info["link"] = data[0]
    info["first_name"] = data[1].split(" ")[0]
    info["last_name"] = data[1].split(" ")[1]
    info["year"] = yearShortToLong(data[2])
    info["hometown"] = data[4]
    info["high_school"] = data[5]
    info["height"] = toInches(data[3])
    return info

def FIT(soup):
    return soup.find("table", "table table-condensed table-striped roster").tbody

def FITSanitize(data):
    info = {}
    info["link"] = data[0]
    info["first_name"] = data[1].split(" ")[0]
    info["last_name"] = data[1].split(" ")[1]
    info["year"] = yearShortToLong(data[4])
    info["hometown"] = data[5]
    info["high_school"] = data[6]
    info["height"] = toInches(data[2])
    info["weight"] = data[3]
    return info

def GW(soup):
    return soup.find("table", id="sortable_roster").tbody

def GWSanitize(data):
    info = {}
    info["link"] = data[1]
    info["first_name"] = data[2].split(" ")[0]
    info["last_name"] = data[2].split(" ")[1]
    info["year"] = yearShortToLong(data[4])
    info["hometown"] = getSlash(data[7])[0]
    info["high_school"] = getSlash(data[7])[1]
    info["height"] = data[5]
    return info

def Harvard(soup):
    return soup.find("div", "roster").table.tbody

def HarvardSanitize(data):
    info = {}
    info["link"] = data[0]
    info["first_name"] = data[1].split(" ")[0]
    info["last_name"] = data[1].split(" ")[1]
    info["year"] = data[2]
    info["hometown"] = data[3]
    info["high_school"] = data[4]
    return info

def Hobart(soup):
    return soup.find("table", id="ctl00_cplhMainContent_dgrdRoster").tbody

def HobartSanitize(data):
    info = {}
    info["link"] = data[2]
    info["first_name"] = data[3].split(" ")[0]
    info["last_name"] = data[3].split(" ")[1]
    info["year"] = yearShortToLong(data[4])
    info["hometown"] = data[7]
    info["high_school"] = data[8]
    info["height"] = toInches(data[5])
    info["weight"] = data[6]
    return info

def HolyCross(soup):
    return soup.find("table", id="roster-table").tbody

def HolyCrossSanitize(data):
    info = {}
    info["link"] = data[0]
    info["first_name"] = data[1][:len(data[1])/2].split(" ")[1]
    info["last_name"] = data[1].split(" ")[0]
    info["year"] = yearShortToLong(data[4])
    info["hometown"] = getParentheses(data[5])[0]
    info["high_school"] = getParentheses(data[5])[1]
    info["height"] = toInches(data[2])
    info["weight"] = data[3]
    return info

def Navy(soup):
    return soup.find("table", id="sortable_roster").tbody

def NavySanitize(data):
    info = {}
    info["link"] = data[1]
    info["first_name"] = data[2].split(" ")[0]
    info["last_name"] = data[2].split(" ")[1]
    info["year"] = yearShortToLong(data[4])
    info["hometown"] = getSlash(data[7])[0]
    info["high_school"] = getSlash(data[7])[1]
    info["height"] = data[5]
    info["weight"] = data[6]
    return info

def Northeastern(soup):
    return soup.find("table", id="ctl00_cplhMainContent_dgrdRoster").tbody

def NortheasternSanitize(data):
    info = {}
    info["link"] = data[1]
    info["first_name"] = data[2].split(" ")[0]
    info["last_name"] = data[2].split(" ")[1]
    info["year"] = yearShortToLong(data[2])
    info["hometown"] = data[5]
    info["high_school"] = data[6]
    info["height"] = toInches(data[3])
    info["weight"] = data[4]
    info["major"] = data[8]
    return info

def OKCity(soup):
    return soup.find("table", id="ctl00_cplhMainContent_dgrdRoster_M").tbody

def OKCitySanitize(data):
    info = {}
    info["link"] = data[1]
    info["first_name"] = data[2].split(" ")[0]
    info["last_name"] = data[2].split(" ")[1]
    info["year"] = yearShortToLong(data[5])
    info["hometown"] = getSlash(data[6])[0]
    info["high_school"] = getSlash(data[6])[1]
    info["height"] = data[3]
    info["weight"] = data[4]
    return info

def OregonState(soup):
    return soup.find("table", id="roster-list-table").tbody

def OregonStateSanitize(data):
    info = {}
    i = 0
    if data[0].startswith("http://"):
        info["link"] = data[0]
        i = 1
    info["first_name"] = data[i][:len(data[i])/2].split(" ")[1]
    info["last_name"] = data[i].split(" ")[0]
    info["height"] = toInches(data[i+2])
    info["year"] = yearShortToLong(data[i + 3])
    info["hometown"] = getParentheses(data[i+4])[0]
    info["high_school"] = getParentheses(data[i+4])[1]
    return info

def Pennsylvania(soup):
    return soup.find("div", {"class":"whiteAreaBox"}).table.tbody.findAll("tbody")[1].findAll("tr")[4:]

def PennsylvaniaSanitize(data):
    info = {}
    i = 0
    if data[0].startswith("http://"):
        info["link"] = data[0]
        i = 1
    info["first_name"] = data[i].split(" ")[0]
    info["last_name"] = data[i].split(" ")[1]
    info["height"] = toInches(data[i+1])
    info["year"] = yearShortToLong(data[i+2])
    info["hometown"] = getParentheses(data[i+3])[0]
    info["high_school"] = getParentheses(data[i+3])[1]
    return info

def Princeton(soup):
    return soup.find("table", id="roster-table").tbody

def PrincetonSanitize(data):
    info = {}
    info["link"] = data[0]
    info["first_name"] = data[1][:len(data[1])/2].split(" ")[1]
    info["last_name"] = data[1].split(" ")[0]
    info["year"] = yearShortToLong(data[2])
    info["hometown"] = getParentheses(data[3])[0]
    info["high_school"] = getParentheses(data[3])[1]
    return info

def SantaClara(soup):
    return soup.find("div", "roster").table.tbody

def SantaClaraSanitize(data):
    info = {}
    info["link"] = data[0]
    info["first_name"] = data[1].split(" ")[0]
    info["last_name"] = u" ".join(data[1].split(" ")[1:])
    info["year"] = yearShortToLong(data[3])
    info["hometown"] = data[4]
    info["side"] = data[2]
    return info

def Stanford(soup):
    return soup.find("table", id="roster-table").tbody

def StanfordSanitize(data):
    info = {}
    info["link"] = data[0]
    info["first_name"] = data[1].split(",")[1].strip()
    info["last_name"] = data[1].split(",")[1].strip()
    info["year"] = yearShortToLong(data[4])
    info["hometown"] = getParentheses(data[6])[0]
    info["high_school"] = getParentheses(data[6])[1]
    info["height"] = toInches(data[3])
    info["side"] = data[2]
    return info

def Syracuse(soup):
    return soup.find("table", id="ctl00_cplhMainContent_dgrdRoster").tbody

def SyracuseSanitize(data):
    info = {}
    info["link"] = data[1]
    info["first_name"] = data[2].split(" ")[0]
    info["last_name"] = data[2].split(" ")[1]
    info["year"] = yearShortToLong(data[4])
    info["hometown"] = getSlash(data[5])[0]
    info["high_school"] = getSlash(data[5])[1]
    info["height"] = toInches(data[2])
    info["weight"] = data[3]
    return info

def Washington(soup):
    return soup.find("table", id="roster-table").tbody

def WashingtonSanitize(data):
    info = {}
    info["link"] = data[0]
    info["first_name"] = data[1].split(",")[1].strip()
    info["last_name"] = data[1].split(",")[0].strip()
    info["year"] = yearShortToLong(data[4])
    info["hometown"] = getSlash(data[5])[0]
    info["high_school"] = getSlash(data[5])[1]
    info["height"] = toInches(data[3])
    return info

def Wisconsin(soup):
    return soup.find("table", id="ctl00_cplhMainContent_dgrdRoster").tbody

def WisconsinSanitize(data):
    return {}
    info = {}
    info["link"] = data[0]
    info["first_name"] = data[1].split(" ")[0]
    info["last_name"] = data[1].split(" ")[1]
    info["year"] = yearShortToLong(data[2])
    info["hometown"] = data[3]
    return info

def Yale(soup):
    return soup.find("div", "roster").table.tbody

def YaleSanitize(data):
    info = {}
    info["link"] = data[0]
    info["first_name"] = data[1].split(" ")[0]
    info["last_name"] = data[1].split(" ")[1]
    info["year"] = yearShortToLong(data[2])
    info["hometown"] = getSlash(data[5])[0]
    info["high_school"] = getSlash(data[5])[1]
    info["height"] = toInches(data[3])
    info["weight"] = data[4]
    return info

tablefunctions = {'Wisconsin.htm': Wisconsin,
                  'Brown.htm': Brown,
                  'Washington.htm': Washington,
                  'Stanford.htm': Stanford,
                  'Pennsylvania.htm': Pennsylvania,
                  'Princeton.htm': Princeton,
                  'BU.htm': BU,
                  'Navy.htm': Navy,
                  'Columbia.htm': Columbia,
                  'California.htm': California,
                  'Dartmouth.htm': Dartmouth,
                  'HolyCross.htm': HolyCross,
                  'Harvard.htm': Harvard,
                  'FIT.htm': FIT,
                  'Northeastern.htm': Northeastern,
                  'Cornell.htm': Cornell,
                  'GW.htm': GW,
                  'SantaClara.htm': SantaClara,
                  'OKCity.htm': OKCity,
                  'OregonState.htm': OregonState,
                  'Syracuse.htm': Syracuse,
                  'Drexel.htm': Drexel,
                  'Yale.htm': Yale,
                  'Hobart.htm': Hobart}

sanitizefunctions = {'Wisconsin.htm': WisconsinSanitize,
                  'Brown.htm': BrownSanitize,
                  'Washington.htm': WashingtonSanitize,
                  'Stanford.htm': StanfordSanitize,
                  'Pennsylvania.htm': PennsylvaniaSanitize,
                  'Princeton.htm': PrincetonSanitize,
                  'BU.htm': BUSanitize,
                  'Navy.htm': NavySanitize,
                  'Columbia.htm': ColumbiaSanitize,
                  'California.htm': CaliforniaSanitize,
                  'Dartmouth.htm': DartmouthSanitize,
                  'HolyCross.htm': HolyCrossSanitize,
                  'Harvard.htm': HarvardSanitize,
                  'FIT.htm': FITSanitize,
                  'Northeastern.htm': NortheasternSanitize,
                  'Cornell.htm': CornellSanitize,
                  'GW.htm': GWSanitize,
                  'SantaClara.htm': SantaClaraSanitize,
                  'OKCity.htm': OKCitySanitize,
                  'OregonState.htm': OregonStateSanitize,
                  'Syracuse.htm': SyracuseSanitize,
                  'Drexel.htm': DrexelSanitize,
                  'Yale.htm': YaleSanitize,
                  'Hobart.htm': HobartSanitize}

def sub(item):
    return re.sub(u'[\n\t]+', u'', item).strip()

def quotify(s):
    if type(s) == NoneType:
        return u'""'
    elif type(s) == ListType:
        return [quotify(x) for x in s]
    elif type(s) == DictType:
        temp = {}
        for key in s:
            temp[key] = quotify(s[key])
        return temp
    elif type(s) != UnicodeType:
        s = unicode(s)
    return u'"' + sub(s).strip() + u'"'

rosters = {}

for filename in os.listdir("./rosters"):
    if not filename.endswith(".htm"):
        continue
    f = open("rosters/" + filename, 'r') 
    soup = BeautifulSoup(f.read(), "html.parser")
    f.close()

    table = tablefunctions[filename](soup)
    if type(table) == ListType:
        rows = table
    else:
        rows = table.findAll("tr")

    roster = []
    for row in rows:
        data = []
        for td in row.findAll("td"):
            if td.a:
                data.append(td.a["href"])
            data.append(sub(td.text))
        sanitized = sanitizefunctions[filename](data)
        roster.append(sanitized)
        
    rosters[filename[0:-4]] = roster

conn = sqlite3.connect("athletes.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS athlete (
                id INTEGER PRIMARY KEY,
                first_name text,
                last_name text,
                height real,
                weight integer,
                hometown text,
                high_school text,
                team text,
                year text,
                age integer,
                major text,
                side text)''')

for team, roster in sorted(rosters.items()):
    print team
    for athlete in roster:
        if athlete:
            first_name = athlete.get("first_name")
            last_name = athlete.get("last_name")
            height = athlete.get("height")
            weight = athlete.get("weight")
            hometown = athlete.get("hometown")
            high_school = athlete.get("high_school")
            year = athlete.get("year")
            age = athlete.get("age")
            major = athlete.get("major")
            side = athlete.get("side")
            info = quotify([first_name, last_name, height, weight, hometown, high_school, team, year, age, major, side])
            c.execute(u"INSERT INTO athlete (first_name, last_name, height, weight, hometown, high_school, team, year, age, major, side)VALUES (" + u",".join(info) + u");")
            print u"Successfully added " + unicode(first_name) + u' ' + unicode(last_name)

conn.commit()
conn.close()
