from enum import Enum


class EState(Enum):
    IDLE: int = 0
    ACTIVE: int = 1
    STUCK: int = 2
    INITIATION: int = 3
