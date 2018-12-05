
class Sheet:
    #  TODO complete the sheet class and make it iterable

    def __init__(self, duration=None, musicName=None, notes=None):
        self.__notes = notes
        self.duration = duration
        self.musicName = musicName

    def __iter__(self):
        pass

    def getNotes(self):
        return self.__notes

