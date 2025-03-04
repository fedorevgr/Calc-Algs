from pandas import DataFrame


type _SliceT = list[list[float]]


class Table:
    data: dict[str, _SliceT] = {}

    def __init__(self, filename: str):
        self.data = {}
        with open(filename, 'r') as f:
            lastZ = ""
            for line in f:
                line = line.strip()

                if not line:
                    continue

                if line.startswith('z'):
                    lastZ = line
                    self.data[lastZ] = []
                elif line.startswith('y\\x'):
                    continue
                else:
                    line = list(map(float, line.split()[1:]))
                    self.data[lastZ].append(line)

    def getAsDF(self) -> dict[str, tuple[float, DataFrame]]:
        return {
            z: (
                float(z[2:]),
                DataFrame(tbl)
            ) for z, tbl in self.data.items()
        }
