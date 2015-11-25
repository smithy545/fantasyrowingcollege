import sys
from models import League

def main(args):
    league = League(args[1])
    teams = league.get_members()

    for team in teams:
        print team

def roundRobin(teams, sets = None):
    """ Generates a schedule of "fair" pairings from a list of units """
    count = len(units)
    sets = sets or (count - 1)
    half = count / 2
    for turn in range(sets):
        left = units[:half]
        right = units[count - half - 1 + 1:][::-1]
        pairings = zip(left, right)
        if turn % 2 == 1:
            pairings = [(y, x) for (x, y) in pairings]
        units.insert(1, units.pop())
        yield pairings

if __name__ == "__main__":
    main(sys.argv)
