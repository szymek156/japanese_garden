class Socket:
    def __init__(self, entrances):
        """ Entrances starts from top left and continue clockwise:
              0 1
            7     2
            6     3
              4 5
        """
        self.entrances_ = entrances
        self.tile_ = None

    def setTile(self, tile):
        self.tile_ = tile

    def getEntrance(self, entrance_id):
        try:
            return self.entrances_[entrance_id]
        except IndexError:
            return None


    def getConnection(self, entrance_id):
        return self.tile_.getConnection(entrance_id)