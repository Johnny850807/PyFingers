from abc import ABCMeta, abstractmethod
import copy


class Sprite(metaclass=ABCMeta):
    def __init__(self, imgs, x=0, y=0, z=0, w=0, h=0):
        self.__curImgPointer = 0
        self.context = None  # TODO make context an interface
        self.imgs = imgs  # used for animation
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.z = z

    def setXY(self, x, y):
        self.x = x
        self.y = y

    def setWH(self, w, h):
        self.w = w
        self.h = h

    def setContext(self, context):
        self.context = context

    @abstractmethod
    def update(self):
        pass

    def nextImage(self):
        self.__curImgPointer = self.__curImgPointer + 1 if self.__curImgPointer != len(self.imgs)-1 else 0
        return self.imgs[self.__curImgPointer]

    def __lt__(self, other):
        return self.z < other.z

    def clone(self):
        return copy.copy(self)
