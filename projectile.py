class Projectile:
    def __init__(self, x, y, image, left, right):
        self.x = x
        self.y = y
        self.image = image
        self.left = left
        self.right = right

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, dx, dy=0):
        self.x += dx
        self.y += dy
        self.bottom = self.y + self.image.get_height()
