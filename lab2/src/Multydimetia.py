from pandas import DataFrame
from enum import Enum

from .Math.Spline import SplineInterpolation as SI
from .Math.Newton import InterpolationTable as NI


class Method(Enum):
    Newton = NI
    Spline = SI


type dataT = dict[float, dict[float, ...]]
type VectorT = list[float]
type MethodVectorT = list[Method]
type PowerVectorT = list[int]


class MultidimensionalInterpolatorInator:
    @staticmethod
    def interp(
            data: dataT,
            vector: VectorT,
            mVector: MethodVectorT | Method,
            _powers: PowerVectorT | int = 1
    ) -> float:

        if isinstance(mVector, Method):
            mVector = [mVector] * len(vector)

        if isinstance(_powers, int):
            _powers = [_powers] * len(vector)

        if isinstance(list(data.values())[0], float | int):
            return MultidimensionalInterpolatorInator.unionInterpolate(data, vector[0], mVector[0], _powers[0])

        else:
            newData: dict[float, float] = {}

            for x, val in data.items():
                newData[x] = MultidimensionalInterpolatorInator.interp(val, vector[1:], mVector[1:], _powers[1:])

            return MultidimensionalInterpolatorInator.unionInterpolate(newData, vector[1], mVector[1], _powers[1])

    @staticmethod
    def unionInterpolate(d: dict, val: float, method: Method, _power: int = 0):
        if method == Method.Spline:
            return SI(DataFrame(d.items()))(val)
        else:
            return NI.newtonInterpolation(DataFrame(d.items()), _power, val)(val)

