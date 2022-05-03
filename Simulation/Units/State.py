# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


from enum import Enum, auto


class State(Enum):
    DOCKED_READY = auto()
    DOCKED_REFUELING = auto()
    PATROL = auto()
    ENGAGE = auto()
    SEARCH = auto()
    EVADE = auto()
    TRANSIT = auto()
    RTB = auto()
    NONE = auto()
