import unittest
import copy

from tile import Tile

class TestTile(unittest.TestCase):
    def test_rotation1(self):
        tile = Tile(0, [(0, 5, 'b'), (1, 6, None), (2, 7, 'b'), (3, 4, None),
                    (4, 3, None), (5, 0, 'b'), (6, 1, None), (7, 2, 'b')])


        tilecw = Tile(0, [(0, 3, None), (1, 4, 'b'), (2, 7, 'b'), (3, 0, None),
                    (4, 1, 'b'), (5, 6, None), (6, 5, None), (7, 2, 'b') ])
        tilecw.rotation_ = 1

        tile_not_rotated = copy.deepcopy(tile)

        tile.rotate(1)

        self.assertEqual(tile.paths_, tilecw.paths_)

        tilecw.rotate(None)

        self.assertEqual(tilecw.paths_, tile_not_rotated.paths_)

    def test_rotation_reset(self):
        tile = Tile(0, [(0, 5, 'b'), (1, 6, None), (2, 7, 'b'), (3, 4, None),
                    (4, 3, None), (5, 0, 'b'), (6, 1, None), (7, 2, 'b')])

        tile_not_rotated = copy.deepcopy(tile)

        tile.rotate(1)
        tile.rotate(1)

        tile.rotate(1)
        tile.rotate(None)
        tile.rotate(1)
        tile.rotate(1)

        tile.rotate(None)


        self.assertEqual(tile.rotation_, tile_not_rotated.rotation_)
        self.assertEqual(tile.paths_, tile_not_rotated.paths_)

    # def test_rotation2(self):
    #     tile = Tile(0, [(0, 5, 'b'), (1, 6, None), (2, 7, 'b'), (3, 4, None),
    #                 (4, 3, None), (5, 0, 'b'), (6, 1, None), (7, 2, 'b')])

    #     tilecw = Tile(0, [(4, 3, None), (5, 0, 'b'), (6, 1, None), (7, 2, 'b'),
    #                 (0, 5, 'b'), (1, 6, None), (2, 7, 'b'), (3, 4, None)])

    #     tilecw.rotation_ = 2


    #     tile.rotate(2)

    #     self.assertEqual(tile.paths_, tilecw.paths_)


if __name__ == '__main__':
    unittest.main()