from tile import TILES
from level import Level3


def setState(level, state):
    for s in range(len(state)):
        tile = TILES[state[s][0]]
        tile.rotate(None)
        tile.rotate(state[s][1])

        level.getSocketById(s).setTile(tile)

    return level


def nextTilesState(level):
    print("sockets count ", level.getSocketsCount())

    candidates = set(range(7))
    for a in candidates:
        level.getSocketById(0).setTile(TILES[a])

        for _ in range(4):
            TILES[a].rotate(1)

            for b in candidates - {a}:
                for _ in range(4):
                    TILES[b].rotate(1)
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

            if (cnt == 3):
                print (27)

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