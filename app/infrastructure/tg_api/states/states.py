from enum import Enum


class GameState(Enum):
    PRE_START = 1
    START = 2
    PRE_BET = 3
    BET = 4
    PRE_MOTION = 5
    MOTION = 6
    STOP = 7


class PlayerState(Enum):
    WAIT = 1
    BET = 2
    MOTION = 3
    SKIP = 4
    LOSE = 5
