import matplotlib.pyplot as plt

# Not upset
for cmax in range(0, 20):
    winner = []
    loser = []
    for mov in range(0, 60):
        winner.append((mov - cmax + 10)*2)
        loser.append((cmax - mov + 2)*2)
    plt.figure(1)
    plt.plot(range(0,60),winner)
    plt.plot(range(0,60),loser)

plt.show()

# Upset
for cmax in range(0, 20):
    winner = []
    loser = []
    for mov in range(0, 60):
        winner.append(-2*(mov + cmax + 10))
        loser.append((cmax + mov + 5)*2)
    plt.figure(2)
    plt.plot(range(0,60),winner)
    plt.plot(range(0,60),loser)

plt.show()
