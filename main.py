import level
import time
# import gui
from solver import NaiveSolver, ParallelSolver


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

    lvls = [level.Level3(), level.Level13(),
            level.Level22(), level.Level26(),
            level.Level27(), level.Level29(),
            level.Level35(), level.Level50()]

    jobs = 32
    for lvl in  lvls:
    #     # level.SetLevelState(lvl, lvl.getSolution())
    #     # gui.Gui(lvl).showLevel()
        print("######################################################################")
        print("solve_process Level: ", lvl)

        start_time = time.time()
        state = ParallelSolver(lvl, jobs=jobs).solve_process()
        print("--- %s seconds ---" % (time.time() - start_time))

        print("solve_pool Level: ", lvl)
        start_time = time.time()
        state = ParallelSolver(lvl, jobs=jobs).solve_pool()
        print("--- %s seconds ---" % (time.time() - start_time))

        # if (state):
        #     level.SetLevelState(lvl, state)
        #     gui.Gui(lvl).showLevel()

    # ParallelSolver(level.Level29(), jobs=jobs).solve_process()
    # ParallelSolver(level.Level29(), jobs=jobs).solve_pool()
