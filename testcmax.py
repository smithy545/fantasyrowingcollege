import matplotlib.pyplot as plt

# Not upset
for cmax in range(0, 20):
    winner = []
    loser = []
    for mov in range(0, 60):
        winner.append((mov - cmax + 10))
        loser.append((cmax - mov + 2))
    plt.figure(1)
    plt.xlabel('MOV - dCMAX')
    plt.ylabel('Points earned')
    plt.plot([x - cmax for x in range(0,60)],winner, 'rx')
    plt.plot([x - cmax for x in range(0,60)],loser, 'bo')

plt.show()

# Upset
for cmax in range(0, 20):
    winner = []
    loser = []
    for mov in range(0, 60):
        winner.append(-(mov + cmax + 10))
        loser.append((cmax + mov + 5))
    plt.figure(2)
    plt.xlabel('MOV - dCMAX')
    plt.ylabel('Points earned')
    plt.plot([x - cmax for x in range(0,60)],winner, 'rx')
    plt.plot([x - cmax for x in range(0,60)],loser,'bo')

plt.show()
