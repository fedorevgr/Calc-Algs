from pandas import DataFrame
from numpy import linspace
from  src.Math.Spline import SplineInterpolation
from matplotlib import pyplot as plt

func = lambda x: x ** 2

LEFT = 0
RIGHT = 5
TEST_SEG = 6


X = linspace(LEFT, RIGHT, TEST_SEG)
srcData = {
    "x": X,
    "y": list(map(func, X))
}

data = DataFrame(srcData)
print(data)

spline = SplineInterpolation(data)

print(spline.spline)
print(spline(2))

X = linspace(LEFT, RIGHT, 200)
Y = list(map(spline, X))
plt.scatter(data["x"], data["y"])
plt.plot(X, Y)
plt.show()
