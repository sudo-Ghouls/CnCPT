# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


from shapely.geometry import Point
from CnCPT.Simulation.Units.State import State
from CnCPT.Simulation.GeographyPhysics import Geography


def return_to_parent(unit, time):
    my_location = Point(unit.kinematics.get_location())
    parent_location = Point(unit.parent.get_location())
    distance_to_parent = Geography.haversine(my_location, parent_location)
    bearing_to_parent = Geography.bearing(my_location, parent_location)
    unit.kinematics.set_heading(bearing_to_parent)
    if distance_to_parent < unit.kinematics.get_speed() * unit.time_between_thoughts:
        unit.docked = True
        unit.state = State.DOCKED
        unit.state_change_time = time
