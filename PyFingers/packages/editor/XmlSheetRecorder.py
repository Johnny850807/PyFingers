from packages.editor.SheetRecorder import SheetRecorder


class XmlSheetRecorder(SheetRecorder):
    # TODO the xml I/O

    def record(self, sheet):
        print("Sheet recorded.")
    
    def load(self):
        print(self.sheetName)
