from pandas import DataFrame
from numpy import nan
from bisect import bisect_left

from .exc import IllegalDataError


class SplineInterpolation:
    spline: DataFrame
    __KsiZero: float = 0
    __NuZero: float = 0

    def __init__(self, configuration: DataFrame) -> None:
        if configuration.shape[1] != 2:
            raise IllegalDataError("Table width is not 2")
        if configuration.shape[0] < 3:
            raise IllegalDataError("Table height is less than 2")

        X: DataFrame = configuration.iloc[:, 0]
        Y: DataFrame = configuration.iloc[:, 1]

        self.spline = DataFrame(
            nan,
            index=range(configuration.shape[0] + 1),
            columns=["x_i", "y_i", "A", "B", "C", "D", "F", "k", "n"]
        )
        self.spline["x_i"] = X.shift(1)
        self.spline["y_i"] = Y.shift(1)

        self.spline.loc[0, "C"] = 0
        self.spline.loc[configuration.shape[0], "C"] = 0

        self.spline.loc[1:, "A"] = Y.shift(1)
        self.spline.loc[1:, "D"] = X - X.shift(1)
        # -2 * (h_n - h_(n-1))
        self.spline.loc[1:, "B"] = (X + X.shift(1)) * -2
        self.spline.loc[:, "F"] = 3 * (
            (Y.shift(1) - Y.shift(2)) / self.spline["D"].shift(1) -
            (Y - Y.shift(1)) / self.spline.D
        )

        self.spline.loc[2, "k"] = self.__KsiZero
        self.spline.loc[2, "n"] = self.__NuZero

        self.straightPath()
        self.reversePath()

        C = self.spline.C
        H = self.spline.D
        f2 = (C.shift(-1) - 2 * C.shift(1))
        f1 = (Y - Y.shift(1)) / H

        self.spline.B = f1 - H * f2 / 3

        self.spline.D = (C.shift(-1) - C) / (3 * H)

    def straightPath(self):
        F: DataFrame = self.spline["F"]
        D: DataFrame = self.spline["D"]
        B: DataFrame = self.spline["B"]
        A: DataFrame = self.spline["A"]
        ksi: DataFrame = self.spline["k"]
        nu: DataFrame = self.spline["n"]

        for i in range(2, self.spline.shape[0]):
            ksi[i+1] = D[i] / (B[i] - A[i] * ksi[i])
            nu[i+1] = (A[i] * nu[i] + F[i]) / (B[i] - A[i] * ksi[i])

    def reversePath(self):
        C: DataFrame = self.spline["C"]
        K: DataFrame = self.spline["k"]
        N: DataFrame = self.spline["n"]

        for i in range(self.spline.shape[0] - 1, 1, -1):
            C[i-1] = K[i] * C[i] + N[i]


    def __call__(self, x: float) -> float:
        # 1 2 3 4
        #    ^
        #    2.5
        rowDF = self.spline[self.spline["x_i"] <= x]

        if rowDF.empty:
            row = self.spline.iloc[0]
        else:
            row = rowDF.iloc[-1]

        return row.A + row.B * (x - row.x_i) + row.C * (x - row.x_i) ** 2 + row.D * (x - row.x_i) ** 3

