from packages.model import Arrow, Level


class Punch:

    def __init__(self, level=Level.PERFECT, finger=Arrow.UP):
        self.level = level
        self.finger = finger