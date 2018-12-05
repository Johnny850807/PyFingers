import sys

import os
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QMessageBox

from MyGameView import MyGameView
from MyMusicEditorView import MyMusicEditorView
from packages.MyUtils import decorateDefaultView, Path


class MyMainView(QMainWindow):
    WINDOW_WIDTH, WINDOW_HEIGHT = (800, 500)
    WINDOW_QSIZE = QSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    WIDGET_WIDTH = WINDOW_WIDTH - 20

    def __init__(self):
        super().__init__()
        self.musicEditorView = None
        self.gameView = None
        self.chooseMusicBtn = decorateDefaultView(QPushButton("選擇曲目"), MyMainView.WIDGET_WIDTH, 80)
        self.chooseMusicBtn.clicked.connect(self.chooseSongBtnOnClick)
        self.editMusicBtn = decorateDefaultView(QPushButton("音樂編輯器"), MyMainView.WIDGET_WIDTH, 80)
        self.editMusicBtn.clicked.connect(self.editMusicBtnOnClick)
        self.songListView = decorateDefaultView(QListWidget(), MyMainView.WIDGET_WIDTH, 300,
                                                bgcolor="#2B2B2B", fontColor="#A9B7C6", fontSize=19)
        self.songs = self.loadSongList()
        self.initLayout()

    def initLayout(self):
        self.setWindowTitle('PyFingers')
        centralWidget = QWidget()
        centralWidget.setLayout(self.initControls())
        self.setCentralWidget(centralWidget)
        self.setFixedSize(MyMainView.WINDOW_QSIZE)

    def initControls(self):
        vBar = QVBoxLayout()
        self.initSongListView()
        vBar.addWidget(self.chooseMusicBtn)
        vBar.addWidget(self.songListView)
        vBar.addWidget(self.editMusicBtn)
        return vBar

    def initSongListView(self):
        self.songListView.setSpacing(7)
        for i in self.songs:
            self.addSongItemInSongListView(i)

    def loadSongList(self):
        # remove the file type such as '.wav'
        return [path[0:path.rfind(".")] for path in os.listdir(Path.SHEETS_PATH)
                if "." in path]

    def addSongItemInSongListView(self, songName):
        item = QListWidgetItem(songName)
        item.setTextAlignment(Qt.AlignLeft)
        self.songListView.addItem(item)

    def start(self):
        self.show()

    def chooseSongBtnOnClick(self):
        currentItem = self.songListView.currentItem()
        if currentItem:
            self.gameView = MyGameView(self, currentItem.text())
            self.gameView.start()
        else:
            QMessageBox.question(self, 'Message', '請先在清單中選擇曲目唷！', QMessageBox.Ok)

    def onGameViewClosed(self):
        self.gameView = None

    def editMusicBtnOnClick(self):
        if not self.musicEditorView:
            self.musicEditorView = MyMusicEditorView(self)
            self.musicEditorView.start()

    def onEditorViewClosed(self):
        self.musicEditorView = None
        self.songListView.clear()
        self.songs = self.loadSongList()
        self.initSongListView()


if __name__ == '__main__':
    Path.initAbsolutePath(os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"))
    app = QApplication(sys.argv)
    mainView = MyMainView()
    mainView.start()
    sys.exit(app.exec_())
