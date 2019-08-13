

class Tile:
    def __init__(self, id, paths):
        self.paths_ = paths

        symmetric = map(lambda tup: (tup[1], tup[0], tup[2]), paths)
        self.paths_ = self.paths_ + list(symmetric)

        print(self.paths_)
        self.id_ = id

    def rotate(self, cw):
        pass

    def getConnection(self, entrance_id):
        return self.paths_[entrance_id]


class Level:
    def __init__(self):
        self.board_ =  [ [ None for i in range(7) ] for j in range(7) ]

    def constructPath(self, entrance_id, x, y):
        socket = self.getSocket(x, y)
        if (socket is None):
            return None

        entrance = socket.getEntrance(entrance_id)
        if entrance is None or isinstance(entrance, EntranceConnection):
            return None


        path = self.traverse(entrance_id, x, y)
        return path

    def traverse(self, entrance_id, x, y):
        socket = self.getSocket(x, y)
        if (socket is None):
            return []

        connection = socket.getConnection(entrance_id)

        path = []
        if (connection[1] in [0, 1]): # Go north
            path = self.traverse(5 - connection[1], x, y - 1)
        elif (connection[1] in [2, 3]): # Go east
            path = self.traverse(9 - connection[1], x + 1, y)
        elif (connection[1] in [4, 5]): # Go south
            path = self.traverse(5 - connection[1], x, y + 1)
        elif (connection[1] in [6, 7]): # Go west
            path = self.traverse(9 - connection[1], x - 1, y)

        return [connection] + path

    def getSocket(self, x, y):
        try:
            return self.board_[x][y]
        except IndexError:
            return None


class Level3(Level):
    def __init__(self):
        super().__init__()

        self.board_[0][0] = Socket([
            None, None,
            None, EntranceCountTiles,
            EntranceConnection, EntranceConnection,
            None, EntrancePagoda
            ])

        self.board_[0][1] = Socket([
            EntranceConnection, EntranceConnection,
            None, EntrancePagoda,
            None, None,
            None, None
        ])


class EntranceCountBridges:
    def __init__(self, count):
        self.count_ = count

class EntranceColor:
    def __init__(self, color):
        self.color_ = color

class EntrancePagoda:
    def __init__(self):
        pass

    def check(path):
        return len(list(filter(lambda p: p(2) == 'p', path.path_))) > 0

class EntranceCountTiles:
    def __init__(self, count):
        self.count_ = count

class EntranceYinYang:
    def __init__(self):
        pass

class EntranceConnection:
    def __init__(self):
        pass

class Socket:
    def __init__(self, entrances):
        self.entrances_ = entrances
        self.tile_ = None

    def setTile(self, tile):
        self.tile_ = tile

    def getEntrance(self, entrance_id):
        try:
            return self.entrances_[entrance_id]
        except IndexError:
            return None


    def getConnection(self, entrance_id):
        return self.tile_.getConnection(entrance_id)



def createTiles():
    tiles = [
        Tile(0, [(0, 5, 'b'), (1, 6, None), (2, 7, 'b'), (3, 4, None)]), #ok
        Tile(1, [(0, 6, None), (1, 7, None), (2, 5, 'p'), (3, 4, None)]), #ok
        Tile(2, [(0, 5, 'b'), (1, 7, None), (2, 3, None), (4, 6, None) ]),#ok
        Tile(3, [(0, 3, None), (1, 7, None), (2, 5, None), (4, 6, None) ]),
        Tile(4, [(0, 1, None), (2, 7, 'b'), (3, 4, None), (5, 6, None) ]),
        Tile(5, [(0, 7, None), (1, 3, None), (2, 100, 'p'), (5, 5, None), (6, 100, 'p')]),
        Tile(6, [(0, 1, None), (2, 5, None), (3, 6, 'b'), (4, 7, None) ]),
    ]

    return tiles

if __name__ == "__main__":
    tiles = createTiles()

    l3 = Level3()

    l3.board_[0][0].setTile(tiles[6])
    l3.board_[0][1].setTile(tiles[5])

    l3.constructPath(7, 0, 0)