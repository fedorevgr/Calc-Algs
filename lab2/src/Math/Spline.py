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
            columns=["x_i", "y_i", "h_i", "A", "B", "C", "D", "F", "k", "n"]
        )
        self.spline["x_i"] = X.shift(1)
        self.spline["y_i"] = Y.shift(1)
        self.spline["h_i"] = X - X.shift(1)

        self.spline.loc[0, "C"] = 0
        self.spline.loc[configuration.shape[0], "C"] = 0

        self.spline.loc[1:, "A"] = Y.shift(1)

        self.spline.loc[:, "F"] = 3 * (
                (Y.shift(1) - Y.shift(2)) / self.spline.h_i.shift(1) -
                (Y - Y.shift(1)) / self.spline.h_i
        )

        self.spline.loc[2, "k"] = self.__KsiZero
        self.spline.loc[2, "n"] = self.__NuZero

        self.straightPath()
        self.reversePath()

        C = self.spline.C
        H = self.spline.h_i
        f2 = (C.shift(-1) - 2 * C)
        f1 = (Y - Y.shift(1)) / H

        self.spline.B = f1 - H * f2 / 3

        self.spline.D = (C.shift(-1) - C) / (3 * H)

    def straightPath(self):
        D: DataFrame = self.spline.h_i
        A: DataFrame = self.spline.h_i.shift(1)

        F: DataFrame = self.spline["F"]

        B: DataFrame = -2 * (A + D)

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
        rowDF = self.spline[self.spline["x_i"] < x]

        if rowDF.empty:
            row = self.spline.iloc[0]
        else:
            row = rowDF.iloc[-1]

        return row.A + row.B * (x - row.x_i) + row.C * (x - row.x_i) ** 2 + row.D * (x - row.x_i) ** 3

    def __repr__(self):
        return "\n".join(
            f"{row.A:g} + {row.B:g} * (x - {row.x_i:g}) + {row.C:g} * (x - {row.x_i:g})^2 + {row.D:g} * (x - {row.x_i:g})^3"
            for i, row in self.spline.iterrows()
        )
