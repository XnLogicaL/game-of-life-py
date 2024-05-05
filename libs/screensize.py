class ScreenSize:
    def __init__(self, x, y):
        self.X = int(x)
        self.Y = int(y)

        self.aspect_ratio = int(x) / int(y)

    def to_tuple(self):
        return self.X, self.Y

    def to_arr(self):
        return [self.X, self.Y]

    def to_dict(self):
        return {"X": self.X, "Y": self.Y}
