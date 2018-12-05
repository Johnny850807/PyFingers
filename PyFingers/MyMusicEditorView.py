import threading
from os.path import expanduser

import time
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QPushButton, QLabel, QFrame, QVBoxLayout, QHBoxLayout, QDialog, \
    QFileDialog, QMessageBox


from packages.MyUtils import decorateDefaultView, Path, Color
from packages.editor.BasicTxtSheetRecorder import BasicTextSheetRecorder
from packages.editor.MusicEditor import MusicEditor
from packages.editor.XmlSheetRecorder import XmlSheetRecorder
from packages.model.SheetArranger import SheetArranger
from packages.music.QMediaPlayerAdapter import QMediaPlayerAdapter
from packages.model import Arrow


# TODO to solve meta class conflict
class MyMusicEditorView(QDialog):
    RIGHT_COLUMN_WIDTH = 350
    WINDOW_WIDTH, WINDOW_HEIGHT = (245 + RIGHT_COLUMN_WIDTH, 325)
    WINDOW_QSIZE = QSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    ARROW_KEY_MAP = {Qt.Key_Left: Arrow.LEFT, Qt.Key_Right: Arrow.RIGHT, Qt.Key_Up: Arrow.UP, Qt.Key_Down: Arrow.DOWN}
    ARROW_COLOR_MAP = {Arrow.UP: Color.WHITE, Arrow.DOWN: Color.BLUE, Arrow.LEFT: Color.RED, Arrow.RIGHT: Color.GREEN}

    def __init__(self, parent):
        super().__init__(parent)
        self.panelPainting = False  # the variable used for put a lock on the punchPaintingPanel preventing multiple paintings at the same time.
        self.musicEditor = self.initMusicEditor()
        self.setFocusPolicy(Qt.StrongFocus)
        self.chooseMusicFileBtn = decorateDefaultView(QPushButton("選擇音樂檔案"), MyMusicEditorView.RIGHT_COLUMN_WIDTH, 53)
        self.startEditingBtn = decorateDefaultView(QPushButton("開始編輯"), MyMusicEditorView.RIGHT_COLUMN_WIDTH, 53)
        self.fileNameLabel = decorateDefaultView(QLabel("尚未載入檔案"), MyMusicEditorView.RIGHT_COLUMN_WIDTH, 30,
                                                 fontSize=15)
        self.punchPaintingPanel = decorateDefaultView(QFrame(), 159, 243, bgcolor="black")
        self.__connectAllWidgetSignals()
        self.__initLayout()

    def initMusicEditor(self):
        recorder = BasicTextSheetRecorder(Path.SHEETS_PATH)
        editor = MusicEditor(Path.MUSICS_PATH, SheetArranger(), recorder)  # dependency injection
        editor.setMusicEditorView(self)
        editor.setPlayer(QMediaPlayerAdapter())
        return editor

    def __connectAllWidgetSignals(self):
        self.chooseMusicFileBtn.clicked.connect(self.chooseMusicFileBtnOnClick)
        self.startEditingBtn.clicked.connect(self.startEditingBtnOnClick)

    def __initLayout(self):
        self.setWindowTitle('PyFingers')
        self.setLayout(self.initControls())
        self.setFixedSize(MyMusicEditorView.WINDOW_QSIZE)

    def initControls(self):
        hBar = QHBoxLayout()
        rightColumn = QVBoxLayout()
        hBar.addWidget(self.punchPaintingPanel)
        hBar.addLayout(rightColumn)

        rightColumn.addWidget(self.chooseMusicFileBtn)
        rightColumn.addWidget(self.fileNameLabel)
        rightColumn.addWidget(self.startEditingBtn)
        return hBar

    def start(self):
        self.show()

    def keyPressEvent(self, event):
        if self.musicEditor.isEditing():
            key = event.key()
            if key in MyMusicEditorView.ARROW_KEY_MAP:
                arrow = MyMusicEditorView.ARROW_KEY_MAP[key]
                self.musicEditor.arrange(arrow)

    def chooseMusicFileBtnOnClick(self):
        fileChosen = QFileDialog.getOpenFileName(self, caption='開啟音樂檔案', directory=expanduser('~'),
                                                 filter='Audio (*.mp3 *.ogg *.wav)',
                                                 initialFilter='*.mp3 *.ogg *.wav')
        print(fileChosen)
        musicFilePath = fileChosen[0]
        if len(musicFilePath) != 0:
            self.fileNameLabel.setText(musicFilePath)
            self.musicEditor.setMusicPath(musicFilePath)

    def startEditingBtnOnClick(self):
        if self.musicEditor.isMusicMediaPrepared():
            self.fileNameLabel.setText("Ready !!!")
            threading.Thread(target=self.musicEditor.start).start()

    def onNoteCreated(self, note):
        if not self.panelPainting:
            try:
                self.panelPainting = True
                color = MyMusicEditorView.ARROW_COLOR_MAP[note.arrow]
                self.punchPaintingPanel.setStyleSheet("background-color:  rgb" + str(color))  # make flash
                time.sleep(0.0522)
                self.punchPaintingPanel.setStyleSheet("background-color:  rgb(0, 0, 0)")  # change the bg back to the black
                self.panelPainting = False
            except Exception as err:
                print (err)
        else:
            print("Painting blocked.")

    def onSavingSheet(self, sheet):
        self.fileNameLabel.setText("正在儲存樂譜 " + (sheet.musicName if sheet else "") + " ...")

    def onEditCompleted(self):
        self.fileNameLabel.setText("儲存完畢")
        QMessageBox.question(self, '完成了', '音樂編輯已完成，可以在清單中進行歌曲囉！', QMessageBox.Ok)
        self.close()

    def onMusicStart(self):
        self.fileNameLabel.setText("編輯開始，請點選上下左右編曲。")

    def closeEvent(self, QCloseEvent):
        self.musicEditor.stop()
        self.parent().onEditorViewClosed()  # notify that the editor is closed or finished.
