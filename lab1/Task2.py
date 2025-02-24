from pandas import DataFrame

from src.Math import InterpolationTable
from src.Table import Table


DATA_FILE: str = "data/data.txt"


POWERS: int = 5


def main() -> int:
    table: Table = Table(DATA_FILE)
    data: DataFrame = DataFrame(table.data, dtype="float64")
    data["x'"] = 1 / data["y'"]
    data["x''"] = - data["y''"] / (data["y'"] ** 2)

    reverseData: DataFrame = data[["y", "x", "x'", "x''"]]

    power: int
    try:
        power = int(input("Enter power: "))
    except ValueError:
        print("Invalid input")
        return 1

    if power < 0:
        print("Invalid input")
        return 1

    valNewton: float = InterpolationTable.newtonInterpolation(reverseData, power, 0)(0)
    valHermite: float = InterpolationTable.hermiteInterpolation(reverseData, power, 0)(0)

    print(f"Newton:\t{valNewton}\nHermite:\t{valHermite}")

    return 0


if __name__ == '__main__':
    exit(main())
