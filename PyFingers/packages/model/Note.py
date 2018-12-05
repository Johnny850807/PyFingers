from packages.model import Arrow


class Note:

    def __init__(self, arrow=Arrow.UP, startTime=0):
        self.arrow = arrow
        self.startTime = startTime
    
    @property
    def arrow(self):  # getter
        return self.__arrow
    
    @arrow.setter
    def arrow(self, arrow): # setter
        assert arrow in Arrow.ARROWS, "finger should be in the enum of Note.Fingers"
        self.__arrow = arrow

    @property
    def startTime(self):
        return self.__startTime
    
    @startTime.setter
    def startTime(self, startTime):
        self.__startTime = startTime

    def __str__(self):
        return "Arrow number: {0}, startTime: {1}".format(self.arrow, self.startTime)

