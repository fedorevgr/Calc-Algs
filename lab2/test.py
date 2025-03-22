from pandas import DataFrame
from numpy import linspace
from src.Math.Spline import SplineInterpolation
from matplotlib import pyplot as plt


func = lambda x: 1/x

LEFT = 0.0001
RIGHT = 2
TEST_SEG = 50


X = linspace(LEFT, RIGHT, TEST_SEG)
srcData = {
    "x": X,
    "y": list(map(func, X))
}

data = DataFrame(srcData)
print(data)

spline = SplineInterpolation(data)

print(spline.spline)
print(spline(0))

