from enum import Enum

class FType(Enum):
    ABSORBED = 1
    POLYMER = 2
    MONOMER = 3

class CProperty(Enum):
    NONE = 0
    ATTACH = 1
    SUBTRACT = 2
    ATTRACT = 3
    REPEL = 4
    SPLIT = 5
    COMBINE = 6
    COPY = 7
    INCREASE_PH = 8
    DECREASE_PH = 9

class Dir(Enum):
    TOP = 0
    TOP_RIGHT = 1
    RIGHT = 2
    BOTTOM_RIGHT = 3
    BOTTOM = 4
    BOTTOM_LEFT = 5
    LEFT = 6
    TOP_LEFT = 7
