from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from packages.music.Player import Player, PlayerCallback


class QMediaPlayerAdapter(Player):
    def __init__(self, interval=1):
        self.__callback = None
        self.__player = QMediaPlayer()
        self.setNotifyInterval(interval)

    def setNotifyInterval(self, interval):
        self.__player.setNotifyInterval(interval)

    def setMusicPath(self, filePath):
        qUrl = QUrl(filePath)
        self.__player.setMedia(QMediaContent(qUrl))

    def getState(self):
        return self.__player.state()

    def getStatus(self):
        return self.__player.mediaStatus()

    def getPosition(self):
        return self.__player.position()

    def getDuration(self):
        return self.__player.duration()

    def start(self):
        if self.__player.state() != QMediaPlayer.NoMedia:
            self.__player.play()
            # self.__player.setPosition(self.__player.duration() - 2000)
        else:
            raise ValueError("The media of the player should be set before the player get started.")

    def pause(self):
        self.__player.pause()

    def stop(self):
        self.__player.stop()

    def setCallback(self, callback):
        '''if not isinstance(callback, PlayerCallback):
            raise TypeError("The callback should be instance of PlayerCallback.")'''

        self.__callback = callback
        self.__player.mediaStatusChanged.connect(self.__callback.onMediaStatusChanged)
        self.__player.stateChanged.connect(self.__callback.onStateChanged)
        self.__player.positionChanged.connect(self.__callback.onPlayerPositionChanged)
