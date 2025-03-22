from math import exp
from pprint import pprint
from numpy import linspace
from webcolors import names

from src.Multydimetia import MultidimensionalInterpolatorInator as MII
from src.Multydimetia import Method
from matplotlib import pyplot as plt

def FUNCTION(x, y, z):
    return 1 / (x + y) - z # exp(-(x*x + y*y + z*z))

taskValues: dict[float, dict[float, ...]] = {}

xValues = linspace(-1, 2, 20)
yValues = linspace(-1, 4, 50)
zValues = linspace(-1, 2, 30)

for z in zValues:
   taskValues[z] = {}
   for y in yValues:
       taskValues[z][y] = {}
       for x in xValues:
           fVal = FUNCTION(x, y, z)
           taskValues[z][y][x] = fVal

nValues = {}

for z in taskValues.keys():
    nValues[z] = {}
    for y in taskValues[z].keys():
        nValues[z][y] = {}
        for x in taskValues[z][y].keys():
            if x + y > 0:
                nValues[z][y][x] = 1 / taskValues[z][y][x]

for z in list(nValues.keys()):
    for y in list(nValues[z].keys()):
        if nValues[z][y] == {}:
            nValues[z].pop(y)

for z in list(nValues.keys()):
    if nValues[z] == {}:
        nValues.pop(z)



vector = [0.152, -.151, 0.1]
print(FUNCTION(*vector))

vector.reverse()
pprint(1 / MII.interp(nValues, vector, Method.Spline))
pprint(1 / MII.interp(nValues, vector, Method.Newton, 6))
# pprint(MII.interp(taskValues, vector, Method.Newton, 1))

