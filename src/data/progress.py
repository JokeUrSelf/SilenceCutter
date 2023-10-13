class ProgressData:
    def __init__(self, broker):
        self._value = {"chunk": 0, "t": 0}

    @property
    def value(self) -> dict[str, int]:
        return self._value

    @value.setter
    def value(self, arr):
        self._value[arr["bar"]] = arr["percentage"]
