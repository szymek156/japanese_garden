from PIL import Image, ImageColor

TILE_GRAPHIC = []
IMG_DIM = 715//4

class Gui:
    def __init__(self):
        self.loadTiles()
        self.board_ = None

    def loadTiles(self):
        for i in range(0,7):
            im = Image.open("tiles/{}.png".format(i))

            im_resized = im.resize((IMG_DIM, IMG_DIM))

            TILE_GRAPHIC.append(im_resized)


    def showLevel(self, level):
        max_w = max([x for (x,y) in level.socket_coordinates_]) + 1
        max_h = max([y for (x,y) in level.socket_coordinates_]) + 1

        self.board_ = Image.new("RGBA", (max_w * IMG_DIM, max_h * IMG_DIM),
            color=ImageColor.getcolor('black', 'RGBA'))

        for (x, y) in level.socket_coordinates_:
            sock = level.getSocket(x, y)

            self.putTile(x, y, sock.tile_)

        self.board_.save("tiles/board.png")
        self.board_.show()


    def putTile(self, x, y, tile):
        t_img = TILE_GRAPHIC[tile.id_].copy()

        t_img = t_img.rotate(-90 * tile.rotation_)

        self.board_.paste(t_img, (x * IMG_DIM, y * IMG_DIM))
