from pandas import DataFrame
from numpy import nan

from typing import Optional, Iterable

from .exc import InterpolationError


def getConfiguration(data: DataFrame, power: int, val: float) -> DataFrame:
    """
    Returns DataFrame of adjacent values to val

    :param data: DataFrame of values in the 1st column
    :param power: power of interpolation, requires 'power + 1' rows
    :param val: value of the first column
    :return: DataFrame of adjacent values to val
    :raises InterpolationError, RuntimeError: Interpolation error if not enough rows, RuntimeError if any other error
    """
    if len(data) < power + 1:
        raise InterpolationError("Not enough points")

    nearestRowIdx: int = (data.iloc[:, 0] - val).abs().idxmin()

    smallestIdx: int = nearestRowIdx - power // 2
    largestIdx: int = smallestIdx + power

    if smallestIdx < 0:
        smallestIdx, largestIdx = 0, power  # todo: check indexes
    elif largestIdx > len(data) - 1:
        largestIdx = len(data) - 1
        smallestIdx = largestIdx - power

    return data[smallestIdx:largestIdx]


def newtonInterpolation(data: DataFrame, power: int, val: float) -> DataFrame:
    """
    Performs Newton interpolation
    if columns more the 2 - derivatives also would be included into calculation
    :param data: 1st column: val, 2nd column: f(val), 3rd column: f'(val), ...
    :param power: Interpolation power
    :param val: value to interpolate
    :return: Interpolation table adjusted to left upper corner
    :raises InterpolationError, RuntimeError: Interpolation error if not enough rows
    """
    configuration: DataFrame = getConfiguration(data, power, val)

    interpolationLevels: Iterable[int] = range(2, power + 1)

    separateDiffTable: DataFrame = DataFrame(configuration.iloc[:, :2].values, columns=["x", "y"])

    for levelI in interpolationLevels:
        separateDiffTable[f"y({" ".join([f"x_{i}" for i in range(levelI)])})"] = nan

        sepArgsN: int = levelI
        for rowStartIdx in range(power - levelI + 1):
            tableBefore: DataFrame = separateDiffTable.iloc[rowStartIdx:rowStartIdx+sepArgsN, [0, levelI-1]]
            separateDiffTable.iat[rowStartIdx, levelI] = (
                    (tableBefore.iloc[0, 1] - tableBefore.iloc[1, 1])
                    /
                    (tableBefore.iloc[0, 0] - tableBefore.iloc[-1, 0])
            )

    return separateDiffTable


def hermiteInterpolation(data: DataFrame, power: int, val: float) -> DataFrame:
    configuration: DataFrame = getConfiguration(data, power, val)

    return configuration

