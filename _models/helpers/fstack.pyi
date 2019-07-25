from typing import Callable, Dict, List


class FStack:

    __slots__: List[str]

    def __init__(self) -> None: ...

    def getStack(self) -> List: ...

    def stackIt(self, obj: Callable) -> Callable: ...

    def execTop(self) -> None: ...

    def execSequentially(self) -> Dict: ...
