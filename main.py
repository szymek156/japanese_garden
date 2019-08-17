from tile import TILES
from level import Level3
from math import floor
from functools import reduce
import time
import gui

def setState(level, state):
    for s in range(len(state)):
        tile = TILES[state[s][0]]
        tile.rotate(None)
        tile.rotate(state[s][1])

        level.getSocketById(s).setTile(tile)

    return level

def getNextState(level):
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

    sockets = level.getSocketsCount()
    print("sockets count ", sockets)

    # Get modulos
    magic = [(i, 4) for i in range(7, 0 ,-1)]

    # Get only those which are gonna be used for given level
    magic = magic[0:sockets]

    # Flatten iterable
    magic = list(sum(magic, ()))

    search_space = reduce(lambda x, y: x * y, magic)

    print("search space ", search_space)
    tile_offsets = [0] * sockets

    for idx in range(search_space):
        state = []
        used_tiles = []

        for i in range(sockets):
            s_field = i * 2

            s_divider = reduce(lambda x, y: x * y, magic[s_field+1:], 1)
            s_modulo = magic[s_field]
            tile = floor(idx/s_divider) % s_modulo

            r_field = s_field + 1
            r_divider = reduce(lambda x, y: x * y, magic[r_field+1:], 1)
            r_modulo = magic[r_field]
            rotation = floor(idx/r_divider) % r_modulo

            while tile + tile_offsets[i] in used_tiles:
                tile_offsets[i] = tile_offsets[i] + 1

            if ((tile + tile_offsets[i]) % len(TILES) == 0):
                tile_offsets[i] = 0

            used_tiles.append(tile + tile_offsets[i])

            state.append((tile + tile_offsets[i], rotation))

        if ((idx % 100000) == 0):
            print("State #", idx, " ", state)

        yield state



def nextTilesState(level):
    print("sockets count ", level.getSocketsCount())

    candidates = set(range(7))
    for a in candidates:
        level.getSocketById(0).setTile(TILES[a])

        for _ in range(4):
            for b in candidates - {a}:
                for _ in range(4):
                    level.getSocketById(1).setTile(TILES[b])
                    yield level
                    TILES[b].rotate(1)
                TILES[b].rotate(None)

            TILES[a].rotate(1)

        TILES[a].rotate(None)

def validateSocket(level, socket_id):
    for entrance_id in range(8):
        path = level.constructPath(entrance_id, socket_id)

        if (path is not None and not socket.getEntrance(entrance_id).check(path)):
            return False

    return True

if __name__ == "__main__":

    l3 = Level3()

    # start = time.time()

    # for _ in getNextState(l3):
    #     pass

    # print (time.time() - start)

    # exit(1)

    # idx = 0
    # for a, b in zip(getNextState(l3), nextTilesState(l3)):
    #     list_b = []
    #     for socket_id in range(b.getSocketsCount()):
    #         list_b.append((b.getSocketById(socket_id).tile_.id_ , b.getSocketById(socket_id).tile_.rotation_))

    #     print(a)
    #     print(list_b)
    #     print("----- ", idx, " -----")
    #     idx = idx + 1

    #     if a != list_b:
    #         print("THEY DIFFER")
    #         break

    # exit(1)

    cnt = 0
    for state in  nextTilesState(l3):
        cnt = cnt + 1

        if l3.getSocketById(0).tile_.id_ == 5 and \
            l3.getSocketById(0).tile_.rotation_ == 2 and \
            l3.getSocketById(1).tile_.id_ == 1 and \
            l3.getSocketById(1).tile_.rotation_ == 3:
            print("OK setup iteration ", cnt)

        print (cnt)
        for socket_id in range(l3.getSocketsCount()):
            print(l3.getSocketById(socket_id).tile_)
        print ("---------------------")

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

            gui.Gui().showLevel(l3)
            exit(0)

    print("No solution found, after ", cnt, " iterations")




    # l3.board_[0][0].setTile(tiles[6])
    # l3.board_[0][1].setTile(tiles[5])

    # l3.constructPath(7, 0, 0)