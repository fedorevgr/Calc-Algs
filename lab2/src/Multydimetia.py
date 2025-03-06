from pandas import DataFrame

from .Math.Spline import SplineInterpolation as SI
from .Math.Newton import InterpolationTable as NI

type dataT = dict[float, dict[float, ...]]
type VectorT = list[float]


class MultidimensionalInterpolatorInator:
    @staticmethod
    def interp(data: dataT, vector: VectorT) -> float:
        if isinstance(list(data.values())[0], float | int):
            return SI(DataFrame(data.items()))(vector[0])

        else:
            newData: dict[float, float] = {}

            for x, val in data.items():
                newData[x] = MultidimensionalInterpolatorInator.interp(val, vector[1:])

            return SI(DataFrame(newData.items()))(vector[1])
