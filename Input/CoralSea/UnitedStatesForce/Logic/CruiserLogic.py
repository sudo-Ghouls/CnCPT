# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from Simulation.Communication.Message import DetectionMessage
from Simulation.GeographyPhysics.core import reckon
from Simulation.Logic.General import determine_priority_target_contact, pursue_target
from Simulation.Logic.Patrol import patrol
from Simulation.Units.State import State
from Simulation.Utility.Area import Area
from Simulation.Utility.Conversions import kts_to_ms


def behavior_aggressive(unit, simulation_manager):
    """

    """
    unit.kinematics.set_speed(kts_to_ms(20))


def behavior_passive(unit, simulation_manager):
    """

    """
    unit.kinematics.set_speed(kts_to_ms(20))


def behavior_baseline(unit, simulation_manager):
    """

    """
    unit.kinematics.set_speed(kts_to_ms(20))
