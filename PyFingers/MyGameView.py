import collections
import threading
import time
import traceback

from PyQt5.QtCore import QSize, Qt, QPoint, QBasicTimer
from PyQt5.QtGui import QPainter, QImage, QPen
from PyQt5.QtWidgets import QDialog, QFrame, QHBoxLayout, QMessageBox
from collections import defaultdict

from PyQt5.uic.properties import QtGui

from ThreadPool import *
from packages.MyUtils import decorateDefaultView, Path, Color
from packages.editor.BasicTxtSheetRecorder import BasicTextSheetRecorder
from packages.model import Arrow
from packages.model import Level
from packages.model.Punch import Punch
from packages.model.ScoreRecorder import ScoreRecorder
from packages.music.MusicPlayer import MusicPlayer
from packages.music.QMediaPlayerAdapter import QMediaPlayerAdapter

from packages.music.sprite.SpritePrototypeFactory import SpritePrototypeFactory


class MyGameView(QDialog):
    GAME_WIDTH, GAME_HEIGHT = (1120, 627)
    MIDDLE_X = GAME_WIDTH // 2
    WINDOW_QSIZE = QSize(GAME_WIDTH, GAME_HEIGHT)
    ARROW_COLOR_MAP = {Arrow.UP: Color.WHITE, Arrow.DOWN: Color.BLUE, Arrow.LEFT: Color.RED, Arrow.RIGHT: Color.GREEN}

    def __init__(self, parent, sheetName):
        super().__init__(parent)
        try:
            self.sheetName = sheetName
            self.gamePanel = decorateDefaultView(GameBoard(self), MyGameView.GAME_WIDTH, MyGameView.GAME_HEIGHT,
                                                 bgcolor="black")
            self.musicPlayer = self.initMusicPlayer()
            self.initLayout()
            self.launchMusicGame()
        except:
            print(traceback.format_exc())

    def initMusicPlayer(self):
        musicPlayer = MusicPlayer()
        musicPlayer.setMusicPlayerView(self.gamePanel)
        musicPlayer.setPlayer(QMediaPlayerAdapter())
        musicPlayer.setScoreRecorder(ScoreRecorder())
        sheetRecorder = BasicTextSheetRecorder(Path.SHEETS_PATH)
        sheetRecorder.setSheetName(self.sheetName)
        musicPlayer.setSheetRecorder(sheetRecorder)
        return musicPlayer

    def initLayout(self):
        panel = QHBoxLayout()
        panel.addWidget(self.gamePanel)
        self.setLayout(panel)
        self.setFixedSize(MyGameView.WINDOW_QSIZE)

    def launchMusicGame(self):
        self.musicPlayer.playSheet(self.sheetName)

    def start(self):
        self.show()

    def closeEvent(self, QCloseEvent):
        self.musicPlayer.stop()


# TODO solve metaclass conflict
class GameBoard(QFrame):
    SPEED = 1
    ARROW_NUM_MAP = {Arrow.UP: 3, Arrow.DOWN: 2, Arrow.LEFT: 1, Arrow.RIGHT: 4}
    NUM_ARROW_MAP = [-1, Arrow.UP, Arrow.DOWN, Arrow.LEFT, Arrow.RIGHT, Arrow.UP, Arrow.DOWN, Arrow.LEFT, Arrow.RIGHT]
    ARROW_SPRITE_MAP = {Arrow.UP: SpritePrototypeFactory.ARROW_UP, Arrow.DOWN: SpritePrototypeFactory.ARROW_DOWN,
                        Arrow.LEFT: SpritePrototypeFactory.ARROW_LEFT, Arrow.RIGHT: SpritePrototypeFactory.ARROW_RIGHT}
    KEY_ARROWNUM_MAP = {Qt.Key_W: 3, Qt.Key_S: 2, Qt.Key_A: 1, Qt.Key_D: 4,
                        Qt.Key_Up: 7, Qt.Key_Down: 6, Qt.Key_Left: 5, Qt.Key_Right: 8}
    LEVEL_MAP = {Level.PERFECT: SpritePrototypeFactory.FEEDBACK_PERFECT,
                 Level.GOOD: SpritePrototypeFactory.FEEDBACK_GOOD,
                 Level.BAD: SpritePrototypeFactory.FEEDBACK_BAD, Level.MISS: SpritePrototypeFactory.FEEDBACK_MISS}

    def __init__(self, parent):
        super().__init__(parent)
        self.fixedSprites = list(
            range(0, 8))  # eight fixed top arrow, each arrow should be put in the number of the arrow
        self.arrowSprites = []
        self.levelFeedbackSprites = [None] * 2  # level feedback of two players, [0] -> p1, [1] -> p2
        self.setFocusPolicy(Qt.StrongFocus)
        self.threadPool = ThreadPool(20)
        self.spritePrototypeFactory = SpritePrototypeFactory()
        self.spritePrototypeFactory.prepare(MyGameView.GAME_WIDTH, MyGameView.GAME_HEIGHT)
        self.createAllTopFixedArrow()
        self.scoreRecordersMap = defaultdict(ScoreRecorder)

    def createAllTopFixedArrow(self):
        numOfTopArrow = 1

        for spriteEnum in SpritePrototypeFactory.TOP_FIXED_ARROWS:
            for num in (numOfTopArrow, numOfTopArrow + 4):
                self.fixedSprites[num - 1] = self.spritePrototypeFactory.createTopFixedArrow(num, spriteEnum)
            numOfTopArrow += 1

    def paintEvent(self, event):
        try:
            painter = QPainter(self)
            self.paintMiddleLine(painter)
            self.drawSprites(painter, self.levelFeedbackSprites)
            self.drawSprites(painter, self.fixedSprites)
            self.drawSprites(painter, self.arrowSprites)
        except:
            print(traceback.format_exc())

    def drawSprites(self, painter, sprites):
        for sprite in sprites:
            if sprite:
                image = sprite.nextImage()
                painter.drawImage(sprite.x, sprite.y, image)

    def paintMiddleLine(self, painter):
        whitePen = QPen(Qt.white)
        whitePen.setWidth(8)
        painter.setPen(whitePen)
        painter.drawLine(QPoint(MyGameView.MIDDLE_X, 0), QPoint(MyGameView.MIDDLE_X, MyGameView.GAME_HEIGHT))

    def onMusicStart(self):
        print("Music Started.")

    def onMusicOver(self):
        print("Music Stopped.")  # TODO create score window
        p1SR = self.scoreRecordersMap[SpritePrototypeFactory.PLAYER_1]
        assert isinstance(p1SR, ScoreRecorder)
        p2SR = self.scoreRecordersMap[SpritePrototypeFactory.PLAYER_2]
        assert isinstance(p2SR, ScoreRecorder)
        p1Score = p1SR.countFinalScore()
        p2Score = p2SR.countFinalScore()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        winner = "P1" if p1Score > p2Score else "平手" if p1Score == p2Score else "P2"
        try:
            msg.setText("勝利者為：" + winner)
            msg.setStyleSheet("QLabel{min-width:160 px; text-align:center;font-size: 20px; font-family: 微軟正黑體;} QPushButton{ width:130px; font-size: 18px;  font-family: 微軟正黑體;}");
            msg.setInformativeText("分數結算以下...")
            msg.setWindowTitle("分數結算！")
            msg.setDetailedText("P1 最大 Combo " + str(p1SR.getMaxCombo()) + ", Perfect " + str(p1SR.perfect()) +
                                ", Good " + str(p1SR.good()) + ", Bad " + str(p1SR.bad()) + ", Miss " + str(p1SR.miss()) +
                                "\nP2 最大 Combo " + str(p2SR.getMaxCombo()) + ", Perfect " + str(p2SR.perfect()) +
                                ", Good " + str(p2SR.good()) + ", Bad " + str(p2SR.bad()) + ", Miss " + str(p2SR.miss())
                                )
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
            self.parent().close()
        except:
            print(traceback.format_exc())

    def onPositionUpdated(self):
        requests = makeRequests(self.updateSprite, self.arrowSprites + self.levelFeedbackSprites)
        [self.threadPool.putRequest(request) for request in requests]
        self.threadPool.wait()
        self.update()

    def updateSprite(self, sprite):
        if sprite:
            sprite.update()

    def onSpriteOutOfBound(self, sprite):
        self.arrowSprites.remove(sprite)
        player = SpritePrototypeFactory.PLAYER_1 if sprite.numOfArrow <= 4 else SpritePrototypeFactory.PLAYER_2
        level = Level.MISS
        self.makeFeedBack(player, level)

    def onNewNotes(self, notes):
        for note in notes:
            # print(str(note.startTime))
            threading.Thread(target=self.createAndAppendArrow, args=[note]).start()

    def createAndAppendArrow(self, note):
        arrowEnum = GameBoard.ARROW_SPRITE_MAP[note.arrow]
        numOfArrow = GameBoard.ARROW_NUM_MAP[note.arrow]
        spriteP1 = self.spritePrototypeFactory.createArrow(numOfArrow, arrowEnum)
        spriteP2 = self.spritePrototypeFactory.createArrow(numOfArrow + 4, arrowEnum)
        spriteP1.setContext(self)
        spriteP2.setContext(self)
        self.arrowSprites.append(spriteP1)
        self.arrowSprites.append(spriteP2)

    def keyPressEvent(self, event):
        key = event.key()
        try:
            if key in GameBoard.KEY_ARROWNUM_MAP:
                numOfArrow = GameBoard.KEY_ARROWNUM_MAP[key]
                self.fixedSprites[numOfArrow - 1].setClicked(True)
                self.detectPunch(numOfArrow)
        except:
            print(traceback.format_exc())

    def keyReleaseEvent(self, event):
        key = event.key()
        if key in GameBoard.KEY_ARROWNUM_MAP:
            numOfArrow = GameBoard.KEY_ARROWNUM_MAP[key]
            self.fixedSprites[numOfArrow - 1].setClicked(False)

    def detectPunch(self, numOfArrowPressed):
        player = SpritePrototypeFactory.PLAYER_1 if numOfArrowPressed <= 4 else SpritePrototypeFactory.PLAYER_2
        level = self.detectLevelAndRemovePunchedArrow(numOfArrowPressed)
        self.makeFeedBack(player, level)

    def makeFeedBack(self, player, level):
        feedbackSprite = self.spritePrototypeFactory.createLevelFeedback(player, GameBoard.LEVEL_MAP[level])
        self.levelFeedbackSprites[player - 1] = feedbackSprite  # TODO make punch and send it to the music player
        self.scoreRecordersMap[player].record(Punch(level=level, finger=Arrow.RIGHT))

    def detectLevelAndRemovePunchedArrow(self, numOfArrowPressed):
        fixArrow = self.fixedSprites[numOfArrowPressed - 1]
        numSprites = [sprite for sprite in self.arrowSprites if sprite.numOfArrow == numOfArrowPressed]
        minDiffY = 999
        minSprite = None
        for sprite in numSprites:
            diffY = abs(fixArrow.y - sprite.y)
            if diffY < minDiffY:
                minDiffY = diffY
                minSprite = sprite

        if minDiffY < 81:
            self.arrowSprites.remove(minSprite)
            if minDiffY < 30:
                return Level.PERFECT
            elif minDiffY < 48:
                return Level.GOOD
            else:
                return Level.BAD
        return Level.MISS
