from pandas import DataFrame

from src.Math import InterpolationTable
from src.Table import Table


DATA_FILE: str = "data/data.txt"


POWERS: int = 5


def main() -> int:
    table: Table = Table(DATA_FILE)
    data: DataFrame = DataFrame(table.data, dtype="float64")

    x: float

    try:
        x = float(input("Enter x: "))
    except ValueError:
        print("Invalid input")
        return 1

    results: dict[str, list[float]] = {"newton": [0] * POWERS, "hermite": [0] * POWERS}

    for power in range(1, POWERS + 1):
        val_: float = InterpolationTable.newtonInterpolation(data, power, x)(x)
        results["newton"][power - 1] = val_

        val_ = InterpolationTable.hermiteInterpolation(data, power, x)(x)
        results["hermite"][power - 1] = val_

    print(DataFrame(data=results))

    return 0


if __name__ == '__main__':
    exit(main())
