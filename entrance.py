class EntranceCountBridges:
    def __init__(self, count):
        self.count_ = count

    def check(self, traversal):
        _, path = traversal
        return len(list(filter(lambda p: p[2] == 'b', path))) == self.count_

class EntranceColor:
    YELLOW = 1
    BLUE = 2
    RED = 3
    PURPLE = 4

    def __init__(self, color):
        self.color_ = color

    def check(self, traversal):
        stop, _ = traversal
        if type(stop) is EntranceColor:
            return self.color_ == stop.color_

        return False

class EntrancePagoda:
    def __init__(self):
        pass

    def check(self, traversal):
        _, path = traversal
        return len(list(filter(lambda p: p[2] == 'p', path))) > 0

class EntranceCountTiles:
    def __init__(self, count):
        self.count_ = count

    def check(self, traversal):
        _, path = traversal
        return len(path) == self.count_

class EntranceYinYang:
    def __init__(self):
        pass

    def check(self, traversal):
        _, path = traversal
        return len(list(filter(lambda p: p[2] == 'y', path))) > 0

class EntranceConnection:
    def __init__(self):
        pass

    def check(self, _):
        return True