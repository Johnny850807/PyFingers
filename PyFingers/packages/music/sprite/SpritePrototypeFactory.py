from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, qRgb

from packages.MyUtils import Path
from packages.music.sprite.ArrowSprite import ArrowSprite
from packages.music.sprite.FeedbackSprite import FeedbackSprite
from packages.music.sprite.Sprite import Sprite
from packages.music.sprite.TopFixedArrowSprite import TopFixedArrowSprite


class SpritePrototypeFactory(object):
    # TODO Finish singleton
    # TODO Finish prototyping
    PLAYER_1, PLAYER_2 = (1, 2)
    ARROW_UP, ARROW_DOWN, ARROW_LEFT, ARROW_RIGHT = (1, 2, 3, 4)
    FEEDBACK_PERFECT, FEEDBACK_GOOD, FEEDBACK_BAD, FEEDBACK_MISS = (5, 6, 7, 8)
    TOP_FIXED_ARROWS = (9, 10, 11, 12)
    TOP_ARROW_LEFT, TOP_ARROW_DOWN, TOP_ARROW_UP, TOP_ARROW_RIGHT = TOP_FIXED_ARROWS
    PUNCH_EFFECT = 13

    def __init__(self):
        self.__sprites = dict()
        self.screenWidth = None
        self.screenHeight = None
        self.arrowFragmentWidth = None
        self.levelFeedbackY = None
        self.levelFeedbackWidth = 234
        self.levelFeedbackHeight = 71
        self.arrowSize = 88  # same width and height
        self.topFixedArrowY = 40  # fixed y where the top

    def prepare(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.arrowFragmentWidth = screenWidth // 8
        self.levelFeedbackY = self.screenHeight // 2 - self.levelFeedbackWidth // 2
        self.putSprite(SpritePrototypeFactory.TOP_ARROW_UP, TopFixedArrowSprite([self.openImage(Path.IMAGES_PATH + r"/top_arrow_up2.png"), self.openImage(Path.IMAGES_PATH + r"/top_arrow_clicked_up.png")], w=self.arrowSize, h=self.arrowSize, z=0))
        self.putSprite(SpritePrototypeFactory.TOP_ARROW_DOWN, TopFixedArrowSprite([self.openImage(Path.IMAGES_PATH + r"/top_arrow_down2.png"), self.openImage(Path.IMAGES_PATH + r"/top_arrow_clicked_down.png")], w=self.arrowSize, h=self.arrowSize,  z=0))
        self.putSprite(SpritePrototypeFactory.TOP_ARROW_LEFT, TopFixedArrowSprite([self.openImage(Path.IMAGES_PATH + r"/top_arrow_left2.png"), self.openImage(Path.IMAGES_PATH + r"/top_arrow_clicked_left.png")], w=self.arrowSize, h=self.arrowSize,  z=0))
        self.putSprite(SpritePrototypeFactory.TOP_ARROW_RIGHT, TopFixedArrowSprite([self.openImage(Path.IMAGES_PATH + r"/top_arrow_right2.png"), self.openImage(Path.IMAGES_PATH + r"/top_arrow_clicked_right.png")], w=self.arrowSize, h=self.arrowSize,  z=0))
        self.putSprite(SpritePrototypeFactory.ARROW_UP, ArrowSprite([self.openImage(Path.IMAGES_PATH + r"/arrow_up2.png")], w=self.arrowSize, h=self.arrowSize,  z=1))
        self.putSprite(SpritePrototypeFactory.ARROW_DOWN, ArrowSprite([self.openImage(Path.IMAGES_PATH + r"/arrow_down2.png")], w=self.arrowSize, h=self.arrowSize,  z=1))
        self.putSprite(SpritePrototypeFactory.ARROW_LEFT, ArrowSprite([self.openImage(Path.IMAGES_PATH + r"/arrow_left2.png")], w=self.arrowSize, h=self.arrowSize,  z=1))
        self.putSprite(SpritePrototypeFactory.ARROW_RIGHT, ArrowSprite([self.openImage(Path.IMAGES_PATH + r"/arrow_right2.png")], w=self.arrowSize, h=self.arrowSize,  z=1))
        self.putSprite(SpritePrototypeFactory.FEEDBACK_PERFECT, FeedbackSprite([self.openImage(Path.IMAGES_PATH + r"/feedback_perfect.png")], maxY=self.levelFeedbackY, w=self.levelFeedbackWidth, h=self.levelFeedbackHeight,  z=0))
        self.putSprite(SpritePrototypeFactory.FEEDBACK_GOOD, FeedbackSprite([self.openImage(Path.IMAGES_PATH + r"/feedback_good.png")], maxY=self.levelFeedbackY, w=self.levelFeedbackWidth, h=self.levelFeedbackHeight, z=0))
        self.putSprite(SpritePrototypeFactory.FEEDBACK_BAD, FeedbackSprite([self.openImage(Path.IMAGES_PATH + r"/feedback_bad.png")], maxY=self.levelFeedbackY, w=self.levelFeedbackWidth, h=self.levelFeedbackHeight, z=0))
        self.putSprite(SpritePrototypeFactory.FEEDBACK_MISS, FeedbackSprite([self.openImage(Path.IMAGES_PATH + r"/feedback_miss.png")], maxY=self.levelFeedbackY, w=self.levelFeedbackWidth, h=self.levelFeedbackHeight, z=0))

    def putSprite(self, spriteEnum, sprite):
        assert spriteEnum in range(1, 14) and isinstance(sprite, Sprite)
        self.__sprites[spriteEnum] = sprite

    def create(self, spriteEnum):
        assert spriteEnum in range(1, 14)
        return self.__sprites[spriteEnum].clone()

    def createTopFixedArrow(self, numOfTopArrow, spriteEnum):
        assert spriteEnum in range(9, 13)
        topArrowSprite = self.create(spriteEnum)
        topArrowSprite.setXY(self.countArrowX(numOfTopArrow), self.topFixedArrowY)
        return topArrowSprite

    def createArrow(self, numOfArrow, spriteEnum):
        assert spriteEnum in range(1, 5)
        arrowSprite = self.create(spriteEnum)
        arrowSprite.setXY(self.countArrowX(numOfArrow), self.screenHeight)
        arrowSprite.numOfArrow = numOfArrow
        return arrowSprite

    def createLevelFeedback(self, player, spriteEnum):
        assert spriteEnum in range(5, 9) and player in range(1, 3)
        levelFeedbackSprite = self.create(spriteEnum)
        levelFeedbackSprite.setXY(self.countLevelFeedbackX(player), levelFeedbackSprite.y)
        return levelFeedbackSprite

    def countArrowX(self, numOfTopArrow):
        """Return the appropriate x of the top fixed arrow. Each arrow fragment should be equally wide.
        So first count the start x point of the num of that arrow fragment, then move the x to the middle point of that
        arrow fragment, finally move back a half of the width of the arrow image should place the arrow in the center."""

        x = (numOfTopArrow-1) * self.arrowFragmentWidth + self.arrowFragmentWidth // 2 - self.arrowSize // 2
        return x

    def countLevelFeedbackX(self, player):
        x = self.screenWidth // 4 - self.levelFeedbackWidth // 2
        if player == SpritePrototypeFactory.PLAYER_2:  # the feedback should be at the right side.
            x += self.screenWidth // 2
        return x

    def openImage(self, fileName):
        loadedImage = QImage()
        if not loadedImage.load(fileName):
            return None
        return loadedImage
