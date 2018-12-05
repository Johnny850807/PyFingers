import os


def copyBytesFile(fromFileName, toFileName):
    with open(fromFileName, "rb") as in_file:  # opening for [r]eading as [b]inary
        data = in_file.read()  # if you only wanted to read 512 bytes, do .read(512)
        with open(toFileName, "wb") as out_file:
            out_file.write(data)


def decorateDefaultView(view, width, height, bgcolor="white", fontColor="black", fontSize=22):
    view.setFixedSize(width, height)
    view.setStyleSheet("background-color:" + bgcolor + "; color:" + fontColor + "; font-family:  Microsoft JhengHei, "
                                                                                "新細明體; font-style: bold; font-size:" + str(
        fontSize) + "px")
    return view


class Path:
    RESOURCES_PATH = None
    SHEETS_PATH = None
    MUSICS_PATH = None
    IMAGES_PATH = None

    @staticmethod
    def initAbsolutePath(rootDirectory):
        Path.RESOURCES_PATH = rootDirectory + r"/resources"
        Path.SHEETS_PATH = Path.RESOURCES_PATH + r"/sheets"
        Path.MUSICS_PATH = Path.SHEETS_PATH + r"/musics"
        Path.IMAGES_PATH = Path.RESOURCES_PATH + r"/img"


class Color:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
