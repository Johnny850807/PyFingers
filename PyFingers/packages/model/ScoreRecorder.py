from packages.model import Level


class ScoreRecorder:

    def __init__(self):
        self.combo = 0
        self.maxCombo = 0
        self.nowScore = 0
        self.punches = {Level.PERFECT: list(), Level.GOOD: list(), Level.BAD: list(), Level.MISS: list()}
        # TODO finish all properties declaration.

    def record(self, punch):
        self.punches.get(punch.level).append(punch)
        self.nowScore += punch.level
        if punch.level is not Level.MISS:
            self.combo += 1
        else:
            self.combo = 0
        if self.maxCombo < self.combo:
            self.maxCombo = self.combo

    def countFinalScore(self):
        finalScore = self.getNowScore() + self.getMaxCombo() * 100
        return finalScore

    def getCombo(self):
        return self.combo

    def getMaxCombo(self):
        return self.maxCombo

    def getNowScore(self):
        return self.nowScore

    def perfect(self):
        return len(self.punches[Level.PERFECT])

    def good(self):
        return len(self.punches[Level.GOOD])

    def bad(self):
        return len(self.punches[Level.BAD])

    def miss(self):
        return len(self.punches[Level.MISS])
