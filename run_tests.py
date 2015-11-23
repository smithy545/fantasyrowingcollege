import os
from tabulate import tabulate
second = 5
other = 10

washington = []

def transpose(matrix):
    newMatrix = []
    for x in matrix:
        for i in range(x):
            

for head in range(5, 15):
    for sprint in range(15,25):
        f = open("config.txt", "w")
        f.write("KHEAD = " + str(head)\
                + "\nKSPRINT = " + str(sprint)\
                + "\nKSECOND = " + str(second)\
                + "\nKOTHER = " + str(other))
        f.close()
        execfile("big crew compare.py")

        washington.append([row[9] for row in table])


print tabulate(washington)
