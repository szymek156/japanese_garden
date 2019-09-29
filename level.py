from sock import Socket
from entrance import *
from tile import TILES

def SetLevelState(level, state):
    for s in range(len(state)):
        tile = TILES[state[s][0]]
        tile.rotate(None)
        tile.rotate(state[s][1])

        level.getSocketById(s).setTile(tile)

class Level:
    def __init__(self):
        self.board_ =  [ [ None for i in range(7) ] for j in range(7) ]
        self.socket_coordinates_ = []

    def getSocketsCount(self):
        return len(self.socket_coordinates_)

    def setSocket(self, x, y, socket):
        coordinate = (x, y)

        if (coordinate in self.socket_coordinates_):
            raise AttributeError("Coordinate %s already exists" % (coordinate,))

        self.board_[x][y] = socket
        self.socket_coordinates_.append(coordinate)

    def getSocketById(self, idx):
        coords = self.socket_coordinates_[idx]
        return self.getSocket(coords[0], coords[1])

    def getSocket(self, x, y):
        try:
            return self.board_[x][y]
        except IndexError:
            return None

    def getSolution(self):
        raise NotImplementedError("getSolution is not overridden")

    def constructPath(self, entrance_id, socket_id):
        socket = self.getSocketById(socket_id)
        if (socket is None):
            return None

        entrance = socket.getEntrance(entrance_id)
        if entrance is None or isinstance(entrance, EntranceConnection):
            return None

        coords = self.socket_coordinates_[socket_id]
        path = self._traverse(entrance_id, coords[0], coords[1])
        return path

    # def _traverse(self, entrance_id, x, y):
    #     socket = self.getSocket(x, y)
    #     if (socket is None):
    #         return []

    #     connection = socket.getConnection(entrance_id)

    #     path = []
    #     if (connection[1] in [0, 1]): # Go north
    #         path = self._traverse(5 - connection[1], x, y - 1)
    #     elif (connection[1] in [2, 3]): # Go east
    #         path = self._traverse(9 - connection[1], x + 1, y)
    #     elif (connection[1] in [4, 5]): # Go south
    #         path = self._traverse(5 - connection[1], x, y + 1)
    #     elif (connection[1] in [6, 7]): # Go west
    #         path = self._traverse(9 - connection[1], x - 1, y)
    #     else:
    #         # Special yin yang case, path ends in the middle of a tile
    #         pass

    #     return [connection] + path

    def _traverse(self, entrance_id, x, y):
        socket = self.getSocket(x, y)
        if (socket is None):
            return [None, []]

        connection = socket.getConnection(entrance_id)

        stop = None
        path = []

        if (connection[1] in [0, 1]): # Go north
            stop, path = self._traverse(5 - connection[1], x, y - 1)
        elif (connection[1] in [2, 3]): # Go east
            stop, path = self._traverse(9 - connection[1], x + 1, y)
        elif (connection[1] in [4, 5]): # Go south
            stop, path = self._traverse(5 - connection[1], x, y + 1)
        elif (connection[1] in [6, 7]): # Go west
            stop, path = self._traverse(9 - connection[1], x - 1, y)
        else:
            # Special yin yang case, path ends in the middle of a tile
            pass

        traversal = [None, []]
        if (not path):
            # This is last tile, get ending entrance
            if (connection[1] is not None):
                traversal[0] = socket.getEntrance(connection[1])
            # if connection[1] is None, this is yin-yang tile
        else:
            # This is tile in the middle of traversal, bubble up ending entrance
            traversal[0] = stop

        # Erlange path by connection on current tile
        traversal[1] = [connection] + path

        return traversal

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

    def getSolution(self):
        return [(5, 2), (1, 3)]


class Level13(Level):
    def __init__(self):
        super().__init__()

        self.setSocket(1, 0, Socket([
            None, EntranceColor(EntranceColor.YELLOW),
            None, EntranceColor(EntranceColor.RED),
            EntranceConnection(), EntranceConnection(),
            EntranceColor(EntranceColor.RED), None
        ]))

        self.setSocket(0, 1, Socket([
            EntranceColor(EntranceColor.PURPLE), None,
            EntranceConnection(), EntranceConnection(),
            EntranceColor(EntranceColor.BLUE), EntranceColor(EntranceColor.YELLOW),
            None, EntranceColor(EntranceColor.BLUE)
        ]))

        self.setSocket(1, 1, Socket([
            EntranceConnection(), EntranceConnection(),
            EntranceColor(EntranceColor.PURPLE), None,
            None, None,
            EntranceConnection(), EntranceConnection()
        ]))

    def getSolution(self):
        return [(0, 2), (3, 2), (6, 2)]

class Level35(Level):
    def __init__(self):
        super().__init__()

        self.setSocket(0, 0, Socket([
            None, None,
            None, None,
            EntranceConnection(), EntranceConnection(),
            EntrancePagoda(), None
            ]))

        self.setSocket(2, 0, Socket([
            None, None,
            None, EntrancePagoda(),
            EntranceConnection(), EntranceConnection(),
            None, None
            ]))

        self.setSocket(0, 1, Socket([
            EntranceConnection(), EntranceConnection(),
            EntranceConnection(), EntranceConnection(),
            None, None,
            None, None
            ]))

        self.setSocket(1, 1, Socket([
            None, None,
            EntranceConnection(), EntranceConnection(),
            EntranceCountBridges(1), EntranceYinYang(),
            EntranceConnection(), EntranceConnection()
            ]))

        self.setSocket(2, 1, Socket([
            EntranceConnection(), EntranceConnection(),
            None, None,
            None, EntranceCountBridges(2),
            EntranceConnection(), EntranceConnection()
            ]))

    def getSolution(self):
        return [(5, 3), (4, 3), (1, 3), (2, 3), (0, 0)]

class Level50(Level):
    def __init__(self):
        super().__init__()

        self.setSocket(0, 0, Socket([
            EntranceCountTiles(2), None,
            EntranceConnection(), EntranceConnection(),
            EntranceConnection(), EntranceConnection(),
            EntrancePagoda(), None
            ]))

        self.setSocket(1, 0, Socket([
            EntranceCountTiles(2), EntranceCountTiles(2),
            EntranceConnection(), EntranceConnection(),
            EntranceConnection(), EntranceConnection(),
            EntranceConnection(), EntranceConnection(),
            ]))

        self.setSocket(2, 0, Socket([
            None, None,
            EntranceCountTiles(2), EntranceCountTiles(2),
            EntranceConnection(), EntranceConnection(),
            EntranceConnection(), EntranceConnection(),
            ]))

        self.setSocket(0, 1, Socket([
            EntranceConnection(), EntranceConnection(),
            EntranceConnection(), EntranceConnection(),
            None, None,
            None, None
            ]))

        self.setSocket(1, 1, Socket([
            EntranceConnection(), EntranceConnection(),
            EntranceConnection(), EntranceConnection(),
            EntranceCountTiles(2), EntranceCountTiles(11),
            EntranceConnection(), EntranceConnection(),
            ]))

        self.setSocket(2, 1, Socket([
            EntranceConnection(), EntranceConnection(),
            None, EntranceCountTiles(2),
            EntranceCountTiles(2), None,
            EntranceConnection(), EntranceConnection(),
            ]))

    def getSolution(self):
        return [(3, 0), (6, 2), (2, 3), (1, 3), (4, 3), (0, 2)]