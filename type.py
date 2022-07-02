from enum import IntEnum
class Type(IntEnum) :
    NEW = 1
    EDIT = 2
    REMOVE = 3
    CHECK = 4
    F_OPEN = 5
    F_NEW = 6 
    UNDO = 7
    REDO = 8
    ALL_REMOVE = 9