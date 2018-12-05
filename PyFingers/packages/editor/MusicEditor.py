import os
import threading

import time
from PyQt5.QtMultimedia import QMediaPlayer

from packages.MyUtils import copyBytesFile
from packages.editor.SheetRecorder import SheetRecorder
from packages.model.Note import Note
from packages.model.SheetArranger import SheetArranger
from packages.music.Player import Player, PlayerCallback


class MusicEditor(PlayerCallback):
    def __init__(self, musicsDirectoryPath, sheetArranger, sheetRecorder):
        self.__musicEditorView = None
        self.sheetName = None
        self.musicFileTypeName = None
        self.chosenMusicFileAbsolutePath = None
        self.player = None
        self.musicsDirectoryPath = musicsDirectoryPath
        assert isinstance(sheetArranger, SheetArranger) and isinstance(sheetRecorder, SheetRecorder)
        self.sheetArranger = sheetArranger
        self.sheetRecorder = sheetRecorder

    def setMusicEditorView(self, view):
        self.__musicEditorView = view

    def setPlayer(self, player):
        if not isinstance(player, Player):
            raise TypeError("The player should be an instance of Player")

        self.player = player
        self.player.setCallback(self)

    def arrange(self, arrow):
        threading.Thread(target=self.createNoteAndArrange, args=[arrow]).start()

    def isEditing(self):
        return self.player.getState() == QMediaPlayer.PlayingState

    def isMusicMediaPrepared(self):
        return self.player.getStatus() == QMediaPlayer.LoadedMedia

    def createNoteAndArrange(self, arrow):
        position = self.player.getPosition()
        note = Note(arrow=arrow, startTime=position)
        threading.Thread(target=self.__musicEditorView.onNoteCreated, args=[note]).start()
        self.sheetArranger.arrange(note)

    def setMusicPath(self, path):
        self.sheetName = self.getMusicNameFromPath(path)
        self.musicFileTypeName = self.sheetName[self.sheetName.rfind("."):]  # get the type name
        self.sheetName = self.sheetName[0:self.sheetName.rfind(".")]  # get the name before the type name
        self.sheetArranger.setMusicInfo(self.sheetName, self.musicFileTypeName, self.player.getDuration())
        self.chosenMusicFileAbsolutePath = path
        self.player.setMusicPath(self.chosenMusicFileAbsolutePath)
        self.sheetRecorder.setSheetName(self.sheetName)

    def getMusicNameFromPath(self, path):
        firstIndexOfSlash = path.rfind("/")
        return path[firstIndexOfSlash + 1:]

    def start(self):
        time.sleep(3)
        if self.player and self.player.getState() != QMediaPlayer.PlayingState:
            self.player.start()

    def stop(self):
        self.player.stop()
        self.player = None

    def onPlayerPositionChanged(self, position):
        pass  # the editor doesn't have to sync the position with the music

    def onMediaStatusChanged(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.saveSheetAndCompleteEditing()

    def onStateChanged(self, state):
        if state == QMediaPlayer.PlayingState:
            self.__musicEditorView.onMusicStart()

    def saveSheetAndCompleteEditing(self):
        sheet = self.sheetArranger.buildSheet()
        self.__musicEditorView.onSavingSheet(sheet)
        self.sheetRecorder.record(sheet)
        # copy the music file into resources file
        copyBytesFile(self.chosenMusicFileAbsolutePath, self.musicsDirectoryPath + "/" + self.sheetName + self.musicFileTypeName)
        self.__musicEditorView.onEditCompleted()
