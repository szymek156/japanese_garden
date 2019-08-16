class Tile:
    def __init__(self, id, paths):
        self.rotation_ = 0
        self.paths_ = paths
        self.id_ = id

    def rotate(self, cw):
        if (cw == None):
            self.rotate(4 - self.rotation_)
        else:
            cw = cw % 4

            self.rotation_ = (self.rotation_ + cw) % 4

            self.paths_ = list(map(lambda p: (self.mapRotation(p[0], cw), self.mapRotation(p[1], cw), p[2]), self.paths_))

            split = len(self.paths_) - ((cw % 4) * 2)
            self.paths_ = self.paths_[split:] + self.paths_[:split]


    def mapRotation(self, entrance_id, cw):
        if (entrance_id is None):
            return None

        return (entrance_id + (cw * 2)) % 8

    def getConnection(self, entrance_id):
        return self.paths_[entrance_id]

    def __repr__(self):
        return "(" + str(self.id_) + ", " + str(self.rotation_) + ")"

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