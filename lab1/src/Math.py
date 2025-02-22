from pandas import DataFrame, concat
from numpy import nan

from typing import Iterable, Callable

from math import factorial as fact
from math import ceil, prod

from .exc import InterpolationError


type _Pn = Callable[[float], float]


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

    configuration: DataFrame = data.sort_values(by=data.columns[0], key=lambda col: abs(col - val)).iloc[:power].copy()
    configuration.sort_values(by=data.columns[0], inplace=True)

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
    configuration: DataFrame = getRawConfiguration(data, power + 1, val)

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

    if nArgs % 3 == 2:
        configurationExtensions.append(configuration.iloc[[-1]].copy())

    configuration = concat([configuration] + configurationExtensions, ignore_index=True)

    configuration.sort_values(by="tag", inplace=True)

    print(configuration)
    return __newtonInterpolate(configuration)


def getPolynomial(configurationTable: DataFrame) -> _Pn:
    confRow: DataFrame = configurationTable.iloc[0]
    xs: DataFrame = configurationTable.iloc[:, 0]

    return lambda x: sum(
        prod(x - xs.iloc[j-1] for j in range(1, i)) * confRow.iloc[i]
        for i in range(1, len(confRow))
    )


def stringPolynomial(configurationTable: DataFrame) -> str:
    confRow: DataFrame = configurationTable.iloc[0]
    xs: DataFrame = configurationTable.iloc[:, 0]

    return " + ".join(
        "".join(f"(x - {xs.iloc[j-1]})" for j in range(1, i)) +
        f" * ({confRow.iloc[i]})"
        for i in range(1, len(confRow)))
