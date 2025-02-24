from pandas import DataFrame

from .Table import Table
from .Math import InterpolationTable, _Pn


DATA_FILE: str = "data/data.txt"
table: Table = Table(DATA_FILE)


data: DataFrame = DataFrame(table.data, dtype="float64")

"""
y = f(x)
y' = dy/dx
dx / dy = 1/y'
"""
data["x'"] = 1 / data["y'"]

"""
d2x/dy2 = - y''/y'^2
"""
data["x''"] = - data["y''"] / (data["y'"] ** 2)

directData: DataFrame = data[["x", "y", "y'", "y''"]]
reverseData: DataFrame = data[["y", "x", "x'", "x''"]]


def main() -> int:
    newtonPower: int
    hermitPower: int
    X: float

    try:
        newtonPower = int(input("Enter newton power: "))
        hermitPower = int(input("Enter hermit power: "))
        X = float(input("Enter X: "))
    except ValueError:
        print("Invalid input")
        return 1

    newton: _Pn = InterpolationTable.newtonInterpolation(directData, newtonPower, X)
    hermit: _Pn = InterpolationTable.hermiteInterpolation(directData, hermitPower, X)

    print(f"Newton calculated value: {newton(X)}")
    print(f"Hermit calculated value: {hermit(X)}")

    return 0


if __name__ == "__main__":
    exit(main())

