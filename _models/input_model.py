class InputModel:
    def __init__(self):
        self.iEntries = []

    # If This method is implemented then it will be used instead of repr and str for print
    def __str__(self):
        return "Last received data entry:\n{}".format(self.iEntries.pop())

    @staticmethod
    def ParseEntry(entry):
        raise NotImplementedError

    def AddNewEntries(self, entries):
        if entries is None or not entries:
            raise Exception("Wrong input data type.")
        else:
            for entry in entries:
                self.iEntries.append(self.ParseEntry(entry))

    def AddNewEntry(self, entry):
        if entry is None or not entry:
            raise Exception("Wrong input data type.")
        else:
            self.iEntries.append(self.ParseEntry(entry))
