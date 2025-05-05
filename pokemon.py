class Pokemon:
    def __init__(self, images, x, y):
        self.images = images
        self.x = x
        self.y = y
        self.width = images[0].get_width()
        self.height = images[0].get_height()
        self.right = True
        self.left = False
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    @property
    def bottom(self):
        return self.y + self.height

    @bottom.setter
    def bottom(self, value):
        self.y = value - self.height
