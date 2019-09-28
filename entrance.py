class EntranceCountBridges:
    def __init__(self, count):
        self.count_ = count

    def check(self, path):
        return len(list(filter(lambda p: p[2] == 'b', path))) == self.count_

class EntranceColor:
    def __init__(self, color):
        self.color_ = color

    def check(self, _):
        raise NotImplementedError("TODO: check for colors")

class EntrancePagoda:
    def __init__(self):
        pass

    def check(self, path):
        return len(list(filter(lambda p: p[2] == 'p', path))) > 0

class EntranceCountTiles:
    def __init__(self, count):
        self.count_ = count

    def check(self, path):
        return len(path) == self.count_

class EntranceYinYang:
    def __init__(self):
        pass

    def check(self, path):
        return len(list(filter(lambda p: p[2] == 'y', path))) > 0

class EntranceConnection:
    def __init__(self):
        pass

    def check(self, _):
        return True