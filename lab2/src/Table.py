from pandas import DataFrame

type _SliceT = list[list[float]]

ABOBA = {
    0: {
        0: {0: 0, 1: 1, 2: 4, 3: 9, 4: 16},
        1: {0: 1, 1: 2, 2: 5, 3: 10, 4: 17},
        2: {0: 4, 1: 5, 2: 8, 3: 13, 4: 20},
        3: {0: 9, 1: 10, 2: 13, 3: 18, 4: 25},
        4: {0: 16, 1: 17, 2: 20, 3: 25, 4: 32}
    },
    1: {
        0: {0: 1, 1: 2, 2: 5, 3: 10, 4: 17},
        1: {0: 2, 1: 3, 2: 6, 3: 11, 4: 18},
        2: {0: 5, 1: 6, 2: 9, 3: 14, 4: 21},
        3: {0: 10, 1: 11, 2: 14, 3: 19, 4: 26},
        4: {0: 17, 1: 18, 2: 21, 3: 26, 4: 33}
    },
    2: {
        0: {0: 4, 1: 5, 2: 8, 3: 13, 4: 20},
        1: {0: 5, 1: 6, 2: 9, 3: 14, 4: 21},
        2: {0: 8, 1: 9, 2: 12, 3: 17, 4: 24},
        3: {0: 13, 1: 14, 2: 17, 3: 22, 4: 29},
        4: {0: 20, 1: 21, 2: 24, 3: 29, 4: 36}
    },
    3: {
        0: {0: 9, 1: 10, 2: 13, 3: 18, 4: 25},
        1: {0: 10, 1: 11, 2: 14, 3: 19, 4: 26},
        2: {0: 13, 1: 14, 2: 17, 3: 22, 4: 29},
        3: {0: 18, 1: 19, 2: 22, 3: 27, 4: 34},
        4: {0: 25, 1: 26, 2: 29, 3: 34, 4: 41}
    },
    4: {
        0: {0: 16, 1: 17, 2: 20, 3: 25, 4: 32},
        1: {0: 17, 1: 18, 2: 21, 3: 26, 4: 33},
        2: {0: 20, 1: 21, 2: 24, 3: 29, 4: 36},
        3: {0: 25, 1: 26, 2: 29, 3: 34, 4: 41},
        4: {0: 32, 1: 33, 2: 36, 3: 41, 4: 48}
    }
}


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
