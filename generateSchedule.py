import sys
from models import League

def main(args):
    league = League(args[1])
    teams = league.get_members()

    for team in teams:
        print team

if __name__ == "__main__":
    main(sys.argv)
