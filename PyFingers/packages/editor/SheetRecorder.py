from abc import ABCMeta, abstractmethod


class SheetRecorder(metaclass=ABCMeta):
    def __init__(self, sheetsDirectoryPath):
        self.sheetsDirectoryPath = sheetsDirectoryPath
        self.sheetName = None

    @abstractmethod
    def record(self, sheet):
        pass

    @abstractmethod
    def load(self):
        pass

    def setSheetName(self, sheetName):
        self.sheetName = sheetName
