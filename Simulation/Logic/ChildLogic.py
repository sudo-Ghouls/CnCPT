# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


from shapely.geometry import Point

from Simulation.GeographyPhysics.core import bearing, haversine
from Simulation.Units.State import State


def return_to_parent(unit, time):
    if unit.state is not State.RTB:
        unit.state, unit.state_change_time = State.RTB, time
    my_location = Point(unit.kinematics.get_location())
    parent_location = Point(unit.parent.kinematics.get_location())
    distance_to_parent = haversine(my_location, parent_location)
    bearing_to_parent = bearing(my_location, parent_location)
    unit.kinematics.set_heading(bearing_to_parent)
    if distance_to_parent < unit.kinematics.get_speed() * unit.time_between_thoughts:
        dock(unit, time)


def dock(unit, time, refuel=True):
    if refuel:
        unit.state = State.DOCKED_REFUELING
    else:
        unit.state = State.DOCKED_READY
    unit.formation_lock = True
    unit.docked = True
    unit.state_change_time = time
    unit.kinematics.reset_range_traveled()


def undock(unit, new_state, time):
    unit.formation_lock = False
    unit.docked = False
    unit.state = new_state
    unit.state_change_time = time
