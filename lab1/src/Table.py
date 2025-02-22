class Table:
    data: dict[str, list[float]] = {}

    def __init__(self, filename: str):
        with open(filename, 'r') as f:
            header = f.readline().split()
            data = list(map(lambda x: x.split(), f.readlines()))

            for i, tag in enumerate(header):
                self.data[tag] = list(map(lambda x: float(x[i]), data))

