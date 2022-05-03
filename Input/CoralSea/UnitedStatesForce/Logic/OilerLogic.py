# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from Simulation.GeographyPhysics.core import reckon
from Simulation.Logic.Patrol import patrol
from Simulation.Utility.Area import Area
from Simulation.Utility.Conversions import kts_to_ms


def behavior_baseline(unit, _):
    """
    Just follow the baseline route you are initialized with
    """
    unit.kinematics.set_speed(kts_to_ms(20))
