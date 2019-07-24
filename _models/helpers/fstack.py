from templates.CustomErrors import FStackWrongInputTypeError


class FStack:
    """An immutable stack of callable"""

    __slots__ = ['_stackQueue', '_fullReturn']

    def __init__(self):
        """Constructor"""
        super().__setattr__("_stackQueue", [])
        super().__setattr__("_fullReturn", {})

    def __setattr__(self, name, value):
        """"""
        msg = "'%s' has no attribute %s" % (self.__class__, name)
        raise AttributeError(msg)

    def __str__(self):
        tmp = []
        for f in self._stackQueue:
            tmp.append(f.__name__)
        tmp.reverse()
        return str(tmp)

    def getStack(self) -> list:
        return self._stackQueue

    def stackIt(self, obj) -> callable:
        try:
            if callable(obj):
                self._stackQueue.append(obj)
            else:
                raise FStackWrongInputTypeError
        except FStackWrongInputTypeError:
            print(f"Stack Error. The given object <{obj}> type of {type(obj)} is not callable")
        except Exception as e:
            print(f"Unexpected Error Type {e} has arisen")

    def execTop(self):
        """Execute Top most stacked function removing it from stack"""
        obj = self._stackQueue.pop()
        try:
            if callable(obj):
                obj()
            else:
                raise FStackWrongInputTypeError
        except FStackWrongInputTypeError:
            print(f"Stack Execution Error. The given object <{obj}> type of {type(obj)} is not callable")
        except Exception as e:
            print(f"Unexpected Error Type {e} has arisen")

    def execSequentially(self):
        """Execute all stacked functions from Top to Bottom removing them from stack"""
        while self._stackQueue:
            obj = self._stackQueue.pop()
            try:
                if callable(obj):
                    self._fullReturn.update({obj.__name__: obj()})
                else:
                    raise FStackWrongInputTypeError
            except FStackWrongInputTypeError:
                print(f"Stack Execution Error. The given object <{obj}> type of {type(obj)} is not callable")
            except Exception as e:
                print(f"Unexpected Error Type {e} has arisen")

        if self._fullReturn:
            return self._fullReturn
