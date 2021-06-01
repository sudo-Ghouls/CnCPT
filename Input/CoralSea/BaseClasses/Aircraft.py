# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from Simulation.Units.State import State
from Simulation.Units.Unit import Unit


class Aircraft(Unit):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None, side=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side)
        self.state = State.DOCKED_READY
        self.docked = True
