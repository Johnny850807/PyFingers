from packages.model.Sheet import Sheet


class SheetArranger:

    def __init__(self):
        self.__notes = []
        self.duration = None
        self.sheetName = None
        self.musicName = None
        self.musicFileTypeName = None

    def arrange(self, note):
        self.__notes.append(note)

    def setMusicInfo(self, sheetName, musicFileTypeName, duration):
        self.duration = duration
        self.sheetName = sheetName
        self.musicFileTypeName = musicFileTypeName
        self.musicName = self.sheetName + self.musicFileTypeName

    def buildSheet(self):
        return Sheet(notes=self.__notes, duration=self.duration, musicName=self.musicName)
