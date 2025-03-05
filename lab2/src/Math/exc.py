class InterpolationError(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class IllegalDataError(Exception):
    def __init__(self, msg: str):
        self.msg = msg
