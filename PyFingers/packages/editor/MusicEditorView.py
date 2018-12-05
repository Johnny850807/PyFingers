from abc import ABCMeta, abstractmethod


class MusicEditorView(metaclass=ABCMeta):
    @abstractmethod
    def onMusicStart(self):
        pass

    @abstractmethod
    def onEditCompleted(self):
        pass

    @abstractmethod
    def onNoteCreated(self, note):
        pass

    @abstractmethod
    def onSavingSheet(self, sheet):
        pass
