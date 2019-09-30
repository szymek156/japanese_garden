import level
import time
# import gui
from solver import NaiveSolver, ParallelSolver

if __name__ == "__main__":

    lvls = [level.Level3(), level.Level13(),
            level.Level22(), level.Level26(),
            level.Level27(), level.Level29(),
            level.Level35(), level.Level50()]

    jobs = 3
    # for lvl in  lvls:
    # #     # level.SetLevelState(lvl, lvl.getSolution())
    # #     # gui.Gui(lvl).showLevel()
    #     print("######################################################################")
    #     print("solve_process Level: ", lvl)

    #     start_time = time.time()
    #     state = ParallelSolver(lvl, jobs=jobs).solve_process()
    #     print("--- %s seconds ---" % (time.time() - start_time))

    #     print("solve_pool Level: ", lvl)
    #     start_time = time.time()
    #     state = ParallelSolver(lvl, jobs=jobs).solve_pool()
    #     print("--- %s seconds ---" % (time.time() - start_time))

    #     # if (state):
    #     #     level.SetLevelState(lvl, state)
    #     #     gui.Gui(lvl).showLevel()

    sum = 0
    for iter in range(1, 20):
        start_time = time.time()
        ParallelSolver(level.Level35(), jobs=jobs).solve_process()
        diff = time.time() - start_time

        sum = sum + diff
        print("--- %s seconds, %s mean ---" % (diff, sum/iter))


    # ParallelSolver(level.Level29(), jobs=jobs).solve_pool()
