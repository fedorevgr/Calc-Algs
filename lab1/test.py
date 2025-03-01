from pandas import DataFrame

from src.Math import InterpolationTable
from src.Table import Table
import numpy as np

DATA_FILE: str = "data/data.txt"

table: Table = Table(DATA_FILE)
data: DataFrame = DataFrame(table.data, dtype="float64")
data["x'"] = 1 / data["y'"]
data["x''"] = - data["y''"] / (data["y'"] ** 2)

reverseData: DataFrame = data[["y", "x", "x'", "x''"]][data["x"] <= 1]
print(reverseData)

meth = InterpolationTable.newtonInterpolation(reverseData, 5, 0)

print(meth)
print(meth(0))