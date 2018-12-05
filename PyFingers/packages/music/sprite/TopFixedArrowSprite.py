from packages.music.sprite.Sprite import Sprite


class TopFixedArrowSprite(Sprite):

    def __init__(self, imgs, x=0, y=0, z=0, w=0, h=0):
        super().__init__(imgs, x, y, z, w, h)
        assert len(imgs) == 2
        self.clicked = False

    def update(self):
        pass

    def setClicked(self, clicked):
        self.clicked = clicked

    def nextImage(self):
        return self.imgs[1] if self.clicked else self.imgs[0]



