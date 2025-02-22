from pandas import DataFrame, concat
from numpy import nan

from typing import Optional, Iterable

from math import factorial as fact
from math import ceil

from .exc import InterpolationError


NON_DERIVE_COLS = 3


def getRawConfiguration(data: DataFrame, power: int, val: float) -> DataFrame:
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

    configuration: DataFrame = data[smallestIdx:largestIdx].copy()
    configuration["tag"] = [f"x_{i}" for i in range(power)]

    return configuration


def __newtonInterpolate(configuration: DataFrame) -> DataFrame:
    power: int = configuration.shape[0]

    interpolationLevels: Iterable[int] = range(2, power + 1)

    separateDiffTable: DataFrame = DataFrame(configuration.iloc[:, :2].values, columns=["arg", "f(arg)"])

    for levelI in interpolationLevels:
        separateDiffTable[f"f({" ".join([f"x_{i}" for i in range(levelI)])})"] = nan

        sepArgsN: int = levelI
        for rowStartIdx in range(power - levelI + 1):
            tableBefore: DataFrame = separateDiffTable.iloc[rowStartIdx:rowStartIdx+sepArgsN, [0, levelI-1]]
            x_0: float = tableBefore.iloc[0, 0]
            x_n: float = tableBefore.iloc[-1, 0]
            res: float

            if x_0 != x_n:
                res = (
                        (tableBefore.iloc[0, 1] - tableBefore.iloc[1, 1])
                        /
                        (x_0 - x_n)
                )
            else:
                res = configuration.iloc[0, 1 + sepArgsN - 1] / fact(sepArgsN - 1)

            separateDiffTable.iat[rowStartIdx, levelI] = res

    return separateDiffTable


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
    configuration: DataFrame = getRawConfiguration(data, power, val)

    return __newtonInterpolate(configuration)


def hermiteInterpolationBAD(data: DataFrame, power: int, val: float) -> DataFrame:
    """
    Assume all derivatives are known
    :param data:
    :param power:
    :param val:
    :return:
    """
    confPoints: int = (power + 1) // 3  # sum(n_k) = power + 1

    configuration: DataFrame = getRawConfiguration(data, confPoints, val)
    configExtension: DataFrame = configuration.copy()

    configuration = concat(
        [configuration] + [configExtension.copy() for _ in range(data.shape[1] - 2)], ignore_index=True
    )  # todo add even control sum(n_k) = power + 1

    configuration.sort_values(by="tag", inplace=True)
    print(configuration)

    return __newtonInterpolate(configuration)


def hermiteInterpolation(data: DataFrame, power: int, val: float) -> DataFrame:
    """
    Assume all derivatives are known
    :param data:
    :param power:
    :param val:
    :return:
    """
    nArgs: int = power + 1
    configuration: DataFrame = getRawConfiguration(data, ceil(nArgs / 3), val)

    configuration.sort_values(by=configuration.columns[0], key=lambda col: abs(col - val), inplace=True)

    configurationExtensions: list[DataFrame] = []

    for copiedRowIdx in range(nArgs // 3):
        configurationExtensions.append(configuration.iloc[[copiedRowIdx]].copy())
        configurationExtensions.append(configuration.iloc[[copiedRowIdx]].copy())

    if nArgs % 3 != 0:
        configurationExtensions.append(configuration.iloc[[-1]].copy())

    configuration = concat([configuration] + configurationExtensions, ignore_index=True)

    configuration.sort_values(by="tag", inplace=True)

    print(configuration)
    return __newtonInterpolate(configuration)

