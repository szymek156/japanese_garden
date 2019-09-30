from math import floor
from functools import reduce
from tqdm import tqdm
from tile import TILES
from level import SetLevelState, Level50
import os
import multiprocessing as mp
import random


DISABLE_PROGRESS = True

def worker(job_info, level, queue):
    NaiveSolver(level, job_info=job_info, queue=queue).solve()

class ParallelSolver:
    def __init__(self, level, jobs=1, debug=False):
        self.level_ = level
        self.jobs_ = jobs
        self.debug_ = debug

    def solve_process(self):
        manager = mp.Manager()
        queue = mp.Queue()
        # queue = manager.Queue()
        procs = [mp.Process(target=worker, args=((self.jobs_, i), self.level_, queue)) for i in range(self.jobs_)]

        i = 0
        for p in procs:
            p.start()
            # os.system("taskset -p -c %d %d &>/dev/null" % ((i % os.cpu_count()), p.pid))
            i = i + 1

        print("Wait on a queue...")
        result = queue.get()

        for p in procs:
            p.terminate()

        print("Result from worker: ", result)

        return result

    def solve_pool(self):
        with mp.Pool(processes=self.jobs_) as pool:
            manager = mp.Manager()
            queue = manager.Queue()

            _ = [pool.apply_async(worker, ((self.jobs_, i), self.level_, queue)) for i in range(self.jobs_)]

            print("Wait on a queue...")
            result = queue.get()
            print("Result from worker: ", result)

            return result


class NaiveSolver:
    def __init__(self, level, job_info=(1, 1), queue=None, debug=False):
        self.level_ = level
        self.jobs_, self.job_id_ = job_info
        self.queue_ = queue
        self.debug_ = debug

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

        # Get modulos
        magic = [(i, 4) for i in range(len(TILES), 0 , -1)]

        # Get only those which are gonna be used for given level
        magic = magic[0:sockets]

        # Flatten iterable
        magic = list(sum(magic, ()))

        search_space = reduce(lambda x, y: x * y, magic)

        job_range = search_space // self.jobs_
        range_start = job_range * self.job_id_

        if (self.job_id_ + 1 == self.jobs_):
            # Last worker gets states to the very end
            range_stop = search_space
        else:
            range_stop = range_start + job_range

        # print("worker #%s range: [%d:%d]" % (self.job_id_, range_start, range_stop))

        tile_offsets = [0] * sockets

        # disable = True
        # if self.job_id_ == 0:
        #     disable = False

        for idx in tqdm(range(range_start, range_stop), position=self.job_id_, disable=DISABLE_PROGRESS):
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
            traversal = self.level_.constructPath(entrance_id, socket_id)

            if (traversal is not None and not socket.getEntrance(entrance_id).check(traversal)):
                if (self.debug_):
                     breakpoint()
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
        if self.debug_:
            print("Solver in debug mode")
            SetLevelState(self.level_, self.level_.getSolution())
            found = self._validateLevel()
            print("Found solution: ", found)
            return

        cnt = 0
        for state in self._getNextState():
            cnt = cnt + 1

            SetLevelState(self.level_, state)

            found = self._validateLevel()

            if (found):
                print("Found solution! After ", cnt, " iterations")
                print("State: ", state)
                if self.queue_:
                    self.queue_.put(state)
                return True

        print("No solution found, after ", cnt, " iterations")
        return False

class RandomNaiveSolver(NaiveSolver):
    def __init__(self, level, job_info=(1, 1), queue=None, debug=False):
        super().__init__(level, job_info, queue, debug)

    def _getNextState(self):
        """ As Naive solver, but pickup idx at random """

        sockets = self.level_.getSocketsCount()

        # Get modulos
        magic = [(i, 4) for i in range(len(TILES), 0 , -1)]

        # Get only those which are gonna be used for given level
        magic = magic[0:sockets]

        # Flatten iterable
        magic = list(sum(magic, ()))

        search_space = reduce(lambda x, y: x * y, magic)

        job_range = search_space // self.jobs_
        range_start = job_range * self.job_id_

        if (self.job_id_ + 1 == self.jobs_):
            # Last worker gets states to the very end
            range_stop = search_space
        else:
            range_stop = range_start + job_range

        # print("worker #%s range: [%d:%d]" % (self.job_id_, range_start, range_stop))

        tile_offsets = [0] * sockets

        # disable = True
        # if self.job_id_ == 0:
        #     disable = False

        visited = set()

        with tqdm(total=job_range, position=self.job_id_, disable=DISABLE_PROGRESS) as pbar:
            while True:
                idx = random.randint(range_start, range_stop)

                if (idx in visited):
                    continue
                visited.add(idx)
                pbar.update()

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

