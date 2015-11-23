# This file allows you to manually add an athlete to the sql database via console

import sqlite3
from types import *

def main():
    conn = sqlite3.connect("athletes.db")
    c = conn.cursor()

    response = raw_input("Adding a team?(y/n) ")
    team = ""
    if response == "y":
        team = raw_input("Team: ")
    response = ""

    while response != "n":
        first_name = raw_input("Athlete First Name: ").title()
        last_name = raw_input("Athlete Last Name: ").title()
        age = input("Athlete Age: ")
        feet = input("Height(feet): ")
        inches = input("Height(inches): ")
        weight = input("Weight(pounds): ")
        if team == "":
            team = raw_input("Team: ").title()
        hometown = raw_input("Hometown: ").title()
        year = input("Year: ")
        athlete = [quotify(i) for i in [first_name, last_name, age, str(feet) + "'" + str(inches),str(weight) + "lbs", team, hometown, year]]
        c.execute("insert into athlete (first_name, last_name, age, height, weight, team, hometown, year) values(" +\
                  ",".join(athlete) + ");")
        response = raw_input("Add another athlete?(y/n) ")

    conn.commit()
    conn.close()


def quotify(s):
    if type(s) == NoneType:
        return '""'
    if type(s) != StringType:
        s = str(s)
    return '"' + s + '"'
