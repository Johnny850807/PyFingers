from packages.editor.SheetRecorder import SheetRecorder
from packages.model.Note import Note
from packages.model import Arrow
from packages.model.Sheet import Sheet


class BasicTextSheetRecorder(SheetRecorder):
    def load(self):
        notes = []
        filePath = self.sheetsDirectoryPath + "/" + self.sheetName + ".txt"
        with open(filePath, "r") as file:
            musicName, duration = file.readline().split("::")
            for line in file.readlines():
                arrow, startTime = line.split(" ")
                notes.append(Note(arrow=int(arrow), startTime=int(startTime)))
            return Sheet(duration=int(duration), musicName=musicName, notes=notes)

    def record(self, sheet):
        assert isinstance(sheet, Sheet)
        filePath = self.sheetsDirectoryPath + "/" + self.sheetName + ".txt"
        with open(filePath, "w") as file:
            file.write(sheet.musicName + "::" + str(sheet.duration) + "\n")
            for note in sheet.getNotes():
                file.write(str(note.arrow) + " " + str(note.startTime)+ "\n")
