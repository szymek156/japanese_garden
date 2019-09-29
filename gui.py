from PIL import Image, ImageColor, ImageDraw, ImageFont

from entrance import *

TILE_GRAPHIC = []
TILE_DIM = 715//4

ENTRANCE_GRAPHIC = {}
ENTRANCE_DIM = 190//4
ENTRANCE_NAME = ["red", "blue", "yellow", "purple", "count-tiles", "pagoda", "yin-yang", "bridge"]

class Gui:
    """ Quick and Dirty gui spend less than day on it, don't expect to be pretty """
    def __init__(self, level):
        self.loadTiles()
        self.loadEntrances()

        self.max_w_ = max([x for (x, y) in level.socket_coordinates_]) + 1
        self.max_h_ = max([y for (x, y) in level.socket_coordinates_]) + 1

        self.margin_ = 100

        self.board_ = Image.new("RGBA", (self.max_w_ * TILE_DIM + self.margin_,
            self.max_h_ * TILE_DIM + self.margin_),
            color=ImageColor.getcolor('green', 'RGBA'))

        self.level_ = level


    def loadTiles(self):
        for i in range(0,7):
            im = Image.open("tiles/{}.png".format(i))

            im_resized = im.resize((TILE_DIM, TILE_DIM))

            TILE_GRAPHIC.append(im_resized)

    def loadEntrances(self):
        for ent in ENTRANCE_NAME:
            im = Image.open("tiles/entrances/{}.png".format(ent))

            im_resized = im.resize((ENTRANCE_DIM, ENTRANCE_DIM))

            ENTRANCE_GRAPHIC[ent] = im_resized

    def showBoard(self):
        for (x, y) in self.level_.socket_coordinates_:
            sock = self.level_.getSocket(x, y)

            for entrance_id in range(0, 8):
                entrance = sock.getEntrance(entrance_id)

                if (entrance):
                    self.putEntrance(x, y, entrance_id, entrance)

        self.board_.save("tiles/board.png")
        # self.board_.show()

    def showLevel(self):
        self.showBoard()

        for (x, y) in self.level_.socket_coordinates_:
            sock = self.level_.getSocket(x, y)

            self.putTile(x, y, sock.tile_)

        self.board_.save("tiles/board_and_solution.png")
        self.board_.show()


    def putTile(self, x, y, tile):
        t_img = TILE_GRAPHIC[tile.id_].copy()

        t_img = t_img.rotate(-90 * tile.rotation_)

        offset = self.margin_ // 2

        self.board_.paste(t_img, (x * TILE_DIM +  offset, y * TILE_DIM + offset))

    def putEntrance(self, x, y, entrance_id, entrance):
        e_img = None
        fnt = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf', 24)

        if type(entrance) is EntranceCountBridges:
            e_img = ENTRANCE_GRAPHIC["bridge"].copy()
            d = ImageDraw.Draw(e_img)
            d.text((17,12), "%d" % entrance.count_, font=fnt, fill=(255, 255, 255))

        elif type(entrance) is EntranceColor:
            # TODO: distinguish colors
            e_img = ENTRANCE_GRAPHIC["red"].copy()

        elif type(entrance) is EntrancePagoda:
            e_img = ENTRANCE_GRAPHIC["pagoda"].copy()

        elif type(entrance) is EntranceCountTiles:
            e_img = ENTRANCE_GRAPHIC["count-tiles"].copy()
            d = ImageDraw.Draw(e_img)
            d.text((17,12), "%d" % entrance.count_, font=fnt, fill=(255, 255, 255))

        elif type(entrance) is EntranceYinYang:
            e_img = ENTRANCE_GRAPHIC["yin-yang"].copy()

        elif type(entrance) is EntranceConnection:
            # TODO: add connection graphic?
            # e_img = ENTRANCE_GRAPHIC["purple"].copy()
            return
        else:
            raise RuntimeError("Unknown entrance type %s" % type(entrance))

        offset_x = 0
        offset_y = 0

        if entrance_id == 0:
            offset_x = 70
        elif entrance_id == 1:
            offset_x = 170
        elif entrance_id == 2:
            offset_x = 230
            offset_y = 70
        elif entrance_id == 3:
            offset_x = 230
            offset_y = 170
        elif entrance_id == 4:
            offset_x = 170
            offset_y = 230
        elif entrance_id == 5:
            offset_x = 70
            offset_y = 230
        elif entrance_id == 6:
            offset_x = 0
            offset_y = 170
        elif entrance_id == 7:
            offset_x = 0
            offset_y = 70


        self.board_.paste(e_img, (x * TILE_DIM +  offset_x, y * TILE_DIM + offset_y))

