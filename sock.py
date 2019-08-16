class Socket:
    def __init__(self, entrances):
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