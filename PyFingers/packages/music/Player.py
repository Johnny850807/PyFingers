from abc import ABCMeta, abstractmethod


class Player(metaclass=ABCMeta):
    @abstractmethod
    def getPosition(self):
        pass

    @abstractmethod
    def setCallback(self, callback):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def getState(self):
        pass

    @abstractmethod
    def getStatus(self):
        pass

    @abstractmethod
    def getDuration(self):
        pass

    @abstractmethod
    def setMusicPath(self, path):
        pass


class PlayerCallback(metaclass=ABCMeta):
    @abstractmethod
    def onMediaStatusChanged(self, status):
        pass

    @abstractmethod
    def onStateChanged(self, state):
        pass

    @abstractmethod
    def onPlayerPositionChanged(self, position):
        pass

