
class Tile:
    def __init__(self, id, paths):
        self.rotation_ = 0
        self.paths_ = paths
        self.id_ = id

    def rotate(self, cw):
        if (cw == None):
            self.rotation_ = 0
        else:
            self.rotation_ = cw % 4

        print("paths before rotate, ", self.paths_)

        self.paths_ = list(map(lambda entrance: (self.mapRotation(entrance[0]), self.mapRotation(entrance[1]), entrance[2]), self.paths_))

        self.paths_.sort()


        print("paths after rotate, ", self.paths_)

    def mapRotation(self, entrance_id):
        if (entrance_id is None):
            return None

        return (entrance_id - (self.rotation_ * 2)) % 8

    def getConnection(self, entrance_id):
        return self.paths_[entrance_id]

def createTiles():
    tiles = [
        Tile(0, [(0, 5, 'b'), (1, 6, None), (2, 7, 'b'), (3, 4, None),
                (4, 3, None), (5, 0, 'b'), (6, 1, None), (7, 2, 'b')]),

        Tile(1, [(0, 6, None), (1, 7, None), (2, 5, 'p'), (3, 4, None),
                (4, 3, None), (5, 2, 'p'), (6, 0, None), (7, 1, None)]),

        Tile(2, [(0, 5, 'b'), (1, 7, None), (2, 3, None), (3, 2, None),
                (4, 6, None), (5, 0, 'b'), (6, 4, None), (7, 1, None)]),

        Tile(3, [(0, 3, None), (1, 7, None), (2, 5, None), (3, 0, None),
                (4, 6, None), (5, 2, None), (6, 4, None), (7, 1, None)]),

        Tile(4, [(0, 1, None), (1, 0, None), (2, 7, 'b'), (3, 4, None),
                (4, 3, None), (5, 6, None), (6, 5, None), (7, 2, 'b')]),

        Tile(5, [(0, 7, None), (1, 3, None), (2, None, 'y'), (3, 1, None),
                (4, 5, None), (5, 4, None), (6, None, 'y'), (7, 0, None)]),

        Tile(6, [(0, 1, None), (1, 0, None), (2, 5, None), (3, 6, 'b'),
                (4, 7, None), (5, 2, None), (6, 3, 'b'), (7, 4, None)]),
    ]

    return tiles

TILES = createTiles()



class Level:
    def __init__(self):
        self.board_ =  [ [ None for i in range(7) ] for j in range(7) ]
        self.socket_list_ = []

    def getSocketsCount(self):
        return len(self.socket_list_)

    def setSocket(self, x, y, socket):
        self.board_[x][y] = socket
        self.socket_list_.append((x, y))

    def getSocketById(self, idx):
        coords = self.socket_list_[idx]
        return self.getSocket(coords[0], coords[1])

    def getSocket(self, x, y):
        try:
            return self.board_[x][y]
        except IndexError:
            return None

    def constructPath(self, entrance_id, socket_id):
        socket = self.getSocketById(socket_id)
        if (socket is None):
            return None

        entrance = socket.getEntrance(entrance_id)
        if entrance is None or isinstance(entrance, EntranceConnection):
            return None

        coords = self.socket_list_[socket_id]
        path = self.traverse(entrance_id, coords[0], coords[1])
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
        else:
            # Special yin yang case, path ends in the middle of a tile
            pass

        return [connection] + path

class Level3(Level):
    def __init__(self):
        super().__init__()

        self.setSocket(0, 0, Socket([
            None, None,
            None, EntranceCountTiles(2),
            EntranceConnection(), EntranceConnection(),
            None, EntrancePagoda()
            ]))

        self.setSocket(0, 1, Socket([
            EntranceConnection(), EntranceConnection(),
            None, EntrancePagoda(),
            None, None,
            None, None
        ]))


class EntranceCountBridges:
    def __init__(self, count):
        self.count_ = count

    def check(self, path):
        return len(filter(lambda p: p(2) == 'b', path)) == self.count_

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

def setState(level, state):
    for s in range(len(state)):
        tile = TILES[state[s][0]]
        tile.rotate(state[s][1])

        level.getSocketById(s).setTile(tile)

    return level


def nextTilesState(level):
    print("sockets count ", level.getSocketsCount())

    candidates = set(range(7))
    for a in candidates:
        level.getSocketById(0).setTile(TILES[a])

        for cw_a in range(4):
            TILES[a].rotate(cw_a)

            for b in candidates - {a}:
                for cw_b in range(4):
                    TILES[b].rotate(cw_b)
                    level.getSocketById(1).setTile(TILES[b])
                    yield level

                TILES[b].rotate(None)
            TILES[a].rotate(None)

def validateSocket(level, socket_id):
    for entrance_id in range(8):
        path = level.constructPath(entrance_id, socket_id)

        if (path is not None and not socket.getEntrance(entrance_id).check(path)):
            return False

    return True

if __name__ == "__main__":

    l3 = Level3()

    cnt = 0
    for state in nextTilesState(l3):
        cnt = cnt + 1

        state = setState(l3, [(5, 2), (1, 3)])
        exit(0)

        if state.getSocketById(0).tile_.id_ == 5 and \
            state.getSocketById(0).tile_.rotation_ == 2 and \
            state.getSocketById(1).tile_.id_ == 1 and \
            state.getSocketById(1).tile_.rotation_ == 3:
            print("OK setup iteration ", cnt)


        found = True
        for socket_id in range(l3.getSocketsCount()):
            socket = l3.getSocketById(socket_id)

            if not validateSocket(l3, socket_id):
                found = False
                break

        if (found):
            print("Found solution! After ", cnt, " iterations")
            for socket_id in range(l3.getSocketsCount()):
                print(l3.getSocketById(socket_id).tile_)
            exit(0)

    print("No solution found, after ", cnt, " iterations")




    # l3.board_[0][0].setTile(tiles[6])
    # l3.board_[0][1].setTile(tiles[5])

    # l3.constructPath(7, 0, 0)