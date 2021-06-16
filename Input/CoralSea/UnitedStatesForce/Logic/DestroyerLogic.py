# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from Simulation.GeographyPhysics.core import reckon
from Simulation.Logic.Patrol import patrol
from Simulation.Utility.Area import Area
from Simulation.Utility.Conversions import kts_to_ms


def behavior_aggressive(unit, _):
    """

    """
    if unit.group.leader is unit:
        if unit.area is None:
            # establish patrol area 150 miles into enemy territory
            my_location = unit.kinematics.get_location()
            center = reckon(150, 0, my_location[0], my_location[1], unit="nmi")
            unit.area = Area.create_patrol_area_from_center(center, 100, 100, unit='nmi')
        patrol(unit)
    unit.kinematics.set_speed(kts_to_ms(20))


def behavior_passive(unit, _):
    """

    """
    if unit.group.leader is unit:
        if unit.area is None:
            # establish patrol area 100 miles away from enemy territory
            my_location = unit.kinematics.get_location()
            center = reckon(100, 180, my_location[0], my_location[1], unit="nmi")
            unit.area = Area.create_patrol_area_from_center(center, 100, 100, unit='nmi')
        patrol(unit)
    unit.kinematics.set_speed(kts_to_ms(20))


def behavior_baseline(unit, _):
    """
    Just follow the baseline route you are initialized with
    """
    unit.kinematics.set_speed(kts_to_ms(20))
