from src.Table import Table
from src.Math import InterpolationTable

from pandas import DataFrame, concat
from numpy import nan

t1: Table = Table("data/data3_1")
t2: Table = Table("data/data3_2")

data1: DataFrame = DataFrame(t1.data, dtype="float64")
data2: DataFrame = DataFrame(t2.data, dtype="float64")

dataExt: DataFrame = data1[["x"]].copy()
dataExt.loc[:, "y"] = nan


POWER: int = 3

for i, r in dataExt.iterrows():
    y = InterpolationTable.newtonInterpolation(data2, POWER, r["x"])(r["x"])
    dataExt.loc[i, "y"] = y

dataExt["y"] = data1["y"] - dataExt["y"]

rX: float = InterpolationTable.newtonInterpolation(dataExt[["y", "x"]].copy(), POWER, 0)(0)

print("Root X:", rX)

print("Root Y:", InterpolationTable.newtonInterpolation(data2, POWER, rX)(rX))