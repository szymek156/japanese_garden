
import level
import gui
from solver import NaiveSolver


# def nextTilesState(level):
#     print("sockets count ", level.getSocketsCount())

#     candidates = set(range(7))
#     for a in candidates:
#         level.getSocketById(0).setTile(TILES[a])

#         for _ in range(4):
#             for b in candidates - {a}:
#                 for _ in range(4):
#                     level.getSocketById(1).setTile(TILES[b])
#                     yield level
#                     TILES[b].rotate(1)
#                 TILES[b].rotate(None)

#             TILES[a].rotate(1)

#         TILES[a].rotate(None)



if __name__ == "__main__":
    lvl = level.Level50()

    level.SetLevelState(lvl, lvl.getSolution())
    gui.Gui(lvl).showLevel()

    # if (NaiveSolver(lvl).solve()):
    #     pass
    #     # gui.Gui().showLevel(level)

