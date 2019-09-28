from tile import TILES
from math import floor
from functools import reduce
from progressbar import progressbar

class NaiveSolver:
    def __init__(self, level):
        self.level_ = level

    def _setLevelState(self, state):
        for s in range(len(state)):
            tile = TILES[state[s][0]]
            tile.rotate(None)
            tile.rotate(state[s][1])

            self.level_.getSocketById(s).setTile(tile)

    def _getNextState(self):
        """ So there are several sockets on each level, there can be 1, 3, even 7.
            To each socket can be assign one of 7 tiles, so for first socket
            there are 7 possibilities, for second 6 for third 5 and so on.
            Each socket can rotate, there are 4 rotations, this means each socket
            has 4 more possibilities, so total space: 7*4*6*4*5*4... => 7*6*..*N * 4**N
            Where N is number of sockets. To generate each possibility it's worth
            to note it is like a binary counter, but instead of modulo 2 on every
            position, there are modulos like 7,4,6,4,... Also number of digits is
            not constrained to have only 0 and 1, but it differs depending on
            position maybe reading the code gives better understanding. To get a
            feeling how it works it's worth to create an excel sheet and
            generate states having given natural number """

        sockets = self.level_.getSocketsCount()
        print("sockets count ", sockets)

        # Get modulos
        magic = [(i, 4) for i in range(len(TILES), 0 ,-1)]

        # Get only those which are gonna be used for given level
        magic = magic[0:sockets]

        # Flatten iterable
        magic = list(sum(magic, ()))

        search_space = reduce(lambda x, y: x * y, magic)

        print("search space ", search_space)
        tile_offsets = [0] * sockets

        for idx in progressbar(range(search_space)):
            state = []
            free_tiles = [i for i in range(0, len(TILES))]

            for i in range(sockets):
                s_field = i * 2

                s_divider = reduce(lambda x, y: x * y, magic[s_field+1:], 1)
                s_modulo = magic[s_field]
                tile_idx = floor(idx/s_divider) % s_modulo

                r_field = s_field + 1
                r_divider = reduce(lambda x, y: x * y, magic[r_field+1:], 1)
                r_modulo = magic[r_field]
                rotation = floor(idx/r_divider) % r_modulo

                tile = free_tiles.pop(tile_idx)

                state.append((tile, rotation))

            # if ((idx % 10000) == 0):
            #     print("State #", idx, " ", state)

            yield state

    def _validateSocket(self, socket_id):
        socket = self.level_.getSocketById(socket_id)

        for entrance_id in range(8):
            path = self.level_.constructPath(entrance_id, socket_id)

            if (path is not None and not socket.getEntrance(entrance_id).check(path)):
                return False

        return True

    def _validateLevel(self):
        found = True
        for socket_id in range(self.level_.getSocketsCount()):
            if not self._validateSocket(socket_id):
                found = False
                break

        return found

    def solve(self):
        cnt = 0
        for state in self._getNextState():
            cnt = cnt + 1

            self._setLevelState(state)

            found = self._validateLevel()

            if (found):
                print("Found solution! After ", cnt, " iterations")
                print("State: ", state)
                return True

        print("No solution found, after ", cnt, " iterations")
        return False
