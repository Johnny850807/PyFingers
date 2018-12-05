from packages.music.sprite.Sprite import Sprite


class ArrowSprite(Sprite):
    def __init__(self, imgs, numOfArrow=0, x=0, y=0, z=0, w=0, h=0):
        super().__init__(imgs, x, y, z, w, h)
        self.numOfArrow = numOfArrow

    def update(self):
        self.y -= 5
        if self.y + self.h < 0:
            self.context.onSpriteOutOfBound(self)

