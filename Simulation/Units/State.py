# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


from enum import Enum, auto


class State(Enum):
    DOCKED = auto()
    PATROL = auto()
    ENGAGE = auto()
    SEARCH = auto()
    EVADE = auto()
    TRANSIT = auto()
    NONE = auto()
