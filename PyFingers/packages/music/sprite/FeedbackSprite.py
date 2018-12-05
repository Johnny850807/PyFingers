from packages.music.sprite.Sprite import Sprite


class FeedbackSprite(Sprite):

    def __init__(self, imgs, maxY=0, x=0, y=0, z=0, w=0, h=0):
        super().__init__(imgs, x, y, z, w, h)
        self.updateCount = 0
        self.maxY = maxY
        self.y = self.maxY + 100

    def update(self):
        self.updateCount += 1
        self.y = self.y - 4 if self.y > self.maxY else self.y
        if self.updateCount >= 200:
            self.y = -100  # make it disappeared
