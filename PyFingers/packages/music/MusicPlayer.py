import collections
import threading

import time
from PyQt5.QtCore import QTimer, QBasicTimer
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QFrame

import ThreadPool
from packages.MyUtils import Path
from packages.editor.SheetRecorder import SheetRecorder
from packages.music.Player import Player, PlayerCallback


class MusicPlayer(PlayerCallback):
    
    def __init__(self):
        self.countPosition = 0
        self.threadPool = ThreadPool.ThreadPool(1000)
        self.diffTime = 1114
        self.deviationTime = 200
        self.timer = QBasicTimer()
        self.__noteMap = collections.defaultdict(list)  # <startTime, note[]>
        self.__player = None
        self.__musicPlayerView = None
        self.sheetRecorder = None
        self.scoreRecorder = None
        self.sheet = None

    def setPlayer(self, player):
        if not isinstance(player, Player):
            raise TypeError("The player should be an instance of Player.")
        else:
            self.__player = player
            self.__player.setCallback(self)

    def setSheetRecorder(self, sheetRecorder):
        assert isinstance(sheetRecorder, SheetRecorder)
        self.sheetRecorder = sheetRecorder
        self.sheet = self.sheetRecorder.load()
        for note in self.sheet.getNotes():
            time = note.startTime - self.diffTime - self.deviationTime
            if time >= 0:
                self.__noteMap[time].append(note)
        print("Note amount: " + str(len(self.__noteMap.keys())))

    def setDiffTime(self, diffTime):
        self.diffTime = diffTime

    def setScoreRecorder(self, scoreRecorder):
        self.scoreRecorder = scoreRecorder

    def playSheet(self, sheetName):
        self.sheetRecorder.setSheetName(sheetName)
        self.sheet = self.sheetRecorder.load()
        self.__player.setMusicPath(Path.MUSICS_PATH + "/" + self.sheet.musicName)

    def stop(self):
        self.__player.stop()
        print("Music duration = " + str(self.__player.getDuration()))
        self.__player = None

    def setMusicPlayerView(self, musicPlayerView):
        self.__musicPlayerView = musicPlayerView

    def punch(self, punch):
        self.scoreRecorder.record(punch)

    def onPlayerPositionChanged(self, position):
        '''request = ThreadPool.makeRequests(self.notifyPositionUpdatedAndSendNewNote, [position])[0]
        self.threadPool.putRequest(request)
        self.threadPool.poll()'''
        # print(str(position))
        threading.Thread(target=self.notifyPositionUpdatedAndSendNewNote, args=[position]).start()

    def notifyPositionUpdatedAndSendNewNote(self, position):
        try:
            if position % 10 == 0:
                self.__musicPlayerView.onPositionUpdated()
            if position in self.__noteMap or (position + 1) in self.__noteMap or (position - 1) in self.__noteMap:  # send note if the position approaches to the note's start time.
                self.__musicPlayerView.onNewNotes(self.__noteMap[position])
                self.__noteMap.pop(position)
        except Exception as err:
            print(err)

    def onMediaStatusChanged(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.__musicPlayerView.onMusicOver()
            print("Position count: " + str(self.countPosition))
        elif status == QMediaPlayer.LoadedMedia:
            self.__player.start()

    def onStateChanged(self, state):
        if state == QMediaPlayer.PlayingState:
            self.__musicPlayerView.onMusicStart()
