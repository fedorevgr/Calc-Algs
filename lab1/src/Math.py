from pandas import DataFrame, Series

from typing import Optional

from .exc import InterpolationError


def gatherPoints(data: DataFrame, power: int, val: float) -> DataFrame:
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

    nearestRow: Optional[Series] = data.min(key=lambda x: abs(x[0] - val))

    if nearestRow is None:
        raise RuntimeError("Cannot find nearest point")

    smallestIdx: int = nearestRow.index - power // 2
    largestIdx: int = smallestIdx + power + 1

    if smallestIdx < 0:
        smallestIdx, largestIdx = 0, power + 1
    elif largestIdx > len(data) - 1:
        largestIdx = len(data) - 1
        smallestIdx = largestIdx - power - 1

    return data.iloc[smallestIdx:largestIdx]


def newtonInterpolation(data: DataFrame, power: int, val: float) -> DataFrame:
    """
    Performs Newton interpolation
    if columns more the 2 - derivatives also would be included into calculation
    :param data: 1st column: val, 2nd column: f(val), 3rd column: f'(val), ...
    :param power: Interpolation power
    :param val: value to interpolate
    :return: Interpolation table adjusted to left upper corner
    """
    workingData: DataFrame = gatherPoints(data, power, val)

    return workingData


def hermiteInterpolation(data: DataFrame, power: int, val: float) -> DataFrame:
    workingData: DataFrame = gatherPoints(data, power, val)

    return workingData

