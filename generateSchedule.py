# Generates a season schedule for a given league in a series of tuples
# Needs to be developed to more specifically apply to fantasy rowing

import sys, itertools, random
from models import League

def main(args):
    league = League(args[1])
    teams = league.get_members()

    set_size = 2
    schedule = set()
    teamrange = range(len(teams))
    for comb in itertools.product(teamrange, repeat=set_size):
        comb = sorted(list(comb))
        if len(set(comb)) == set_size:
            schedule.add(tuple(comb))

    schedule = list(schedule)
    random.shuffle(schedule)
    print schedule

if __name__ == "__main__":
    main(sys.argv)
