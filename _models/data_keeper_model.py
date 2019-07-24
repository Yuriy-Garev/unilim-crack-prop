from templates.EventSystem import Event
from os import path


class DataKeeper(object):
    __instance = None

    class __DataKeeper(Event):
        def __init__(self):
            """Instantiated the object type of <Event> with the list() of Subscriptions"""

            super().__init__()
            self.root_dir = str(path.dirname(path.realpath(__file__))) + path.normpath("/data")
            self.DataDir = self.root_dir + path.normpath("/test.csv")
            print("Data dir:\t", self.root_dir)

            self.__entries = []
            self.__isNewState = None

        def UpdateEntries(self, **kwargs):
            n = len(self.__entries) - 1

            while n > 0:
                n = n - 1
                self.__entries[0].update(self.__entries.pop(1))

            if len(kwargs) != 0:
                self.__entries[0].update(kwargs)

        def GetLastEntry(self):
            self.UpdateEntries()
            return self.__entries[0][-1]

        def GetAllEntries(self):
            self.UpdateEntries()
            return self.__entries[0]

        def RmEntriesByKeys(self, *args):
            self.UpdateEntries()
            for i in args:
                del self.__entries[0][i]

        def GetEntryByKey(self, key):
            self.UpdateEntries()
            return self.__entries[0].get(key)

        def GetAvailableKeys(self):
            self.UpdateEntries()
            return list(self.__entries[0].keys())

        def AddEntries(self, **kwargs):
            if len(kwargs) != 0 and not self.__entries:
                self.__entries.append(kwargs)
            elif len(kwargs) != 0:
                self.__entries.append(kwargs)
                self.UpdateEntries(**kwargs)

        @property
        def State(self):
            """Returns current event State"""

            raise NotImplementedError

        @State.setter
        def State(self, *args, **kwargs):
            """Sets current event State"""

            raise NotImplementedError

        @State.deleter
        def State(self):
            """Resets current event State to the default"""

            raise NotImplementedError

    def __new__(cls):  # __new__ always a classmethod
        if not DataKeeper.__instance:
            DataKeeper.__instance = DataKeeper.__DataKeeper()
        return DataKeeper.__instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
