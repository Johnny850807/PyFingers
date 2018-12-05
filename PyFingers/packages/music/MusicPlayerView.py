from abc import ABCMeta, abstractmethod


class MusicPlayerView(metaclass=ABCMeta):

    @abstractmethod
    def onMusicStart(self):
        pass

    @abstractmethod
    def onNewNotes(self, notes):
        pass

    @abstractmethod
    def onMusicOver(self):
        pass